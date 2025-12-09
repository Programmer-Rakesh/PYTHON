import matplotlib.pyplot as plt
import numpy as np

# scatter graph = shows the relationship btwn two variables
#                 Helps to identify a correlation (+, -, None)
#                 Example: Study hours vs. Test scores

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 7, 8])
y = np.array([55, 60, 65, 70, 72, 75, 78, 80, 85, 87])

x1 = np.array([0, 1, 2, 3, 4, 5, 3, 7, 7, 9])
y1 = np.array([55, 60, 68, 73, 72, 75, 50, 80, 80, 97])


plt.scatter(x, y, color='blue',
            label='Class A')
plt.scatter(x1, y1, color='red',
            label='Class B')

plt.legend()
plt.show()