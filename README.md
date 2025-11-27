##Inter-Process Communication for Trading Systems

## Overview
The project is a simplified multi-process trading system that uses interprocess communication (IPC) to connect independent components through real TCP sockets and shared memory.
The focus is on building a mini trading stack — a Gateway, Strategy, and OrderManager — that communicate in real time emphasizing process orchestration, socket programming, serialization, and shared memory synchronization in the context of financial systems.
## Setup Instructions

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd Inter-Process-Communication-for-Trading-Systems/
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install socket pytest numpy"
   ```

3. **Verify installation**:
   ```bash
   python -c "import socket, pandas, numpy; print('All dependencies installed successfully')"
   ```

4. **Run the main application**:
   ```bash
   python main.py
   ```

## Architecture

**-Gateway streams price and sentiment data to all subscribed clients.**
<br />**-Strategy reads from shared memory, generates buy/sell signals, and sends serialized JSON orders via TCP to the OrderManager.**
<br />**-OrderManager receives orders, logs them to file, and confirms receipt.**

### Core Modules

#### `gateway.py`
**-Reads price and sentiment CSVs.**
<br />**-Broadcasts encoded tick messages over TCP.**
<br />**-Tracks throughput in ticks/seconds**
<br />**-Each client registers via a simple handshake message.**

#### `strategy.py`
-**Connects to the Gateway to receive live sentiment.**
<br />-**Reads live prices from shared memory.**
<br />-**Generates signals (e.g. sentiment trigger).**
<br />-**Immediately sends JSON orders to the OrderManager**

#### `order_manager.py`
**-Listens for strategy connections via TCP.**
<br />**-Receives JSON orders, logs them, and can optionally send acknowledgements.**
<br />**-Maintains order_log.txt with timestamps and signal details.**

#### `shared_memory_utils.py`
-Defines reusable shared memory structures:
<br />   **SharedNewsBook**
<br />-Backed by multiprocessing.shared_memory and numpy.ndarray for fast numerical sharing.

### How to Run

#### Environment
```bash
python3 -m venv venv
<br />source venv/bin/activate
<br />pip install -r requirements.txt
```


### Start the full system
Run the orchestrator:
```bash
python main.py
```

This will launch all core processes:
<br />**-Gateway**
<br />**-OrderManager**
<br />**-Strategy (News)**
And each process will print specific logs.


### Performance Metrics
Key metrics recorded in performance_report.md:
<br />**-Average tick rate (price + sentiment): ~500 ticks/sec.**
<br />**-Shared memory write/read latency: < 0.1 ms.**
<br />**-OrderManager round-trip acknowledgment: < 1 ms.**
<br />**-CPU / memory footprint under 100 MB for all processes.**


### Key features
**-Inter-Process Communication (IPC)**
<br />**-TCP socket programming)**
<br />**-Serialization / deserialization (JSON))**
<br />**-Shared memory via multiprocessing.shared_memory)**
<br />**-Process synchronization and orchestration)**
<br />**-Low-latency trading infrastructure simulation)**

### Future Extensions
**-Replace TCP sockets with ZeroMQ or gRPC for scalability.**
<br />**-Add pandas/Polars analytics layer for performance dashboards.**
<br />**-Implement asynchronous I/O with asyncio for non-blocking strategies.**
<br />**-Expand to include risk management and execution simulation modules.**

## Author
- Mohammed Rhazi - University of Chicago (mrhazi@uchicago.edu)

---

For detailed implementation examples and advanced usage patterns, refer to the source code documentation and the generated performance reports.




