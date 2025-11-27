import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

data = pd.read_csv("./logs/latency_metrics.csv")

processing_latency = data["decision_latency_ms"]

sample = processing_latency.sample(300, random_state=0)   # keep only 300 points

plt.figure(figsize=(4, 6))

sns.boxplot(y=sample, width=0.25, color="white", fliersize=0)
sns.stripplot(y=sample, jitter=True, size=4, color="black", alpha=0.7)

# Zoom in to the tight region
plt.ylim(np.percentile(sample, 1), np.percentile(sample, 99))
plt.grid(axis='y', alpha=0.2)

plt.show()