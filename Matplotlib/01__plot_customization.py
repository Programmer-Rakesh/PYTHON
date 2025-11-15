import matplotlib.pyplot as plt
import numpy as np

x = np.array([2023, 2024, 2025, 2026])
y = np.array([15, 25, 1500, 20])
y2 = np.array([1005, 25, 3000, 20])

plt.plot(x, y, marker='o', 
                markersize=10,
                markerfacecolor="cyan",
                markeredgecolor="blue",
                # linestyle='line',
                linewidth=4)

plt.plot(x, y2, marker='o', 
                markersize=10,
                markerfacecolor="red",
                markeredgecolor="green",
                # linestyle='dotted',
                linewidth=4)

plt.show()