# Week 3 - Parts 4 and 5

I had very little to write about this week - I followed the tutorial steps more or less exactly, and didn't make any notable additions or changes. Instead I'll talk about something I learned along the way, and hopefully others might find it helpful to understand the tutorial code better.

The tutorial makes frequent use of `ndarray` containers for the game map, but if (like me) you haven't encountered these before, some of the syntax can be a bit confusing! Consider this function:

```python
def update_fov(self) -> None:
    """Recompute the visible area based on the player's point of view."""
    self.game_map.visible[:] = compute_fov(
        self.game_map.tiles["transparent"],
        (self.player.x, self.player.y),
        radius = 8
    )
    # If a tile is "visible" it should be added to "explored".
    self.game_map.explored |= self.game_map.visible
```

What the heck is `self.game_map.tiles["transparent"]`? Is that indexing with a *string?*

The [NumPy documentation](https://numpy.org/doc/stable/reference/arrays.ndarray.html) for `ndarray` came to my rescue here, specifically the section on [field access](https://numpy.org/doc/stable/user/basics.indexing.html#field-access). It turns out that yes, it is indeed indexing on a string - the name of a field from the array's data type. The returned value is a view of the original array that only contains that specific field from each element. That's pretty neat! Rather than iterating an array of tiles and query for the value of `transparent` in each one, `compute_fov` can iterate an array of those boolean values directly!

I was also unfamiliar with Python's [slicing syntax](https://docs.python.org/3/reference/expressions.html#slicings), and the [`np.select` function](https://numpy.org/doc/stable/reference/generated/numpy.select.html) defied my understanding for a while too. If you find yourself in the same boat, I highly recommend reading up on those!
