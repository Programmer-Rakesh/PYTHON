import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# LEG PARAMETERS (mm)
# -------------------------
L1 = 120   # upper leg (femur)
L2 = 100   # lower leg (tibia)

# starting foot position
x = 80
y = -120

# -------------------------
# INVERSE KINEMATICS
# -------------------------
def inverse_kinematics(x, y, L1, L2):
    r = np.sqrt(x**2 + y**2)

    if r > (L1 + L2) or r < abs(L1 - L2):
        return None, None

    theta2 = np.arccos((r**2 - L1**2 - L2**2) / (2 * L1 * L2))
    theta1 = np.arctan2(y, x) - np.arccos((r**2 + L1**2 - L2**2) / (2 * r * L1))

    return theta1, theta2

# -------------------------
# FORWARD KINEMATICS
# -------------------------
def forward_kinematics(theta1, theta2, L1, L2):
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)

    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)

    return (x1, y1), (x2, y2)

# -------------------------
# PLOT SETUP
# -------------------------
fig, ax = plt.subplots()
ax.set_xlim(-250, 250)
ax.set_ylim(-250, 50)
ax.set_aspect('equal')
ax.grid()

line1, = ax.plot([], [], 'r-o', linewidth=3)
line2, = ax.plot([], [], 'g-o', linewidth=3)
target = ax.scatter([], [], c='blue')

# -------------------------
# UPDATE FUNCTION (KEYBOARD)
# -------------------------
def update(event):
    global x, y
    step = 5

    if event.key == 'up':
        y += step
    elif event.key == 'down':
        y -= step
    elif event.key == 'left':
        x -= step
    elif event.key == 'right':
        x += step

    theta1, theta2 = inverse_kinematics(x, y, L1, L2)
    if theta1 is None:
        return

    (jx, jy), (fx, fy) = forward_kinematics(theta1, theta2, L1, L2)

    line1.set_data([0, jx], [0, jy])
    line2.set_data([jx, fx], [jy, fy])
    target.set_offsets([x, y])

    fig.canvas.draw_idle()

fig.canvas.mpl_connect('key_press_event', update)

# -------------------------
# INITIAL DRAW
# -------------------------
theta1, theta2 = inverse_kinematics(x, y, L1, L2)
(jx, jy), (fx, fy) = forward_kinematics(theta1, theta2, L1, L2)

line1.set_data([0, jx], [0, jy])
line2.set_data([jx, fx], [jy, fy])
target.set_offsets([x, y])

plt.show()
