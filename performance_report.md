# Performance Report - Assignment 8

## Executive Summary

Overview of trading system performance for AAPL, SPY, and MSFT with focus on latency, throughput, and memory metrics. Without loss of generality, comparison is on a 300 tick sample. 

---

## 1. Latency Analysis


### Latency

![process latency](img/process_latency.jpg)
![decision latency](img/decision_latency.jpg)


Processing and decision latency across AAPL, SPY, and MSFT.

* No significant difference between batches of symbols.


### AAPL Latency Performance

![process Latency distribution](img/process_latency_dist.png)
![decision latency distribution](img/decision_latency_dist.png)

* Mean Processing Latency and Mean Decision Latency are very similar with mean of 12.35ms. Given that most of the latency is clustered around this mean, there seem to be no systematic issue in the process.


![process latency Over Time](img/process_latency_time.png)
![decision latency Over Time](img/decision_latency_t.png)

* No pattern has been found on latency over time. This further confirms delay is not affected by running time of the system. 

---

## 2. Throughput Analysis

![Throughput Metrics](img/Throughput.png)

Mean Througput of price information and that of News information are roughly the same at 157.3 Ticks/second.

---

## 3. Memory Usage

### Shared Memory

![Shared Memory Usage](img/memusage.png)

**Why is Shared Memory Constant at 0.015625 MB (16 KB)?**

Shared memory is pre-allocated with fixed size for predictable performance:
- Fixed-size memory-mapped files for deterministic behavior
- Virtual address space reservation (not physical memory)
- Shared across all components for efficient IPC
- No dynamic growth to prevent fragmentation

### Process Memory

* Orderbook class is continuously consuming the highest memory. This is expected as orderbook
1. is influenced by server connection overhead
2. contains huge data parsing logic for each input msg
3. logs more frequently to keep tick level data

* Price strategy shows more data consumption than News strategy because
1. Prices strategy keeps historical data information for moving average calculation.


