import pygame
from pixeljump.settings import load_settings

settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]


class Target(pygame.sprite.Sprite):
    def __init__(
        self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
