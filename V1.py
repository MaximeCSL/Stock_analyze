#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:48:06 2023

@author: casalino
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.widgets import Cursor
import datetime
import pandas as pd
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands

# Liste de noms d'entreprises et leurs symboles de ticker associés
EURO_STOCK_50 = {
    'Sanofi': 'SAN.PA', 
    'SAP': 'SAP', 
    'Allianz': 'ALV.DE', 
    'ASML Holding': 'ASML', 
    'LVMH': 'MC.PA', 
    'Linde': 'LIN', 
    'Siemens': 'SIE.DE', 
    'Total': 'FP.PA', 
    'Deutsche Telekom': 'DTE.DE', 
    'Enel': 'ENEL.MI', 
    'Unilever': 'UNA.AS', 
    'Diageo': 'DGE.L', 
    'BNP Paribas': 'BNP.PA', 
    'Anheuser-Busch InBev': 'ABI.BR', 
    'Air Liquide': 'AI.PA', 
    'EssilorLuxottica': 'EL.PA', 
    'AstraZeneca': 'AZN.L', 
    'Industria de Diseno Textil': 'ITX.MC',
    'Adidas': 'ADS.DE',
    'Apple Inc.': 'AAPL',
    'Microsoft Corporation': 'MSFT',
    'Amazon.com, Inc.': 'AMZN',
    'Alphabet Inc.': 'GOOGL',
    'Facebook, Inc.': 'FB',
    'Tesla, Inc.': 'TSLA',
    'Johnson & Johnson': 'JNJ',
    'JPMorgan Chase & Co.': 'JPM',
    'Visa Inc.': 'V',
    'Nestle S.A.': 'NESN.SW',
    'Procter & Gamble Co.': 'PG',
    'Samsung Electronics Co., Ltd.': '005930.KS',
    'Toyota Motor Corporation': 'TM',
    'Alibaba Group Holding Limited': 'BABA',
    'Walmart Inc.': 'WMT',
    'Intel Corporation': 'INTC',
    'Netflix, Inc.': 'NFLX',
    'Mastercard Incorporated': 'MA',
    'Adobe Inc.': 'ADBE',
    'Cisco Systems, Inc.': 'CSCO',
    'Pfizer Inc.': 'PFE',
    'Oracle Corporation': 'ORCL',
    'Coca-Cola Company': 'KO',
    'Merck & Co., Inc.': 'MRK',
    'McDonald\'s Corporation': 'MCD',
    'Nike, Inc.': 'NKE',
    'Accenture plc': 'ACN',
    'Verizon Communications Inc.': 'VZ',
    'Sony Group Corporation': 'SONY',
    'Novartis AG': 'NOVN.SW',
    'Comcast Corporation': 'CMCSA',
    'Citigroup Inc.': 'C',
    'General Electric Company': 'GE',
    'Home Depot, Inc.': 'HD',
    'AT&T Inc.': 'T',
    'Abbott Laboratories': 'ABT',
    'Exxon Mobil Corporation': 'XOM',
    'Boeing Company': 'BA',
    'AbbVie Inc.': 'ABBV',
    'Novartis AG': 'NVS',
    'Walt Disney Company': 'DIS',
    'Intel Corporation': 'INTC',
    'Caterpillar Inc.': 'CAT',
    'Oracle Corporation': 'ORCL',
    'Citigroup Inc.': 'C',
    'PepsiCo, Inc.': 'PEP',
    'British American Tobacco plc': 'BATS.L',
    'BHP Group Limited': 'BHP',
    'IBM Corporation': 'IBM',
    'General Motors Company': 'GM',
    'CME Group Inc.': 'CME',
    'Medtronic plc': 'MDT',
    'Charter Communications, Inc.': 'CHTR',
    'Raytheon Technologies Corporation': 'RTX',
    'BlackRock, Inc.': 'BLK',
    'Sony Group Corporation': 'SONY',
    'Amgen Inc.': 'AMGN',
    'Daimler AG': 'DAI.DE',
    'T-Mobile US, Inc.': 'TMUS',
    'Siemens AG': 'SIEGY',
    'Bristol-Myers Squibb Company': 'BMY',
    'TotalEnergies SE': 'TTE.PA',
    'L\'Oreal SA': 'OR.PA',
    'Pfizer Inc.': 'PFE',
    'Netflix, Inc.': 'NFLX',
    'Nike, Inc.': 'NKE',
    'The Goldman Sachs Group, Inc.': 'GS',
    'Colgate-Palmolive Company': 'CL',
    'Novo Nordisk A/S': 'NVO',
    'Honda Motor Co., Ltd.': 'HMC',
    'Deutsche Bank AG': 'DB',
    'Costco Wholesale Corporation': 'COST',
    'Adobe Inc.': 'ADBE',
    'Novo Nordisk A/S': 'NOVO-B.CO',
    'ASML Holding N.V.': 'ASML',
    'Rio Tinto Group': 'RIO',
    'Chevron Corporation': 'CVX',
    'PNC Financial Services Group, Inc.': 'PNC',
    'JD.com, Inc.': 'JD',
    'BHP Group Plc': 'BBL',
    'Citigroup Inc.': 'C',
    'NVIDIA Corporation': 'NVDA',
    'Thermo Fisher Scientific Inc.': 'TMO',
    'Royal Dutch Shell plc': 'RDS-A',
    'UnitedHealth Group Incorporated': 'UNH',
    'AIA Group Limited': '1299.HK',
    'Pinduoduo Inc.': 'PDD',
    'QUALCOMM Incorporated': 'QCOM',
    'Intuit Inc.': 'INTU',
    'Texas Instruments Incorporated': 'TXN',
    'Thermo Fisher Scientific Inc.': 'TMO',
    'Biogen Inc.': 'BIIB',
    'Starbucks Corporation': 'SBUX',
    'Adobe Inc.': 'ADBE',
    'ASML Holding N.V.': 'ASML',
    'Medtronic plc': 'MDT',
    'Pinduoduo Inc.': 'PDD',
    'Toyota Motor Corporation': 'TM',
    'Abbott Laboratories': 'ABT',
    'Medtronic plc': 'MDT',
    'General Electric Company': 'GE',
    'BHP Group Limited': 'BHP',
    'United Parcel Service, Inc.': 'UPS',
    'Exelon Corporation': 'EXC',
    'Bank of America Corporation': 'BAC',
    'Adobe Inc.': 'ADBE',
    'Novartis AG': 'NVS',
    'Airbus SE': 'AIR.PA',
    'The Goldman Sachs Group, Inc.': 'GS',
    'Honeywell International Inc.': 'HON',
    'Nestle S.A.': 'NSRGF',
    'Novo Nordisk A/S': 'NVO',
    'JD.com, Inc.': 'JD',
    'Starbucks Corporation': 'SBUX',
    'Danaher Corporation': 'DHR',
    'The Coca-Cola Company': 'KO',
    'AbbVie Inc.': 'ABBV',
    'Abbott Laboratories': 'ABT',
    'Intuit Inc.': 'INTU',
    'Union Pacific Corporation': 'UNP',
    'McDonald\'s Corporation': 'MCD',
    'Comcast Corporation': 'CMCSA',
    'Vale S.A.': 'VALE',
    'Nike, Inc.': 'NKE',
    'Honeywell International Inc.': 'HON',
    'BHP Group Plc': 'BBL',
    'Thermo Fisher Scientific Inc.': 'TMO',
    'Deutsche Bank AG': 'DB',
    'Texas Instruments Incorporated': 'TXN',
    'Bayer AG': 'BAYN.DE',
    'TotalEnergies SE': 'TTE.PA',
    'Chevron Corporation': 'CVX',
    'Biogen Inc.': 'BIIB',
    'Amgen Inc.': 'AMGN',
    'Colgate-Palmolive Company': 'CL',
    'Rio Tinto Group': 'RIO',
    'ASML Holding N.V.': 'ASML',
    'PNC Financial Services Group, Inc.': 'PNC',
    'General Motors Company': 'GM',
    'Cisco Systems, Inc.': 'CSCO',
    'Intuit Inc.': 'INTU',
    'Exelon Corporation': 'EXC',
    'JD.com, Inc.': 'JD',
    'Pfizer Inc.': 'PFE',
    'Netflix, Inc.': 'NFLX',
    'Amgen Inc.': 'AMGN',
    'Medtronic plc': 'MDT',
    'Deutsche Bank AG': 'DB',
    'Texas Instruments Incorporated': 'TXN',
    'Bayer AG': 'BAYN.DE',
    'PNC Financial Services Group, Inc.': 'PNC',
    'General Motors Company': 'GM',
    'NVIDIA Corporation': 'NVDA',
    'Cisco Systems, Inc.': 'CSCO',
    'JD.com, Inc.': 'JD',
    'Exelon Corporation': 'EXC',
    'Intuit Inc.': 'INTU',
    'Colgate-Palmolive Company': 'CL',
    'ASML Holding N.V.': 'ASML',
    'Amgen Inc.': 'AMGN',
    'Medtronic plc': 'MDT',
    'General Electric Company': 'GE',
    'BHP Group Limited': 'BHP',
    'United Parcel Service, Inc.': 'UPS',
    'Exelon Corporation': 'EXC',
    'Bank of America Corporation': 'BAC',
    'Novartis AG': 'NVS',
    'The Goldman Sachs Group, Inc.': 'GS',
    'Honeywell International Inc.': 'HON',
    'Nestle S.A.': 'NSRGF',
    'Novo Nordisk A/S': 'NVO',
    'JD.com, Inc.': 'JD',
    'Starbucks Corporation': 'SBUX',
    'Danaher Corporation': 'DHR',
    'The Coca-Cola Company': 'KO',
    'AbbVie Inc.': 'ABBV',
    'Abbott Laboratories': 'ABT',
    'Intuit Inc.': 'INTU',
    'Union Pacific Corporation': 'UNP',
    'McDonald\'s Corporation': 'MCD',
    'Comcast Corporation': 'CMCSA',
    'Vale S.A.': 'VALE',
    'Nike, Inc.': 'NKE',
    'Honeywell International Inc.': 'HON',
    'BHP Group Plc': 'BBL',
    'Thermo Fisher Scientific Inc.': 'TMO',
    'Deutsche Bank AG': 'DB',
    'Texas Instruments Incorporated': 'TXN',
    'Bayer AG': 'BAYN.DE',
    'TotalEnergies SE': 'TTE.PA',
    'Chevron Corporation': 'CVX',
    'Biogen Inc.': 'BIIB',
    'Amgen Inc.': 'AMGN',
    'Colgate-Palmolive Company': 'CL',
    'Rio Tinto Group': 'RIO',
    'ASML Holding N.V.': 'ASML',
    'PNC Financial Services Group, Inc.': 'PNC',
    'General Motors Company': 'GM',
    'Cisco Systems, Inc.': 'CSCO',
    'Intuit Inc.': 'INTU',
    'Exelon Corporation': 'EXC',
    'JD.com, Inc.': 'JD',
    'Pfizer Inc.': 'PFE',
    'Netflix, Inc.': 'NFLX',
    'Amgen Inc.': 'AMGN',
    'Medtronic plc': 'MDT',
    'Deutsche Bank AG': 'DB',
    'Texas Instruments Incorporated': 'TXN',
    'Bayer AG': 'BAYN.DE',
    'PNC Financial Services Group, Inc.': 'PNC',
  }


