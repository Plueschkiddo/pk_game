import pygame
import actor
import gamelogic

# Initialize Pygame.
pygame.init()
# Set size of pygame window.
screen = pygame.display.set_mode((640, 576))
# Create empty pygame surface.
background = pygame.Surface(screen.get_size())
# Fill the background black color.
background.fill((0, 0, 0))
# Convert Surface object to make blitting faster.
background = background.convert()
# Copy background to screen (position (0, 0) is upper left corner).
screen.blit(background, (0, 0))
# Create Pygame clock object.
clock = pygame.time.Clock()

mainloop = True
# Desired framerate in frames per second. Try out other values.
FPS = 60
# How many seconds the "game" is played.
playtime = 0.0

# set key repetition
pygame.key.set_repeat(100, 30)

# music
# pygame.mixer.music.load('pallet_town.ogg')
# pygame.mixer.music.set_volume(0.25)
# pygame.mixer.music.play()

arceus = gamelogic.GameLogic(screen)

while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_SPACE:
                arceus.manage_input(pygame.K_SPACE)
            if event.key == pygame.K_LEFT:
                arceus.manage_input(actor.LEFT)
            if event.key == pygame.K_RIGHT:
                arceus.manage_input(actor.RIGHT)
            if event.key == pygame.K_UP:
                arceus.manage_input(actor.UP)
            if event.key == pygame.K_DOWN:
                arceus.manage_input(actor.DOWN)
            if event.key == pygame.K_ESCAPE:
                mainloop = False

    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    # Clear screen
    screen.blit(background, (0, 0))

    # Update game logic
    arceus.update()

    # Update Pygame display.
    pygame.display.flip()

# Finish Pygame.
# pygame.mixer.music.stop()
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))