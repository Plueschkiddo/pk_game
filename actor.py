import pygame

LEFT, RIGHT, UP, DOWN, LEFT_WALK, RIGHT_WALK, UP_WALK, DOWN_WALK = 0, 1, 2, 3, 4, 5, 6, 7


class Actor(pygame.sprite.Sprite):

    # Constructor. Pass in the image of the actor
    def __init__(self, images, x, y):

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # This is an image loaded from the disk
        self.sprite_images = images
        self.image = self.sprite_images.subsurface((0, 0, 56, 64))
        self.image.convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Actor should know its own orientation for animation purposes
        self.orientation = (-1, 0)

    def set_direction(self, direction):
        if direction == LEFT:
            self.orientation = (-1, 0)
        elif direction == RIGHT:
            self.orientation = (1, 0)
        elif direction == UP:
            self.orientation = (0, -1)
        elif direction == DOWN:
            self.orientation = (0, 1)
        self.image = self.sprite_images.subsurface((direction * 56, 0, 56, 64))
        self.image.convert_alpha()

