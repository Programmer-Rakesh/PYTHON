import matplotlib.pyplot as plt
import numpy as np

categories = np.array(["apple", "banana", "onion", "grapes"])
values = np.array([3, 5, 6, 7])

plt.pie(values, labels=categories,
        autopct='%1.1f%%',
        explode=[0, 0, 0.2, 0],
        shadow=True)

plt.show()