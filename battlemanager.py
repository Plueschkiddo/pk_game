import pygame
import os

TRANSITION, ACTIVE, OPTIONS, FIGHT, POKEMON, ITEM, RUN = range(7)

FINAL_CHARACTER_SPRITE_POSITION = (8, 160)


class BattleManager:

    def __init__(self, screen):
        self.state = TRANSITION
        self.screen = screen
        self.character_position = (-151, 160)

        self.screen_surf = pygame.image.load(os.path.join('battle', 'battle_starting_screen.png'))
        self.screen_surf = pygame.transform.scale(self.screen_surf, (640, 576))
        self.screen_surf.convert()

        self.options_surf = pygame.image.load(os.path.join('battle', 'battle_options_screen.png'))
        self.options_surf = pygame.transform.scale(self.options_surf, (640, 576))
        self.options_surf.convert()

        self.character_back_pose_surf = pygame.image.load(os.path.join('battle', 'battle_character_back_pose.png'))
        self.character_back_pose_surf = pygame.transform.scale(self.character_back_pose_surf, (224, 224))
        self.character_back_pose_surf.convert()

    def draw(self):
        if self.state == TRANSITION:
            self.screen.blit(self.screen_surf, (0, 0))
            self.screen.blit(self.character_back_pose_surf, self.character_position)
        elif self.state == ACTIVE:
            self.screen.blit(self.screen_surf, (0, 0))
            self.screen.blit(self.character_back_pose_surf, self.character_position)
        elif self.state == OPTIONS:
            pass
        elif self.state == FIGHT:
            pass
        elif self.state == POKEMON:
            pass
        elif self.state == ITEM:
            pass
        elif self.state == RUN:
            pass

    def update(self):
        if self.state == TRANSITION:
            if self.character_position != FINAL_CHARACTER_SPRITE_POSITION:
                self.character_position = (self.character_position[0] + 3, self.character_position[1])
            else:
                self.state = ACTIVE
