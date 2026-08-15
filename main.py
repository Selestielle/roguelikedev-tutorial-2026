#!/usr/bin/env python3
import warnings
from typing import Any

import tcod
from tcod.tileset import Tileset

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


def get_context_size(display_id: Any, tileset: Tileset, columns: int, rows: int) -> tuple[int]:
    content_scale = tcod.lib.SDL_GetDisplayContentScale(display_id)
    context_width = int(columns * tileset.tile_width * content_scale)
    context_height = int(rows * tileset.tile_height * content_scale)
    return [context_width, context_height]


def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "cp437_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    tcod.lib.SDL_Init(tcod.lib.SDL_INIT_VIDEO)
    display_id = tcod.lib.SDL_GetPrimaryDisplay()
    context_size = get_context_size(display_id, tileset, screen_width, screen_height)

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)
    event_handler = EventHandler()
    engine = Engine(entities, event_handler, game_map, player)

    with tcod.context.new(
        width=context_size[0],
        height=context_size[1],
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(root_console, context)
            events = tcod.event.wait()

            for event in events:
                if isinstance(event, tcod.event.WindowEvent):
                    if (event.type == "DisplayScaleChanged"):
                        display_id = tcod.lib.SDL_GetDisplayForWindow(context.sdl_window_p)
                        context.sdl_window.size = get_context_size(display_id, tileset, screen_width, screen_height)
                        continue

                engine.handle_event(event)


if __name__ == "__main__": 
    # TODO: Replace deprecated EventDispatch with Protocol.
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', ".*is missing from this EventDispatch object.")
        main()
