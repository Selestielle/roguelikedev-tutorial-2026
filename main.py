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


def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "cp437_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

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
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, text="@")

            context.present(root_console)

            root_console.clear()

            for event in tcod.event.wait():
                if isinstance(event, tcod.event.WindowEvent):
                    window_event: tcod.event.WindowEvent = event
                    if (window_event.type == "DisplayScaleChanged"):
                        display_id = tcod.lib.SDL_GetDisplayForWindow(context.sdl_window_p)
                        context.sdl_window.size = get_context_size(display_id, tileset, screen_width, screen_height)
                    continue

                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__": 
    # TODO: Replace deprecated EventDispatch with Protocol.
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', ".*is missing from this EventDispatch object.")
        main()
