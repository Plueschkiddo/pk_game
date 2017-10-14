import os
import pygame
import map
import actor
import transition
import textmanager
import battlemanager

ACTIVE, DIALOGUE, BATTLE, TRANSITION = range(4)


class GameLogic:

    def __init__(self, screen):
        self.screen = screen
        self.accept_input = True
        self.animation = None           # current playing animation
        self.state = ACTIVE             # state that the game starts with. change to experience various features

        self.pallet_town_map = map.Map(pygame.image.load(os.path.join('maps', 'pallet_town.png')), (-64 * 5, 0))

        self.mc = actor.Actor(pygame.image.load(os.path.join('actors', 'mc_final.png')), 64 * 4 + 4, 64 * 4)
        self.actor_group = pygame.sprite.Group(self.mc)

        # Initialize a screen transition
        self.trans = transition.Transition(screen)
        self.trans.order_swirl()

        # Initialize a text manager
        self.txtmgr = textmanager.Textmanager(screen)

        # Do this only if DIALOGUE is the initial game state
        if self.state == DIALOGUE:
            self.txtmgr.set_string('Boogah boogah boogah!')

        # Initiate a battle manager
        self.btlmgr = battlemanager.BattleManager(screen)

    def update(self):
        # If an animation is running, update it.
        if self.animation:
            self.animation_update()

        # Paint the map and actor on the screen.
        self.screen.blit(self.pallet_town_map.image, self.pallet_town_map.position)
        self.actor_group.draw(self.screen)

        # If a textbox is currently displayed, accept no input (except space) and update the text manager.
        # When the text manager is done displaying characters, stop drawing and resume active state.
        if self.state == DIALOGUE:
            self.accept_input = False
            self.txtmgr.draw()
            self.txtmgr.update()
            if self.txtmgr.is_finished():
                self.state = ACTIVE
                self.accept_input = True

        # In this state, the screen will transition from the currently displayed map (actor, text, etc.)
        # to a black screen. Then, change game state to BATTLE.
        if self.state == TRANSITION:
            self.trans.draw()
            self.trans.update()
            if self.trans.is_finished():
                self.state = BATTLE

        # Nothing else here yet, besides updating and drawing.
        if self.state == BATTLE:
            self.btlmgr.draw()
            self.btlmgr.update()

        # When not in ACTIVE game state, don't accept input.
        if self.state != ACTIVE:
            self.accept_input = False

    def manage_input(self, key_input):
        if self.accept_input:
            if key_input == actor.LEFT:
                if not self.pallet_town_map.obstruction_check(-1, 0):
                    self.animation = self.walking_left
                    self.accept_input = False
                    self.pallet_town_map.set_actor_position(-1, 0)
                else:
                    self.mc.set_direction(actor.LEFT)
            if key_input == actor.RIGHT:
                if not self.pallet_town_map.obstruction_check(1, 0):
                    self.animation = self.walking_right
                    self.accept_input = False
                    self.pallet_town_map.set_actor_position(1, 0)
                else:
                    self.mc.set_direction(actor.RIGHT)
            if key_input == actor.UP:
                if not self.pallet_town_map.obstruction_check(0, -1):
                    self.animation = self.walking_up
                    self.accept_input = False
                    self.pallet_town_map.set_actor_position(0, -1)
                else:
                    self.mc.set_direction(actor.UP)
            if key_input == actor.DOWN:
                if not self.pallet_town_map.obstruction_check(0, 1):
                    self.animation = self.walking_down
                    self.accept_input = False
                    self.pallet_town_map.set_actor_position(0, 1)
                else:
                    self.mc.set_direction(actor.DOWN)

        if key_input == pygame.K_SPACE:
            event = self.pallet_town_map.event_check(self.mc.orientation)
            if event:
                self.txtmgr.set_string(event)
                self.state = DIALOGUE
            print(event)
            self.txtmgr.set_continue_dialogue()

    def animation_update(self):
        if self.animation():
            self.animation = None
            self.accept_input = True

    # These bottom four should definitely be somewhere else (probably map.py)
    def walking_right(self):
        self.pallet_town_map.position = (self.pallet_town_map.position[0] - 4, self.pallet_town_map.position[1])
        if self.pallet_town_map.position[0] % 64 < 32:
            self.mc.set_direction(actor.RIGHT)
        if self.pallet_town_map.position[0] % 64 > 32:
            self.mc.set_direction(actor.RIGHT_WALK)
        if self.pallet_town_map.position[0] % 64 == 0:
            self.mc.set_direction(actor.RIGHT)
        if self.pallet_town_map.position[0] % 64:
            return False
        else:
            return True

    def walking_left(self):
        self.pallet_town_map.position = (self.pallet_town_map.position[0] + 4, self.pallet_town_map.position[1])
        if self.pallet_town_map.position[0] % 64 < 32:
            self.mc.set_direction(actor.LEFT_WALK)
        if self.pallet_town_map.position[0] % 64 > 32:
            self.mc.set_direction(actor.LEFT)
        if self.pallet_town_map.position[0] % 64 == 0:
            self.mc.set_direction(actor.LEFT)
        if self.pallet_town_map.position[0] % 64:
            return False
        else:
            return True

    def walking_up(self):
        self.pallet_town_map.position = (self.pallet_town_map.position[0], self.pallet_town_map.position[1] + 4)
        if self.pallet_town_map.position[1] % 64 < 32:
            self.mc.set_direction(actor.UP)
        if self.pallet_town_map.position[1] % 64 > 32:
            self.mc.set_direction(actor.UP_WALK)
        if self.pallet_town_map.position[1] % 64 == 0:
            self.mc.set_direction(actor.UP)
        if self.pallet_town_map.position[1] % 64:
            return False
        else:
            return True

    def walking_down(self):
        self.pallet_town_map.position = (self.pallet_town_map.position[0], self.pallet_town_map.position[1] - 4)
        if self.pallet_town_map.position[1] % 64 < 32:
            self.mc.set_direction(actor.DOWN)
        if self.pallet_town_map.position[1] % 64 > 32:
            self.mc.set_direction(actor.DOWN_WALK)
        if self.pallet_town_map.position[1] % 64 == 0:
            self.mc.set_direction(actor.DOWN)
        if self.pallet_town_map.position[1] % 64:
            return False
        else:
            return True
