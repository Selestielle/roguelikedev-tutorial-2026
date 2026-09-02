import random
from typing import List, Tuple, TYPE_CHECKING

import tcod

import tile_types
from game_map import GameMap
from procgen import RectangularRoom, place_entities, tunnel_between

if TYPE_CHECKING:
    from engine import Engine


def generate_dungeon_bsp(
        map_width: int,
        map_height: int,
        max_depth: int,
        node_min_size: int,
        max_horizontal_ratio: int,
        max_vertical_ratio: int,
        room_min_size: int,
        room_max_size: int,
        max_monsters_per_room: int,
        engine: Engine
) -> GameMap:
    """Generate a new dungeon map using binary space partitioning."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, [player])
    rooms: List[RectangularRoom] = []

    bsp = tcod.bsp.BSP(0, 0, map_width - 1, map_height - 1)
    bsp.split_recursive(
        depth=max_depth,
        min_width=node_min_size,
        min_height=node_min_size,
        max_horizontal_ratio=max_horizontal_ratio,
        max_vertical_ratio=max_vertical_ratio
    )

    for node in bsp.pre_order():
        if node.children:
            pass
        else:
            room_width = random.randint(room_min_size, min(node.width, room_max_size))
            room_height = random.randint(room_min_size, min(node.height, room_max_size))

            x = random.randint(node.x, node.x + node.width - room_width)
            y = random.randint(node.y, node.y + node.height - room_height)

            new_room = RectangularRoom(x, y, room_width, room_height)
            dungeon.tiles[new_room.inner] = tile_types.floor

            place_entities(new_room, dungeon, max_monsters_per_room)

            rooms.append(new_room)

    connected: List[RectangularRoom] = [rooms.pop()]
    unconnected: List[RectangularRoom] = rooms

    while len(unconnected) > 0:
        new_connection = find_next_connection(connected, unconnected)
        unconnected.remove(new_connection[1])
        connected.append(new_connection[1])
        for x, y in tunnel_between(new_connection[0].center, new_connection[1].center):
            dungeon.tiles[x, y] = tile_types.floor

    player.place(*connected[0].center, dungeon)

    return dungeon


def find_next_connection(
        connected: List[RectangularRoom],
        unconnected: List[RectangularRoom]
) -> Tuple[RectangularRoom, RectangularRoom]:
    nearest_connected: RectangularRoom = None
    nearest_unconnected: RectangularRoom = None
    distance_to_nearest: int = -1

    for connected_room in connected:
        for unconnected_room in unconnected:
            abs_x = abs(connected_room.center[0] - unconnected_room.center[0])
            abs_y = abs(connected_room.center[1] - unconnected_room.center[1])
            distance = abs_x + abs_y 
            if distance < distance_to_nearest or nearest_unconnected == None:
                nearest_connected = connected_room
                nearest_unconnected = unconnected_room
                distance_to_nearest = distance

    return [nearest_connected, nearest_unconnected]
