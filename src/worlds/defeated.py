from typing import Sequence

import pygame
from common import util
from common.event import EventType, GameEvent
from common.util import now
from worlds.base_scene import BaseScene
from config import DATA_DIR, Color, GameConfig


class Defeated(BaseScene):
    """Show when player dies."""
    BG_MAX_ALPHA = 160

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.created_at_ms: int = now()
        self.bg_alpha = 0

        self.background = util.scale_image(
            pygame.image.load(GameConfig.DEFEAT_BACKGROUND).convert(),
            (GameConfig.WIDTH, GameConfig.HEIGHT),
        )

    def tick(self, events: Sequence[GameEvent]) -> bool:
        super().tick(events)

        # TODO: clean up, move hardcoded values to configs
        self.draw_background()

        now_ms = now()
        if now_ms - self.created_at_ms > 1800:
            util.display_text(self.screen, text='Restarting Level...', x=500, y=500, font_size=32)
        if now_ms - self.created_at_ms > 4100:
            GameEvent(EventType.RESTART_LEVEL).post()
        return True

    def draw_background(self):
        self.bg_alpha = min(self.bg_alpha + 0.5, self.BG_MAX_ALPHA)
        self.background.set_alpha(self.bg_alpha)
        self.screen.blit(self.background, (0, 0))
