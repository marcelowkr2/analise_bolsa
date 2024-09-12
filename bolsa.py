import tkinter as tk
from tkinter import ttk
import yfinance as yf
import ta
import time
import alpaca_trade_api as tradeapi

# Configurações da API Alpaca (note que ela não é compatível com ações brasileiras)
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
APCA_API_KEY_ID = "PK1BYFC3Q6IH2LQ4OL9Y"
APCA_API_SECRET_KEY = "r4sx1IIt0NJn2YJypCcICOPu8fwfemCxRdWrirVW"

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

positions = {}
running = False

class TradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Trading Automático")

        # Configurações de Interface
        self.ticker_label = ttk.Label(root, text="Ticker:")
        self.ticker_label.grid(row=0, column=0, padx=5, pady=5)
        self.ticker_entry = ttk.Entry(root)
        self.ticker_entry.grid(row=0, column=1, padx=5, pady=5)

        self.quantity_label = ttk.Label(root, text="Quantidade:")
        self.quantity_label.grid(row=1, column=0, padx=5, pady=5)
        self.quantity = tk.IntVar(value=10)
        self.quantity_entry = ttk.Entry(root, textvariable=self.quantity)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        self.stop_loss_pct = tk.DoubleVar(value=1.0)
        self.take_profit_pct = tk.DoubleVar(value=1.0)

        # Configurações de Stop Loss e Take Profit
        config_frame = ttk.LabelFrame(root, text="Configurações de Trading")
        config_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Label(config_frame, text="Stop Loss %:").grid(row=2, column=0, padx=5, pady=5)
        self.stop_loss_slider = ttk.Scale(config_frame, from_=0, to=10, orient="horizontal", variable=self.stop_loss_pct)
        self.stop_loss_slider.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(config_frame, text="Take Profit %:").grid(row=3, column=0, padx=5, pady=5)
        self.take_profit_slider = ttk.Scale(config_frame, from_=0, to=10, orient="horizontal", variable=self.take_profit_pct)
        self.take_profit_slider.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Indicadores Técnicos
        self.rsi_check = tk.BooleanVar(value=True)
        self.macd_check = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Usar RSI", variable=self.rsi_check).grid(row=4, column=0, padx=5, pady=5)
        ttk.Checkbutton(config_frame, text="Usar MACD", variable=self.macd_check).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Painel de Indicadores
        self.indicator_frame = ttk.LabelFrame(root, text="Indicadores Técnicos")
        self.indicator_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.sma_label = ttk.Label(self.indicator_frame, text="SMA 20:")
        self.sma_label.grid(row=0, column=0, padx=5, pady=5)
        self.sma_value = ttk.Label(self.indicator_frame, text="--")
        self.sma_value.grid(row=0, column=1, padx=5, pady=5)

        self.rsi_label = ttk.Label(self.indicator_frame, text="RSI:")
        self.rsi_label.grid(row=1, column=0, padx=5, pady=5)
        self.rsi_value = ttk.Label(self.indicator_frame, text="--")
        self.rsi_value.grid(row=1, column=1, padx=5, pady=5)

        self.macd_label = ttk.Label(self.indicator_frame, text="MACD:")
        self.macd_label.grid(row=2, column=0, padx=5, pady=5)
        self.macd_value = ttk.Label(self.indicator_frame, text="--")
        self.macd_value.grid(row=2, column=1, padx=5, pady=5)

        self.signal_label = ttk.Label(self.indicator_frame, text="Signal:")
        self.signal_label.grid(row=3, column=0, padx=5, pady=5)
        self.signal_value = ttk.Label(self.indicator_frame, text="--")
        self.signal_value.grid(row=3, column=1, padx=5, pady=5)

        # Botões de Controle
        self.start_button = ttk.Button(root, text="Iniciar Trading", command=self.start_trading)
        self.start_button.grid(row=6, column=0, padx=5, pady=5)
        self.stop_button = ttk.Button(root, text="Parar Trading", command=self.stop_trading, state="disabled")
        self.stop_button.grid(row=6, column=1, padx=5, pady=5)

        # Área de Logs
        self.log_text = tk.Text(root, height=10, width=50)
        self.log_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

    def start_trading(self):
        global running
        running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.update_data()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log_message(f"Trading iniciado em {timestamp}.")

    def stop_trading(self):
        global running
        running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log_message(f"Trading parado em {timestamp}.")

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def update_data(self):
        if running:
            trading_loop()
            self.root.after(60000, self.update_data)

    def update_indicators(self, sma, rsi, macd, signal):
        self.sma_value.config(text=f"{sma:.2f}")
        self.rsi_value.config(text=f"{rsi:.2f}")
        self.macd_value.config(text=f"{macd:.2f}")
        self.signal_value.config(text=f"{signal:.2f}")

