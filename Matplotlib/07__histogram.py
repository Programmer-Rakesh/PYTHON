import matplotlib.pyplot as plt
import numpy as np

scores = np.random.normal(loc=80, scale=50, size=100)
# scores = np.clip(scores, 0, 100)

plt.hist(scores)
plt.hist(scores, color='lightgreen',
                    edgecolor='black')

plt.show()