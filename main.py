from multiprocessing import Process
from time import sleep
import signal
import sys
from gateway import start_server
from order_manager import start_ordermanager
from strategy import start_news_strategy

def run_gateway():
    print("[GATEWAY] Starting feed server...")
    start_server()

def run_ordermanager():
    print("[ORDER MANAGER]  order manager...")
    start_ordermanager()

def run_news_strategy():
    sleep(2)
    print("[STRATEGY] Starting news strategy...")
    start_news_strategy()

if __name__ == "__main__":
    print("[MAIN] Starting Trading System with Performance Logging...")
    print("[MAIN] Performance data will be logged to CSV files in logs/directory")

    processes = [
        Process(target=run_gateway),
        Process(target=run_ordermanager),
        Process(target=run_news_strategy),
    ]

    for p in processes: p.start()

    try:
        for p in processes: p.join()
    except KeyboardInterrupt:
        print('[MAIN] Terminating processes...')
        for p in processes:
            p.terminate()
        print('[MAIN] Performance logs saved to logs/directory')
        print('[MAIN] All processes terminated')