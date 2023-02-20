from PyPDF2 import PdfReader
import subprocess
import os

def extract_share_pdf_values(pdf_path):

    reader = PdfReader(pdf_path)
    page = reader.pages[0] #page index, 0 = page 1
    split_pdf_text = page.extract_text().split("\n") #split the text into a list, by line

    # Get the value of a detail (e.g. Gross, Commission, etc.)
    def detail_value(detail):
        for index, line in enumerate(split_pdf_text): #iterate through the list, while grabbing the index
            if detail in line:
                return split_pdf_text[index].split(detail)[1] #peform some string magic to get the value

    # Get the quantity, buy price, currency flag, and ticker
    for index, line in enumerate(split_pdf_text):
        if line == "Quantity Price per Share Security":
            qps_data = split_pdf_text[index+1].split(" ") #peform some string magic to get a list of the quantity, buy price, currency flag, and ticker
            break

    quantity = qps_data[0]
    buy_price = qps_data[1]
    currency_flag = qps_data[2]
    ticker = qps_data[3]
    gross = detail_value("Gross: ")
    commission = detail_value("Commission: ")
    net_amount = detail_value("Net Amount: ")
    for_settlement_on = detail_value("For Settlement On: ")

    return quantity, buy_price, currency_flag, ticker, gross, commission, net_amount, for_settlement_on

if __name__ == "__main__":
    quantity, buy_price, currency_flag, ticker, gross, commission, net_amount, for_settlement_on = extract_share_pdf_values('wealthsimple.pdf')
    
    print(f"Quantity: {quantity}")
    print(f"Buy Price: {buy_price}")
    print(f"Currency Flag: {currency_flag}")
    print(f"Ticker: {ticker}")
    print(f"Gross: {gross}")
    print(f"Commission: {commission}")
    print(f"Net Amount: {net_amount}")
    print(f"For Settlement On: {for_settlement_on}")
