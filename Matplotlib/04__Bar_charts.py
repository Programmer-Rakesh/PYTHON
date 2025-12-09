import matplotlib.pyplot as plt
import numpy as np

# Bar chart = compare categories of data by representing each categotry with a bar

categories = np.array(["apple", "banana", "onion", "grapes"])
values = np.array([3, 5, 6, 7])

plt.bar(categories, values)

plt.show()