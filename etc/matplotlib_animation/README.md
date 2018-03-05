## skeleton code of animation

All animation of time development models have to follow this format for now.

```python
fig = plt.figure()
ax = plt.axes()

# initialization and make artists
artist = make_artist()

def update(frame):
    # update and return artists of figure
    return artist,

anim = animation.FuncAnimation(fig, update, interval=200, blit=True)
plt.show(anim)
```
