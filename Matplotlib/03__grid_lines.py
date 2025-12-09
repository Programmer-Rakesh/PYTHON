import matplotlib.pyplot as plt
import numpy as np

# grid() = helps make plots easier to read by adding refernce lines.

x = [1, 2, 3, 4, 5]
y = [5, 10, 15, 20, 25] 

plt.grid()

#or
#plt.grid(axis='x')

plt.plot(x, y)
plt.show()