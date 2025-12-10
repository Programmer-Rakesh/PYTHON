<<<<<<< HEAD
=======
##ploted for college work!

>>>>>>> db51aaf8300d24d7f8061f746ce5732746ca5880
import matplotlib.pyplot as plt
import numpy as np

x = np.array([0.28, 0.44, 0.48, 0.52, 0.54, 0.56, 0.57, 0.58, 0.59, 0.60])
y = np.array([0.00, 0.02, 0.06, 0.17, 0.23, 0.36, 0.45, 0.45, 0.55, 0.70])

x1 = np.array([0, 5.04, 10.03, 12.07, 15.03, 18.01, 20.0, 20.0, 24.9, 29.9])
y1 = np.array([0.0, 0.5, 1.0, 1.2, 1.5, 1.8, 2.0, 2.2, 2.5, 3.0])

plt.title("class size", fontsize=20,
                        color="blue",
                        family='Arial',
                        fontweight="bold")

plt.xlabel("VF", fontsize=20,
                    family="Arial",
                    fontweight="bold")

plt.ylabel("IF", fontsize=20,
                    family="Arial",
                    fontweight="bold")

<<<<<<< HEAD
=======




>>>>>>> db51aaf8300d24d7f8061f746ce5732746ca5880
plt.plot(x, y)
plt.plot(x1, y1)

plt.xticks(x)

plt.show()