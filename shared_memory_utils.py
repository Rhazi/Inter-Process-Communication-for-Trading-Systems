import time
from datetime import datetime
import os
import csv
from multiprocessing import shared_memory
import psutil


def log_to_csv(filename: str, data: dict):
    #CSV logging function
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    filepath = os.path.join(log_dir, filename)
    file_exists = os.path.exists(filepath)

    with open(filepath, 'a', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def get_shared_memory_size(name:str):
    try:
        shm = shared_memory.SharedMemory(name=name)
        size = shm.size
        shm.close()
        return size
    except:
        return 0

def get_memory_footprint_mb(name:str):
    #get shared memory footprint in mb
    size_bytes = get_shared_memory_size(name)
    return size_bytes/(1024*1024)

def get_process_memory_mb():
    #get current process memory usage in mb
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024*1024)


def log_throughput(component: str, news_tps: float):
    #log throughput metrics to csv
    timestamp = time.time()
    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'timestamp': timestamp,
        'datetime': datetime_str,
        'component': component,
        'news_ticks_per_sec': news_tps,
    }

    log_to_csv('throughput_news_metrics.csv', data)


def log_memory_usage(component:str, shared_memory_name:str = ""):
    #log memory usage to csv
    timestamp = time.time()
    datetimestr = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    shared_mb = get_memory_footprint_mb(shared_memory_name) if shared_memory_name else 0
    process_mb = get_process_memory_mb()

    data = {
        "timestamp": timestamp,
        "datetime": datetimestr,
        "component": component,
        "shared_mb": shared_mb,
        "process_mb": process_mb,
        "shared_memory_name": shared_memory_name
    }

    log_to_csv("memory_usage.csv", data)


def log_latency(component:str, tick_id:int, processing_latency:float, decision_latency:float, symbol:str = ""):
    #logs latency metrics to csv
    timestamp = time.time()
    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    data = {
        "timestamp": timestamp,
        "datetime": datetime_str,
        "component": component,
        "tick_id": tick_id,
        "processing_latency_ms": processing_latency * 1000,
        "decision_latency_ms": decision_latency * 1000,
    }

    log_to_csv("latency_metrics.csv", data)
