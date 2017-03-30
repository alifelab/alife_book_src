# alife_book_src

## development environment

- python 3.5.1
- numpy 1.12.1
- matplotlib 2.0.0


## skeleton code of animation 

All animation of time development models have to follow this format for now.

```python
fig = plt.figure()
ax = plt.axes()

def update(frame):
    # update artists of figure
    return artist,

anim = animation.FuncAnimation(fig, update, interval, blit=True)
plt.show(anim)
```
