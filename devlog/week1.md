# Week 1 - Parts 0 and 1

## Part 0

There isn't much to talk about for this part, installing Python went quite smoothly for me. The few minor wrinkles I encountered were due to user error, stemming from my lack of experience in working with Python - but at least they  provided opportunities to dive in and learn more!

## Part 1

The tutorial steps were easy to understand and complete, and I didn't run into any problems. I was very tempted to tweak a lot of things to my liking as I went, but ultimately decided to do things more or less by-the-book for my first pass, since it will make for easier following along with future tutorial steps.

Two things came up this week that I think deserve a little extra attention in this devlog.

### The EventDispatch Warnings

I noticed a number of different warnings showing up in the terminal while I was testing. I strongly dislike ignoring warnings, even if they're completely benign. If you let it get out of hand, important errors can easily get lost in the noise! Most of the warnings were quite simple to fix - the warnings themselves often tell you exactly what you should be doing - but three of them turned out to be a little more trouble...

```
main.py:36: RuntimeWarning: ev_pixelsizechanged is missing from this EventDispatch object.
main.py:36: RuntimeWarning: ev_displayscalechanged is missing from this EventDispatch object.
main.py:36: RuntimeWarning: ev_clipboardupdate is missing from this EventDispatch object.
```

 The *real* problem here is in the `input_handlers.py` file, although you won't see this warning in the terminal when running `main.py`:

```
input_handlers.py:8: DeprecationWarning: EventDispatch is no longer maintained. Event dispatching should be handled via a single custom method in a Protocol instead of this class.
```

Looks like the three missing events were added to `tcod.event` after `EventDispatch` was deprecated, so the events are being parsed but the `EventDispatch` object is unable to find corresponding function stubs.

The deprecation warning recommends using a `Protocol` instead, but in [this Reddit thread](https://www.reddit.com/r/roguelikedev/comments/1mlzfao/tcod_query_migrating_tutorial_from/) about the issue, HexDecimal (the maintainer of libtcod and python-tcod) suggests simply ignoring the warning instead since it will make the tutorial harder to follow. I'm not going to assume I know better than them, but I still don't want those warnings clogging up my terminal. I'll manually hide the warnings for now and leave a note for myself to fix them properly at the end of the tutorial.

```python
#!/usr/bin/env python3
import warnings

import tcod

# [...]

if __name__ == "__main__":
    # TODO: Replace deprecated EventDispatch with Protocol.
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', ".*is missing from this EventDispatch object.")
        main()
```

Let's see if I remember to come back to that - place your bets now!

### Supporting High DPI

I was primarily developing on a laptop with a high DPI display this week, so my game window was appearing *very* small on my screen and the symbols were difficult to read. I decided to take it upon myself to add high DPI support.

While looking around in the [python-tcod documentation](https://python-tcod.readthedocs.io/en/latest/tcod/context.html), I found the `tcod.context.SDL_WINDOW_ALLOW_HIGHDPI` flag, but simply passing that flag to `tcod.context.new` didn't make an observable difference. Digging into the [SDL documentation](https://wiki.libsdl.org/SDL3/README-highdpi), it seems like that flag is primarily for macOS systems, perhaps? In any case, high DPI support on Windows is instead achieved via getting a content scale from `SDL_GetDisplayContentScale()` and scaling the context up manually.

The tutorial initialises the size of the context via a specific number of columns and rows, but doing so doesn't let us scale that context and its contents easily. Instead I changed the context to initialise with pixel width and height values that are calculated beforehand. Debugging SDL functions to get this working was an interesting challenge!

```python
#!/usr/bin/env python3
import warnings
from typing import Any

import tcod
from tcod.tileset import Tileset

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def get_context_size(display_id: Any, tileset: Tileset, columns: int, rows: int) -> tuple[int]:
    content_scale = tcod.lib.SDL_GetDisplayContentScale(display_id)
    context_width = int(columns * tileset.tile_width * content_scale)
    context_height = int(rows * tileset.tile_height * content_scale)
    return [context_width, context_height]

# [...]

event_handler = EventHandler()

tcod.lib.SDL_Init(tcod.lib.SDL_INIT_VIDEO)
display_id = tcod.lib.SDL_GetPrimaryDisplay()
context_size = get_context_size(display_id, tileset, screen_width, screen_height)

with tcod.context.new(
    width=context_size[0],
    height=context_size[1],
    tileset=tileset,
    title="Yet Another Roguelike Tutorial",
    vsync=True,
) as context:
```

This scales the window to match the content scale upon startup. Later I encountered a new problem when I connected a secondary 1080p display to my laptop and dragged the game window over - the window didn't re-scale for the current display. Luckily, I knew there was a `"DisplayScaleChanged"` event I could hook into from the warnings above - hooking into that event and resizing the window when it is received wasn't too difficult.

```python
for event in tcod.event.wait():
    if isinstance(event, tcod.event.WindowEvent):
        window_event: tcod.event.WindowEvent = event
        if (window_event.type == "DisplayScaleChanged"):
            display_id = tcod.lib.SDL_GetDisplayForWindow(context.sdl_window_p)
            context.sdl_window.size = get_context_size(display_id, tileset, screen_width, screen_height)
        continue
    
    action = event_handler.dispatch(event)
```

Finally, I didn't really like the default font provided by the tutorial - the antialiasing on the symbols just looked too blurry to my eyes - so I grabbed the cp437_12x12.png font that comes included with [REXPaint](https://www.gridsagegames.com/rexpaint/) for my tileset instead. This also required changing the charmap to `tcod.tileset.CHARMAP_CP437` when loading the tilesheet.

```python
tileset = tcod.tileset.load_tilesheet(
    "cp437_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437
)
```

The game window is now much more friendly towards high DPI displays!

That's all for this week! I'm looking forward to week two - come back soon for another devlog!