class StockAnalyzer:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = yf.download(ticker, start, end)

    def add_ema(self, window):
        self.data[f'EMA_{window}'] = self.data['Adj Close'].ewm(span=window).mean()

    def add_rsi(self, window):
        delta = self.data['Adj Close'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        avg_gain = up.rolling(window=window).mean()
        avg_loss = abs(down.rolling(window=window).mean())
        rs = avg_gain / avg_loss
        self.data[f'RSI_{window}'] = 100 - (100 / (1 + rs))

    def add_macd(self, short_window, long_window):
        exp1 = self.data['Adj Close'].ewm(span=short_window, adjust=False).mean()
        exp2 = self.data['Adj Close'].ewm(span=long_window, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        self.data['MACD'] = macd
        self.data['Signal Line'] = signal
        
    

    def analyze(self):
        self.add_ema(10)
        self.add_rsi(14)
        self.add_macd(12, 26)

        fig, axs = plt.subplots(3, sharex=True, figsize=(13,9))
        fig.suptitle('Stock analysis: ' + self.ticker)
        cursor = Cursor(axs[0], useblit=True, color='red', linewidth=1)

        axs[0].plot(self.data.index, self.data['Adj Close'], label='Adj Close')
        axs[0].plot(self.data.index, self.data['EMA_10'], label='10-Day EMA')
        axs[0].set_ylabel('Price (USD)')
        axs[0].legend()

        cmap = plt.get_cmap("RdYlGn_r")  # Get the colormap
        color = cmap(self.data['RSI_14'] / 100)  # Normalize the RSI to the colormap
        axs[1].fill_between(self.data.index, self.data['RSI_14'], color=color)
        axs[1].axhline(0, linestyle='--', alpha=0.1)
        axs[1].axhline(20, linestyle='--', alpha=0.5)
        axs[1].axhline(30, linestyle='--')
        axs[1].axhline(70, linestyle='--')
        axs[1].axhline(80, linestyle='--', alpha=0.5)
        axs[1].axhline(100, linestyle='--', alpha=0.1)
        axs[1].set_ylabel('RSI')
        
        
        axs[2].plot(self.data.index, self.data['MACD'], label='MACD')
        axs[2].plot(self.data.index, self.data['Signal Line'], label='Signal Line')
        axs[2].axhline(0, linestyle='--', alpha=0.1)
        axs[2].set_ylabel('MACD')
        axs[2].set_xlim(left=min(self.data.index), right=max(self.data.index))
        axs[2].legend()

        return fig



class StockApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Analyzer")
        self.geometry("800x600")
        self.create_widgets()
        self.canvas = None

    def create_widgets(self):
        self.label = ttk.Label(self, text="Enter company")
        self.label.pack(side="top")
        
        self.ticker_combobox = ttk.Combobox(self, values=list(EURO_STOCK_50.keys()))
        self.ticker_combobox.pack(side="top")
        self.start_label = ttk.Label(self, text="Start date")
        self.start_label.pack(side="top")
        self.start_entry = DateEntry(self)
        self.start_entry.pack(side="top")

        self.end_label = ttk.Label(self, text="End date")
        self.end_label.pack(side="top")
        self.end_entry = DateEntry(self)
        self.end_entry.pack(side="top")

        self.button = ttk.Button(self, text="Analyze", command=self.analyze)
        self.button.pack(side="top")

        self.save_button = ttk.Button(self, text="Save as PDF", command=self.save_as_pdf)
        self.save_button.pack(side="top")
        
        self.quit_button = ttk.Button(self, text="Quit", command=self.destroy)
        self.quit_button.pack(side="top")



    def format_date(self, date_str):
        
        return datetime.datetime.strptime(date_str, '%m/%d/%y').strftime('%Y-%m-%d')


    def analyze(self):
        ticker = self.ticker_combobox.get()
        start_date = self.format_date(self.start_entry.get())
        end_date = self.format_date(self.end_entry.get())
        
        # Convert the company name to the corresponding ticker symbol
        ticker_symbol = EURO_STOCK_50.get(ticker, ticker)

        analyzer = StockAnalyzer(ticker_symbol, start_date, end_date)
        fig = analyzer.analyze()

        # If a figure was previously drawn, remove it
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Draw the new figure
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def save_as_pdf(self):
        if self.canvas:
            self.canvas.figure.savefig("output.pdf")

if __name__ == "__main__":
    app = StockApplication()
    app.mainloop()
