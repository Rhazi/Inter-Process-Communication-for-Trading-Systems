import socket
from config import *
import threading
import json


def log_trade(order, addr):
    #deserializes order and logs trade
    if "sentiment" in order:
        value = order["sentiment"]
    elif "price" in order:
        value = order["price"]

    symbol = order['symbol']
    signal = order['signal']

    confirmation = print(f"RECEIVED ORDER FROM {addr}: {1} {symbol} {signal} signal at {value}")
    print(confirmation)

    with open(LOG_FILE, "a") as f:
        f.write(confirmation + "\n")


def handle_client(conn, addr):
    print(f"Connected {addr}")
    buffer = b""

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            buffer += data
            print("buffer:", buffer)

            while MESSAGE_DELIMITER in buffer:
                msg, buffer = buffer.split(MESSAGE_DELIMITER, 1)
                order = json.loads(msg.decode())
                log_trade(order, addr)

    except Exception as e:
        print(f"Connection error with {addr} : {e}")
    finally:
        print(f"Disconnected {addr}")

def start_ordermanager():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    server.bind((MANAGER_HOST, MANAGER_PORT))
    server.listen()
    print(f"[ORDER MANAGER] broadcasting on {MANAGER_HOST}:{MANAGER_PORT}")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()


if __name__ == "main":
    start_ordermanager()