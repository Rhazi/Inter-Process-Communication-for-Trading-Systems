import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

data = pd.read_csv("./logs/latency_metrics.csv")

sample = data.sample(300, random_state=0)   # keep only 300 points
"""
plt.figure(figsize=(4, 6))

sns.boxplot(y=sample, width=0.25, color="white", fliersize=0)
sns.stripplot(y=sample, jitter=True, size=4, color="black", alpha=0.7)

# Zoom in to the tight region
plt.ylim(np.percentile(sample, 1), np.percentile(sample, 99))
plt.grid(axis='y', alpha=0.2)

plt.show()
"""
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Your latency Series, e.g.:
# latencies = df["processing_latency_ms"]
latencies = data["decision_latency_ms"].dropna()
latencies = latencies.sample(300, random_state=0)   # keep only 300 points


mean_latency = latencies.mean()

plt.figure(figsize=(12, 6))
sns.histplot(latencies, bins=40, kde=False, color="teal", alpha=0.6)

# Mean line
plt.axvline(mean_latency, color="red", linestyle="--", linewidth=2)
plt.text(mean_latency + 0.02,      # shift slightly to the right
         plt.ylim()[1] * 0.9,       # 90% up the y-axis
         f"Mean: {mean_latency:.2f} ms",
         color="red", fontsize=12)

# Labels & title
plt.title("Processing Latency Distribution", fontsize=16)
plt.xlabel("Latency (ms)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)

plt.grid(axis='y', alpha=0.2)
plt.xlim(np.percentile(latencies, 1), np.percentile(latencies, 99))
plt.show()

"""

import matplotlib.pyplot as plt
import seaborn as sns

#sample = data.sample(300, random_state=0)   # keep only 300 points
sample = data.iloc[1:300]
lat = sample["processing_latency_ms"].dropna()
ticks = sample["tick_id"]  # or df["tick_id"]

plt.figure(figsize=(12, 6))

plt.plot(ticks, lat, color="teal", alpha=0.35, linewidth=2)

plt.title("Processing Latency Over Time", fontsize=16)
plt.xlabel("Tick ID", fontsize=14)
plt.ylabel("Latency (ms)", fontsize=14)

plt.grid(alpha=0.25)
plt.tight_layout()

plt.show()