def reconnect_api():
    global api
    try:
        api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
        print("Reconectado à API Alpaca com sucesso.")
    except Exception as e:
        print(f"Falha ao reconectar à API: {e}")

def obter_dados(ticker):
    try:
        dados = yf.download(ticker, period="1d", interval="1m")
        return dados
    except Exception as e:
        print(f"Erro ao obter dados de {ticker}: {e}")
        return None

def executar_ordem(ticker, quantidade, tipo_ordem, price):
    try:
        if tipo_ordem == "COMPRA":
            api.submit_order(
                symbol=ticker,
                qty=quantidade,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"Ordem de compra enviada: {quantidade} de {ticker} a preço de mercado.")
        elif tipo_ordem.startswith("VENDA"):
            api.submit_order(
                symbol=ticker,
                qty=quantidade,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"Ordem de venda enviada: {quantidade} de {ticker} a preço de mercado.")
    except Exception as e:
        print(f"Erro ao executar ordem para {ticker}: {e}")
        reconnect_api()

def analisar_e_investir(ticker):
    dados = obter_dados(ticker)
    if dados is None or dados.empty:
        print(f"Dados insuficientes para {ticker}. Pulando...")
        return

    # Cálculo de indicadores
    dados['SMA_20'] = ta.trend.sma_indicator(dados['Close'], window=20)
    dados['RSI'] = ta.momentum.rsi(dados['Close'], window=14)
    dados['MACD'] = ta.trend.macd(dados['Close'])
    dados['Signal'] = ta.trend.macd_signal(dados['Close'])

    preco_atual = dados['Close'].iloc[-1]
    sma_20 = dados['SMA_20'].iloc[-1]
    rsi = dados['RSI'].iloc[-1]
    macd = dados['MACD'].iloc[-1]
    signal = dados['Signal'].iloc[-1]

    stop_loss_pct = app.stop_loss_pct.get()
    take_profit_pct = app.take_profit_pct.get()

    stop_loss = preco_atual * (1 - stop_loss_pct / 100)
    take_profit = preco_atual * (1 + take_profit_pct / 100)

    # Atualizar painel de indicadores
    app.update_indicators(sma_20, rsi, macd, signal)

    # Condições de compra
    if preco_atual > sma_20 and rsi < 70 and macd > signal:
        print(f"Sinal de compra para {ticker}. Preço: {preco_atual}, SMA_20: {sma_20}, RSI: {rsi}, MACD: {macd}")
        executar_ordem(ticker, quantidade=app.quantity.get(), tipo_ordem="COMPRA", price=preco_atual)
        positions[ticker] = {'quantity': app.quantity.get(), 'stop_loss': stop_loss, 'take_profit': take_profit}

    # Condições de venda
    elif preco_atual < sma_20 or rsi > 70 or macd < signal:
        print(f"Sinal de venda para {ticker}. Preço: {preco_atual}, SMA_20: {sma_20}, RSI: {rsi}, MACD: {macd}")
        if ticker in positions:
            executar_ordem(ticker, quantidade=positions[ticker]['quantity'], tipo_ordem="VENDA (Condição)", price=preco_atual)
            del positions[ticker]

def trading_loop():
    try:
        tickers = app.ticker_entry.get().upper().split(',')
        for ticker in tickers:
            ticker = ticker.strip()
            analisar_e_investir(ticker)
    except Exception as e:
        print(f"Erro no loop de trading: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()
