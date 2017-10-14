import pygame
import os
from itertools import chain, cycle

ACTIVE, WAITING, SCROLLING, END = [i for i in range(4)]


class Textmanager:   # Probably the most nasty piece of code. Not for the faint of heart.

    def __init__(self, screen):
        self.screen = screen
        self.state = END
        self.active_lines = [0, 1]                                          # lines currently in view in the textbox

        self.scroll_gen = cycle([0 for _ in range(3)] +                     # generator of y-axis-locations where the
                                [16 for _ in range(3)] +                    # the text is (briefly) displayed while
                                [32 for _ in range(3)] +                    # changing active lines.
                                [48 for _ in range(3)] +                    # aka scrolling animation
                                [64 for _ in range(1)])

        self.arrow_cycle_gen = cycle([False for _ in range(40)] +           # generator for the little blinking arrow
                                     [True for _ in range(40)])             # at the bottom right of the textbox
                                                                            # while expecting user input

        self.alphabet = pygame.image.load(os.path.join('text', 'alphabet.png'))
        self.alphabet.convert()

        self.text_box = pygame.image.load(os.path.join('text', 'textbox.png'))
        self.text_box.convert()

        self.text_surface = pygame.Surface((576, 96))
        self.text_surface.fill((248, 248, 248))
        self.text_surface.convert()

        self.string = ''
        self.formatted_string = ''
        self.animation_offset = 0
        self.characters_to_print = 0

        self.alphabet_dict = {'?': (589, 43),                               # locations on the alphabet surface
                              '!': (605, 43),                               # for convenient access
                              '(': (477, 27),
                              ')': (493, 27),
                              ':': (509, 27),
                              ';': (525, 27),
                              '[': (541, 27),
                              ']': (557, 27),
                              '.': (189, 59),
                              '/': (205, 59),
                              ',': (221, 59),
                              ' ': (477, 59),
                              'DOWNARROW': (125, 59)}

        self.char_dict = {}                                                 # (KEY, VALUE) = (CHARACTER, SURFACE)

        # locations of regular alphanumeric characters are all added to the char_dict
        for i in chain(range(65, 91), range(97, 100), range(100, 123), range(48, 58)):
            if 65 <= i <= 90:
                char_position = (61 + (i - 65) * 16, 27)
            if 97 <= i <= 99:
                char_position = (573 + (i - 97) * 16, 27)
            if 100 <= i <= 122:
                char_position = (29 + (i - 100) * 16, 43)
            if 48 <= i <= 57:
                char_position = (253 + (i - 48) * 16, 59)
            char_surf = self.alphabet.subsurface(pygame.Rect(char_position[0], char_position[1], 8, 8))
            char_surf = pygame.transform.scale(char_surf, (32, 32))
            char_surf.convert()
            self.char_dict[chr(i)] = char_surf

        for i in self.alphabet_dict:
            char_surf = self.alphabet.subsurface(pygame.Rect(self.alphabet_dict[i][0], self.alphabet_dict[i][1], 8, 8))
            char_surf = pygame.transform.scale(char_surf, (32, 32))
            char_surf.convert()
            self.char_dict[i] = char_surf

    def draw(self):
        # First thing to do to display the text is to draw the textbox on the screen.
        # Then, the text surface on the inside of the textbox is cleaned.
        self.screen.blit(self.text_box, (0, 7*64 - 64))
        self.text_surface.fill((248, 248, 248))

        # I have no memory of this place, but it works!

        # Print the first line for as many characters as are currently set to display by characters_to_print
        for i, c in enumerate(self.formatted_string[self.active_lines[0]]):
            if i >= self.characters_to_print:
                break
            self.text_surface.blit(self.char_dict[c], (32 * i, 0 - self.animation_offset))

        # Same for the second line
        for i, c in enumerate(self.formatted_string[self.active_lines[1]]):
            if i + len(self.formatted_string[self.active_lines[0]]) >= self.characters_to_print:
                break
            self.text_surface.blit(self.char_dict[c], (32 * i, 64 - self.animation_offset))

        # display the blinking arrow when awaiting user input to scroll to the next visible line of text
        if self.state == WAITING and self.active_lines[1] + 1 < len(self.formatted_string) \
                and next(self.arrow_cycle_gen):
            self.text_surface.blit(self.char_dict['DOWNARROW'], (32 * 17, 64))

        self.screen.blit(self.text_surface, (32, 7 * 64))

    # format a given string to substrings of length 17 max and don't divide words
    def format_18(self):
        split_str = self.string.split(' ')
        split_str.reverse()
        if max(map(len, split_str)) >= 17:
            raise Exception('TextBox String contains words with more than 17 characters.')
        formatted_string = []
        current_line = ''
        while split_str:
            next_word_length = len(split_str[-1])
            if len(current_line) + next_word_length + 1 < 18:
                current_line = current_line + split_str.pop() + ' '
            else:
                formatted_string.append(current_line[:-1])
                current_line = ''
        formatted_string.append(current_line[:-1])
        self.formatted_string = formatted_string

    def is_finished(self):
        if self.state == END:
            return True
        else:
            return False

    def set_string(self, string):
        if self.state == END:
            self.state = ACTIVE
            self.string = string
            self.characters_to_print = 0
            self.animation_offset = 0
            self.active_lines = [0, 1]
            self.format_18()
            print(self.formatted_string)

    def set_continue_dialogue(self):
        if self.state == WAITING:
            if self.active_lines[1] + 1 < len(self.formatted_string):
                self.state = SCROLLING
            else:
                self.state = END

    # text logic
    def update(self):
        # In the ACTIVE state, switch to WAITING state when two lines are fully visible
        if self.state == ACTIVE:
            if self.characters_to_print == len(self.formatted_string[self.active_lines[0]] +
                                               self.formatted_string[self.active_lines[1]]):
                self.state = WAITING

        # In the ACTIVE state, continuously raise characters_to_print
        if self.state == ACTIVE:
            if self.characters_to_print < sum(map(len, self.formatted_string)):
                self.characters_to_print += 1

        # In the SCROLLING state, change location of the active lines until the first line is no longer in view
        # and the second line is in place of the first. Then, increment the active lines and change characters_to_print
        # accordingly
        if self.state == SCROLLING:
            next_generated_value = next(self.scroll_gen)
            self.animation_offset = next_generated_value

            if next_generated_value == 64:
                self.state = ACTIVE
                self.animation_offset = 0
                self.active_lines = [self.active_lines[0] + 1, self.active_lines[1] + 1]
                self.characters_to_print = len(self.formatted_string[self.active_lines[0]])
