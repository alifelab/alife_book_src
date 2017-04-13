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

# initialization and make artists
artist = make_artist()

def update(frame):
    # update and return artists of figure
    return artist,

anim = animation.FuncAnimation(fig, update, interval=200, blit=True)
plt.show(anim)
```

## References

### Chapter3

John E. Pearson (1993) "Complex Patterns in a Simple System" Science 261(5118):189-192.

http://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/
