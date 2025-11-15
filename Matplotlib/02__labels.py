import matplotlib.pyplot as plt
import numpy as np

x = np.array([2023, 2024, 2025, 2026])
y1 = np.array([15, 25, 30, 20])
y2 = np.array([17, 23, 38, 5])
y3 = np.array([13, 15, 20, 30])

plt.title("class size", fontsize=20,
                        color="blue",
                        family='Arial',
                        fontweight="bold")

plt.xlabel("Year", fontsize=20,
                    family="Arial",
                    fontweight="bold")

plt.ylabel("Students", fontsize=20,
                    family="Arial",
                    fontweight="bold")

plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)

plt.xticks(x)

plt.show()