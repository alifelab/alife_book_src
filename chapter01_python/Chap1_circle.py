import matplotlib.pyplot as plt


ax = plt.axes(xlim=(0, 10), ylim=(0, 10), aspect='equal')
circle = plt.Circle((5, 5), 0.75)
ax.add_patch(circle)

plt.show()
