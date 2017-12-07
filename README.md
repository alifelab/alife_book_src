# alife_book_src

## development environment

**anaconda3-5.0.0 is recommended.**

- python 3.5.1
- numpy 1.12.1
- matplotlib 2.0.0


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

## ソースコード解説, References

各Chapter内のREADMEに移動
