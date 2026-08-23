# Week 2 - Parts 2 and 3

I ended up being quite busy this week, and this devlog was written during the following week, so I'm going to keep it brief.

## Part 2

I realised that some of the code refactoring described in this part of the tutorial would conflict with the high DPI support I added last week. At first I tried to move my code to `Engine` or `EventHandler`, but I had no luck with either since they don't have access to the `context` object when handling events. For a while I considered pursuing this solution further by calculating and storing the size in `Engine` when the event is handled, and then updating `context` in `render`. However, I had a peek at the final code repo and saw that event iteration is moved back to `main.py` later. With this in mind, I decided to pre-emptively move this code back to 'main.py' early, thus allowing high DPI support to be handled much the same as it was, and `Engine` now handles a single event at a time.

Another minor thing I noticed in this part is that the `graphic_dt` data type seems redundant when `tcod.console.rgb_graphic` exists. I added a TODO comment to remind myself to look into this later.

## Part 3

I didn't particularly like the layouts that were being created with the procedural generation provided by the tutorial, and the method of placing rooms left something to be desired for me as well. It would technically be possible (though incredibly unlikely) for a "dungeon" to be generated with only a single room! I decided to research and implement a different solution - binary space partitioning. I'd previously heard about BSP and its use in roguelike dungeon generation, and thankfully python-tcod provides the `tcod.bsp` module to handle the boilerplate of creating and traversing a BSP tree.

I created a new `procgen_bsp.py` file so I could develop my solution as a toggleable alternative while leaving the original `procgen.py` file intact. The [documentation](https://python-tcod.readthedocs.io/en/latest/tcod/bsp.html) for `tcod.bsp` provided an excellent example to get me started, and I adapted elements of the tutorial code to create rooms for each of the BSP leaf nodes. After tweaking some parameters being passed to the `split_recursive` function, I was seeing a spread of rooms I was much happier with.

Then came tunneling. At first I simply used the same method as the tutorial, connecting the rooms in the order they were generated, but I didn't like how the tunnels would sometimes span across most of the map to connect distant rooms. I spent quite a lot of time researching different tunneling solutions, and was eventually inspired by [this article](https://varav.in/archive/dungeon/) to use a spanning tree. One room is selected to start the tree, then the closest unconnected room is found and connected with a tunnel. The process repeats, selecting the closest unconnected room to any of the connected rooms and tunneling between them, until all rooms have been connected to the tree. This prevents the massive map-spanning tunnels I was seeing previously, since each connection between rooms is always made to a close neighbour.

I'm much happier with the layouts this new process generates, though I do think they may have come with a cost of being "boring" since this method won't generate any loops, and more backtracking will be required. In the future I would like to explore deliberately placing some loop tunnels between closely neighbouring rooms, and perhaps find other ways to make the layouts more interesting as well.

Here are some resources I found particularly helpful for implementing my BSP procedural generation:
- https://varav.in/archive/dungeon/
- https://eskerda.com/bsp-dungeon-generation/
- https://stonesigil.com/blog/bsp-roguelike-csharp/

See you next week!
