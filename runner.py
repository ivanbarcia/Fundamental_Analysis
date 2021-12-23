import asyncio
import sqlite3
from fundamental_indicators_provider import Company, get_fundamental_indicators_for_company

import pandas as pd

def insert_stock_data(companies):
    con = sqlite3.connect('fundamental_analysis')
    cur = con.cursor()

    cur.execute(''' CREATE TABLE IF NOT EXISTS stock_data ( 
                            Ticker text PRIMARY KEY, 
                            MarketCap real NOT NULL, 
                            PS real NOT NULL, 
                            PE real NOT NULL, 
                            PEG real NOT NULL, 
                            PB real NOT NULL, 
                            ProfitMargin real NOT NULL, 
                            OperMargin real NOT NULL, 
                            CurrentRatio real NOT NULL, 
                            DivPayoutRatio real NOT NULL, 
                            ROA real NOT NULL, 
                            ROE real NOT NULL, 
                            CashShare real NOT NULL, 
                            BookShare real NOT NULL, 
                            DebtEquity real NOT NULL  ) ''')

    qmarks = ', '.join('?' * len(companies))
    query = "INSERT INTO stock_data (Ticker, MarketCap, PS, PE, PEG, PB, ProfitMargin, OperMargin, CurrentRatio, DivPayoutRatio, ROA, ROE, CashShare, BookShare, DebtEquity) VALUES (%s, %s)" % (company.symbol, qmarks)
    cur.execute(query, companies.values())
    # cur.execute(''' INSERT OR IGNORE INTO stock_data (Ticker, MarketCap, PS, PE, PEG, PB, ProfitMargin, OperMargin, CurrentRatio, DivPayoutRatio, ROA, ROE, CashShare, BookShare, DebtEquity)
    #                 VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ) ''', (company.symbol, company.fundamental_indicators.MarketCap, company.fundamental_indicators.PS, company.fundamental_indicators.PE,  company.fundamental_indicators.PEG, company.fundamental_indicators.PB, company.fundamental_indicators.ProfitMargin, company.fundamental_indicators.OperMargin, company.fundamental_indicators.CurrentRatio, company.fundamental_indicators.DivPayoutRatio, company.fundamental_indicators.ROA, company.fundamental_indicators.ROE, company.fundamental_indicators.CashShare, company.fundamental_indicators.BookShare, company.fundamental_indicators.DebtEquity) )

    con.commit()

    for row in cur.execute(''' SELECT * FROM stock_data '''):
        print(row)


def save_excel(companies):
    # Save company values into Excel
    
    current = pd.DataFrame(companies) 
        
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("Fundamental_analysis.xlsx", engine="xlsxwriter")

    # Convert the dataframe to an XlsxWriter Excel object.
    current.to_excel(writer, sheet_name="Companies", index=False, freeze_panes=(1, 1))

    # # Get the xlsxwriter workbook and worksheet objects.
    # workbook = writer.book
    # worksheet = writer.sheets["Companies"]

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    writer.close()


def take_values(company):    
    # Note: You might want to create an event loop and run within the loop:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_fundamental_indicators_for_company(config, company))
    
    print(company.symbol + ' --> ')
    print(company.fundamental_indicators)

    company.fundamental_indicators['company'] = company.symbol
    
    companies.append(company.fundamental_indicators)
    

if __name__ == "__main__":
    config = {}
    companies = list()
    
    company = Company('AAPL')
    take_values(company)
    
    company = Company('NVDA')
    take_values(company)
    
    company = Company('JPM')
    take_values(company)
    
    # Save data into Excel
    save_excel(companies)
    
    # Save data
    # insert_stock_data(companies)