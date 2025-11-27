import socket
from config import *
import threading
from collections import defaultdict
import pandas as pd
import time
from shared_memory_utils import log_throughput

clients = defaultdict() # stores clients
news_tick_count = 0
prev_news = 0

lock = threading.Lock()

def monitor_throughput(interval=5):
    global news_tick_count, prev_news

    while True:
        time.sleep(interval)
        with lock:
            delta_news = news_tick_count - prev_news
            prev_news = news_tick_count

        rate_news = delta_news / interval

        #log throughput to csv
        log_throughput("GATEWAY", rate_news)

        print(f"[THROUGHPUT] News ticks/sec: {rate_news}")

def get_sentiment_data():
    # Simulate news data from a data source
    data = pd.read_csv('./data/market_sentiment.csv')
    return data

def broadcast(msg:bytes, client_type:str):
    global news_tick_count

    if ClientType.STRATEGY.value == client_type:
        with lock:
            news_tick_count += 1

    with lock:
        targets = clients[client_type]
        for conn in targets:
            try:
                conn.sendall(msg)
            except Exception:
                print(f"Dropping disconnected client")
                clients.pop(client_type, None)


def feed_news_stream():
    global news_tick_count
    news_data = get_sentiment_data()

    for _, row in news_data.iterrows():
        sentiment = int(row["sentiment"])
        timestamp = row.get("timestamp", "")
        symbol = row["symbol"]
        feed_time = time.time()
        with lock:
            news_tick_count += 1

        message = f"{MessageType.NEWS_SENTIMENT.value}, {news_tick_count}, {timestamp}, {symbol}, {sentiment}, {feed_time}*".encode()

        #wait for a short time interval to simulate real-time feed
        time.sleep(0.01)

        #broadcast to all strategy clients
        broadcast(message, ClientType.STRATEGY.value)


def handle_client(conn, addr):
    print(f"connected:{addr}")
    buffer = b""
    client_type = None

    try:
        while True:
            data = conn.recv(BYTE_LIMIT)
            if not data:
                break
            buffer += data
            print(f"buffer: {buffer}")

            while MESSAGE_DELIMITER in buffer:
                msg, buffer = buffer.split(MESSAGE_DELIMITER, 1)
                msg_decoded = msg.decode()
                msg_type, client_type, client_id = msg_decoded.split(STRING_DELIMITER)

                if msg_type == MessageType.REGISTER.value:
                    with lock:
                        clients[client_type].append(conn)
                    print(f"Registered client: {client_type} : {client_id}")
    except Exception as e:
        print(f"connection error with {addr}:{e}")
    finally:
        if client_type and client_type in clients:
            with lock:
                del clients[client_type]
        conn.close()
        print(f"disconnected {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT_GATEWAY))
    server.listen()
    print(f"[SERVER] broadcasting on {SERVER_HOST}:{SERVER_PORT_GATEWAY}")

    #thread to handle news stream
    threading.Thread(target=feed_news_stream, daemon=True).start()

    # thread to monitor throughput
    threading.Thread(target=monitor_throughput, daemon=True).start()

    while True:
        conn, addr = server.accept()
        #thread to handle client
        threading.Thread(target=handle_client, args=(conn,addr), daemon=True).start()