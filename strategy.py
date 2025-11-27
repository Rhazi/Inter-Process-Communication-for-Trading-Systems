import socket
from multiprocessing import shared_memory
import numpy as np
from config import *
import json
import time
from shared_memory_utils import log_memory_usage, log_latency
import threading

tick_id = 0
news_signals = []
latency_logs = []


class SharedNewsBook():
    def __init__(self, symbols, name=None, create=True):
        self.symbols = symbols
        self.size = len(symbols)
        if create:
            self.shm = shared_memory.SharedMemory(
                create=True, size=self.size*8, name=name
            )
        else:
            self.shm = shared_memory.SharedMemory(name=name)
        self.sentiments = np.ndarray((
            self.size,), dtype=np.float64, buffer=self.shm.buf
        )
        self.symbol_index = {s: i for i, s in enumerate(self.symbols)}

    def update(self, symbol, sentiment):
        idx = self.symbol_index[symbol]
        self.sentiments[idx] = sentiment

    def read(self, symbol):
        idx = self.symbol_index[symbol]
        return self.sentiments[idx]


class NewsSentimentStrategy():
    def __init__(self, news_book:SharedNewsBook, symbol:str):
        self.news_book = news_book
        self.symbol = symbol

    def generate_signal(self):
        sentiment = self.news_book.read(self.symbol)
        if sentiment > 50:
            return {"symbol": self.symbol, "sentiment":sentiment, "signal":"BUY"}


def start_news_strategy(symbol=" AAPL"):
    global tick_id
    global news_signals

    news_signals.clear()

    #connect to gateway
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )
    print("[STRATEGY] Trying to connect to gateway...")
    client.connect((SERVER_HOST, SERVER_PORT_GATEWAY))
    print("[STRATEGY] Connected to gateway")
    client.sendall((b"REGISTER,STRATEGY,1*"))
    counter = 0

    #connect to order_manager
    manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[STRATEGY] Trying to connect to Order Manager...")
    manager.connect((MANAGER_HOST, MANAGER_PORT))
    print("[STRATEGY] connected to Order Manager")

    symbols = [" AAPL", " SPY", " MSFT"]
    shared_news_book = SharedNewsBook(symbols ,name="Shared_news_book")
    news_strategy = NewsSentimentStrategy(shared_news_book, symbol)

    while True:
        data = client.recv(BYTE_LIMIT)
        if not data:
            break

        output = data.decode().split("*")

        for msg in output:
            if not msg:
                continue
            fields = msg.split(STRING_DELIMITER)
            tick_id += 1
            try:
                ts_sent = float(fields[-1])
            except ValueError:
                print(f"[WARN] Invalid timestamp field {fields[-1]} from {msg}")
            ts_rcvd = time.time()
            latency = ts_rcvd - ts_sent
            latency_logs.append(latency)

            #update news object
            if fields[0] == "NEWS_SENTIMENT":
                news_symbol = fields[3]
                sentiment = float(fields[4])
                shared_news_book.update(news_symbol, sentiment)

            trade_time = time.time()
            news_signal = news_strategy.generate_signal()

            if news_signal:
                print(f"[NEWS STRAT] {news_signal}")
                news_signals.append(news_signal)
                client.sendall((json.dumps(news_signal) + "*").encode())

            #counter += 1

        trade_time = time.time()
        decision_latency = trade_time - ts_sent

        #Log performance metrics to CSV
        log_latency("NEWS_STRATEGY", tick_id, latency, decision_latency, symbol)

        #log memory usage every 50 ticks
        if tick_id % 50 == 0:
            log_memory_usage("NEWS_STRATEGY", "Shared_news_book")

        print(f"[NEWS STRATEGY] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")

    client.close()