from typing import Set, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(
            self,
            entities: Set[Entity],
            event_handler: EventHandler,
            game_map: GameMap,
            player: Entity
    ) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_event(self, event: Any) -> None:
        action = self.event_handler.dispatch(event)

        if action is None:
            return

        action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()
