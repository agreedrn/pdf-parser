from PyPDF2 import PdfReader
import yfinance as yf #new, used to grab yahoo finanace api data
import subprocess
import os

def extract_share_pdf_values():
    for (root,dirs,files) in os.walk('/'):
        if "$Recycle.Bin" in root: #do not want to search the recycle bin
            continue
        if "wealthsimple.pdf" in files:
            pdf_path = root+"/wealthsimple.pdf"
            break
    else:
        raise Exception("Pdf File Not Found. Make sure it is on your system and named 'wealthsimple.pdf'.")

    print(f"Found PDF: {pdf_path}")

    reader = PdfReader(pdf_path)
    page = reader.pages[0] #page index, 0 = page 1
    split_pdf_text = page.extract_text().split("\n")

    detail_value = lambda detail: [split_pdf_text[index].split(detail) for index, line in enumerate(split_pdf_text) if detail in line][0][1]
    qps_data = [split_pdf_text[index+1].split(" ") for index, line in enumerate(split_pdf_text) if line == "Quantity Price per Share Security"][0] #qps_data = Quantity, Price & Share data

    quantity = float(qps_data[0])
    buy_price = float(qps_data[1].replace('$', ''))
    currency_flag = qps_data[2]
    ticker = qps_data[3]
    stock_info = yf.Ticker(ticker).info
    stock_name = stock_info["longName"]
    gross = detail_value("Gross: ")
    commission = detail_value("Commission: ")
    net_amount = detail_value("Net Amount: ")
    for_settlement_on = detail_value("For Settlement On: ")

    return quantity, buy_price, currency_flag, ticker, stock_info, stock_name, gross, commission, net_amount, for_settlement_on

if __name__ == "__main__":
    quantity, buy_price, currency_flag, ticker, stock_info, stock_name, gross, commission, net_amount, for_settlement_on = extract_share_pdf_values()
    
    print(f"Quantity: {quantity}")
    print(f"Buy Price: {buy_price}")
    print(f"Currency Flag: {currency_flag}")
    print(f"Ticker: {ticker}")
    print(f"Stock Name: {stock_name}")
    print(f"Gross: {gross}")
    print(f"Commission: {commission}")
    print(f"Net Amount: {net_amount}")
    print(f"For Settlement On: {for_settlement_on}")
