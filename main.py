import pygame
import random #choose random variables for the ball's movement

pygame.init() #starts pygame and creates a window for the game Pong


#GAME SETTINGS

# Controls how many times the game updates every second
clock = pygame.time.Clock()

# Target frame rate
FPS = 60

# Starting size of the game window
WIDTH = 800
HEIGHT = 500

# Smallest size the window is allowed to become
MIN_WIDTH = 700
MIN_HEIGHT = 450


#COLORS

LIGHT_PINK = (255, 219, 229) #background color of the game
SOFT_PINK = (255, 190, 210)
BUTTON_PINK = (255, 235, 241)
HOVER_PINK = (255, 245, 248)
WHITE = (255, 255, 255)
DARK_PINK = (174, 72, 115)
SHADOW_PINK = (225, 150, 177)
GAME_COLOR = (255, 255, 255) #color used for paddles, ball, and court


#FONTS

# Large bold font used for PONG
title_font = pygame.font.SysFont(
    "arialblack",
    75
)

# Font used for winner messages
winner_font = pygame.font.SysFont(
    "arialblack",
    55
)

# Font used for buttons
menu_font = pygame.font.SysFont(
    "arial",
    34,
    bold=True
)

# Font used for smaller text
small_font = pygame.font.SysFont(
    "arial",
    22,
    bold=True
)

# Font used for lives
lives_font = pygame.font.SysFont(
    "segoeuisymbol",
    28
)


#GAME STATE

current_screen = "menu"

# Keep track of whether the match has started
game_started = False

# Each player starts with 5 lives
left_lives = 5
right_lives = 5

# Keeps track of whether the game is waiting after someone loses a life
round_paused = False

# Keeps track of when the pause started
pause_start_time = 0

# How long the pause lasts in milliseconds
# 2000 milliseconds = 2 seconds
PAUSE_TIME = 2000

# Stores the winner when the game ends
winner = ""

# Remembers whether the player chose singleplayer or multiplayer
last_game_mode = ""

# Stores which difficulty the player chose
ai_difficulty = "normal"

# Controls how quickly the AI paddle moves
AI_SPEED = 4


#WINDOW

# pygame.RESIZABLE allows the player to drag
# the edges of the window to make it bigger or smaller
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption("Pong")


#BUTTONS

# These buttons will have their positions updated
# whenever the window changes size
single_button = pygame.Rect(0, 0, 300, 65)
multiplayer_button = pygame.Rect(0, 0, 300, 65)

back_button = pygame.Rect(30, 30, 120, 50)

play_again_button = pygame.Rect(0, 0, 300, 65)
main_menu_button = pygame.Rect(0, 0, 300, 65)

easy_button = pygame.Rect(0, 0, 300, 60)
normal_button = pygame.Rect(0, 0, 300, 60)
impossible_button = pygame.Rect(0, 0, 300, 60)


#OBJECTS

# Size of each paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 70

# Create the LEFT paddle
left_paddle = pygame.Rect(
    40,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# Create the RIGHT paddle
right_paddle = pygame.Rect(
    WIDTH - 55,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# Create the ball
BALL_SIZE = 20

ball = pygame.Rect(
    WIDTH // 2 - BALL_SIZE // 2,
    HEIGHT // 2 - BALL_SIZE // 2,
    BALL_SIZE,
    BALL_SIZE
)

# How quickly the paddles move
PADDLE_SPEED = 6

# How quickly the ball moves
BALL_SPEED = 5

# Random starting horizontal direction
BALL_SPEED_X = random.choice(
    [-BALL_SPEED, BALL_SPEED]
)

# Random starting vertical direction
BALL_SPEED_Y = random.choice(
    [-BALL_SPEED, BALL_SPEED]
)


#LAYOUT FUNCTION

# This function moves the buttons into the correct places
# depending on the current size of the window
def update_layout():

    #MAIN MENU BUTTONS

    single_button.center = (
        WIDTH // 2,
        HEIGHT // 2
    )

    multiplayer_button.center = (
        WIDTH // 2,
        HEIGHT // 2 + 85
    )


    #DIFFICULTY BUTTONS

    easy_button.center = (
        WIDTH // 2,
        HEIGHT // 2 - 80
    )

    normal_button.center = (
        WIDTH // 2,
        HEIGHT // 2
    )

    impossible_button.center = (
        WIDTH // 2,
        HEIGHT // 2 + 80
    )


    #GAME OVER BUTTONS

    play_again_button.center = (
        WIDTH // 2,
        HEIGHT // 2 + 60
    )

    main_menu_button.center = (
        WIDTH // 2,
        HEIGHT // 2 + 145
    )


    #BACK BUTTON

    # Keep the Back button near the top left
    back_button.x = 30
    back_button.y = 30


# Run the layout function once when the game starts
update_layout()


#BUTTON FUNCTION

# This function draws a button
def draw_button(button, text, font):

    # Get the current mouse position
    mouse_position = pygame.mouse.get_pos()

    # Check if the mouse is touching the button
    mouse_over_button = button.collidepoint(
        mouse_position
    )


    #BUTTON SHADOW

    # Create a rectangle slightly below the real button
    shadow = pygame.Rect(
        button.x,
        button.y + 5,
        button.width,
        button.height
    )

    # Draw the shadow
    pygame.draw.rect(
        screen,
        SHADOW_PINK,
        shadow,
        border_radius=18
    )


    #BUTTON COLOR

    # Make the button lighter when the mouse is over it
    if mouse_over_button:

        button_color = HOVER_PINK

    else:

        button_color = BUTTON_PINK


    # Draw the real button
    pygame.draw.rect(
        screen,
        button_color,
        button,
        border_radius=18
    )


    #BUTTON TEXT

    # Create the text
    button_text = font.render(
        text,
        True,
        DARK_PINK
    )

    # Put the text in the center
    screen.blit(
        button_text,
        button_text.get_rect(
            center=button.center
        )
    )


#HEART FUNCTION

# This function displays the remaining lives
def draw_hearts(lives, center_x):

    # Create one heart for every life remaining
    hearts = "♥ " * lives

    # Create the heart text
    heart_text = lives_font.render(
        hearts,
        True,
        DARK_PINK
    )

    # Center the hearts around the position we give it
    heart_rect = heart_text.get_rect(
        center=(center_x, 35)
    )

    # Draw the hearts
    screen.blit(
        heart_text,
        heart_rect
    )


#RESET FUNCTION

# This function resets the paddles and ball
# so we do not have to repeat the same code as much
def reset_game_objects():

    global BALL_SPEED_X
    global BALL_SPEED_Y

    # Put the left paddle in the center
    left_paddle.x = 40
    left_paddle.centery = HEIGHT // 2

    # Put the right paddle in the center
    right_paddle.x = WIDTH - 55
    right_paddle.centery = HEIGHT // 2

    # Put the ball in the center
    ball.center = (
        WIDTH // 2,
        HEIGHT // 2
    )

    # Choose new random directions
    BALL_SPEED_X = random.choice(
        [-BALL_SPEED, BALL_SPEED]
    )

    BALL_SPEED_Y = random.choice(
        [-BALL_SPEED, BALL_SPEED]
    )


#GAME LOOP

running = True

# The while loop keeps the game running
while running:


    #EVENTS

    # pygame.event.get() checks things the user does
    for event in pygame.event.get():


        #QUIT

        # If the player clicks the X on the window
        if event.type == pygame.QUIT:

            running = False


        #WINDOW RESIZING

        # Check if the player resized the game window
        if event.type == pygame.VIDEORESIZE:

            # Prevent the window from becoming too small
            WIDTH = max(
                event.w,
                MIN_WIDTH
            )

            HEIGHT = max(
                event.h,
                MIN_HEIGHT
            )

            # Create the window again using the new size
            screen = pygame.display.set_mode(
                (WIDTH, HEIGHT),
                pygame.RESIZABLE
            )

            # Move all menu buttons to match the new window
            update_layout()


            #PADDLE POSITIONS

            # Keep the left paddle attached to the left side
            left_paddle.x = 40

            # Keep the right paddle attached to the right side
            right_paddle.x = WIDTH - 55


            #PADDLE BOUNDARIES

            # Stop left paddle from leaving the bottom
            if left_paddle.bottom > HEIGHT:

                left_paddle.bottom = HEIGHT

            # Stop right paddle from leaving the bottom
            if right_paddle.bottom > HEIGHT:

                right_paddle.bottom = HEIGHT


            #BALL BOUNDARIES

            # Stop ball from being outside the right side
            if ball.right > WIDTH:

                ball.right = WIDTH

            # Stop ball from being outside the bottom
            if ball.bottom > HEIGHT:

                ball.bottom = HEIGHT


        #MOUSE CLICKS

        # Check if the mouse was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:


            #MENU

            if current_screen == "menu":

                # Check if Singleplayer was clicked
                if single_button.collidepoint(event.pos):

                    # Go to the difficulty screen
                    current_screen = "difficulty"

                    # Remember Singleplayer
                    last_game_mode = "single"

                    # Game has not started
                    game_started = False


                # Check if Multiplayer was clicked
                elif multiplayer_button.collidepoint(event.pos):

                    # Go to Multiplayer
                    current_screen = "multiplayer"

                    # Remember Multiplayer
                    last_game_mode = "multiplayer"

                    # Reset lives
                    left_lives = 5
                    right_lives = 5

                    # Reset objects
                    reset_game_objects()

                    # Wait for the player to move
                    game_started = False

                    # Make sure the round is not paused
                    round_paused = False


            #DIFFICULTY SCREEN

            elif current_screen == "difficulty":


                #EASY

                if easy_button.collidepoint(event.pos):

                    # Set Easy difficulty
                    ai_difficulty = "easy"

                    # Easy AI moves slowly
                    AI_SPEED = 2

                    # Go to Singleplayer
                    current_screen = "single"

                    # Reset lives
                    left_lives = 5
                    right_lives = 5

                    # Reset objects
                    reset_game_objects()

                    # Wait for player movement
                    game_started = False

                    # Make sure round is not paused
                    round_paused = False


                #NORMAL

                elif normal_button.collidepoint(event.pos):

                    # Set Normal difficulty
                    ai_difficulty = "normal"

                    # Normal AI speed
                    AI_SPEED = 4

                    # Go to Singleplayer
                    current_screen = "single"

                    # Reset lives
                    left_lives = 5
                    right_lives = 5

                    # Reset objects
                    reset_game_objects()

                    # Wait for player movement
                    game_started = False

                    # Make sure round is not paused
                    round_paused = False


                #IMPOSSIBLE

                elif impossible_button.collidepoint(event.pos):

                    # Set Impossible difficulty
                    ai_difficulty = "impossible"

                    # Impossible AI moves very quickly
                    AI_SPEED = 8

                    # Go to Singleplayer
                    current_screen = "single"

                    # Reset lives
                    left_lives = 5
                    right_lives = 5

                    # Reset objects
                    reset_game_objects()

                    # Wait for player movement
                    game_started = False

                    # Make sure round is not paused
                    round_paused = False


                #BACK BUTTON

                elif back_button.collidepoint(event.pos):

                    # Return to menu
                    current_screen = "menu"


            #GAME OVER SCREEN

            elif current_screen == "game_over":


                #PLAY AGAIN

                if play_again_button.collidepoint(event.pos):

                    # Reset lives
                    left_lives = 5
                    right_lives = 5

                    # Reset objects
                    reset_game_objects()

                    # Return to previous game mode
                    current_screen = last_game_mode

                    # Wait for movement
                    game_started = False

                    # Make sure round is not paused
                    round_paused = False


                #MAIN MENU

                elif main_menu_button.collidepoint(event.pos):

                    # Return to menu
                    current_screen = "menu"

                    # Reset lives
                    left_lives = 5
                    right_lives = 5

                    # Reset objects
                    reset_game_objects()

                    # Stop match
                    game_started = False

                    # Make sure round is not paused
                    round_paused = False


            #BACK BUTTON

            elif not game_started:

                # Check if Back was clicked
                if back_button.collidepoint(event.pos):

                    # Return to menu
                    current_screen = "menu"

                    # Reset objects
                    reset_game_objects()


    #KEYBOARD INPUT

    # Get all keyboard keys currently being held down
    keys = pygame.key.get_pressed()


    #MULTIPLAYER CONTROLS

    if current_screen == "multiplayer":


        #START GAME

        # Start if any movement key is pressed
        if (
            keys[pygame.K_w]
            or keys[pygame.K_s]
            or keys[pygame.K_UP]
            or keys[pygame.K_DOWN]
        ):

            game_started = True


        #LEFT PADDLE

        # W moves upward
        if keys[pygame.K_w]:

            left_paddle.y -= PADDLE_SPEED

        # S moves downward
        if keys[pygame.K_s]:

            left_paddle.y += PADDLE_SPEED


        #RIGHT PADDLE

        # Up arrow moves upward
        if keys[pygame.K_UP]:

            right_paddle.y -= PADDLE_SPEED

        # Down arrow moves downward
        if keys[pygame.K_DOWN]:

            right_paddle.y += PADDLE_SPEED


        #BOUNDARY CHECKS

        # Stop left paddle from leaving the top
        if left_paddle.top < 0:

            left_paddle.top = 0

        # Stop left paddle from leaving the bottom
        if left_paddle.bottom > HEIGHT:

            left_paddle.bottom = HEIGHT

        # Stop right paddle from leaving the top
        if right_paddle.top < 0:

            right_paddle.top = 0

        # Stop right paddle from leaving the bottom
        if right_paddle.bottom > HEIGHT:

            right_paddle.bottom = HEIGHT


    #SINGLE PLAYER CONTROLS

    elif current_screen == "single":


        #START GAME

        # Pressing W or S starts the match
        if keys[pygame.K_w] or keys[pygame.K_s]:

            game_started = True


        #PLAYER MOVEMENT

        # W moves upward
        if keys[pygame.K_w]:

            left_paddle.y -= PADDLE_SPEED

        # S moves downward
        if keys[pygame.K_s]:

            left_paddle.y += PADDLE_SPEED


        #PLAYER BOUNDARIES

        # Stop paddle from leaving the top
        if left_paddle.top < 0:

            left_paddle.top = 0

        # Stop paddle from leaving the bottom
        if left_paddle.bottom > HEIGHT:

            left_paddle.bottom = HEIGHT


        #AI MOVEMENT

        # Only move AI when the game is running
        if game_started and not round_paused:


            #EASY AI

            if ai_difficulty == "easy":

                # Easy AI only reacts while the ball
                # is moving toward it
                if BALL_SPEED_X > 0:

                    # Move down
                    if ball.centery > right_paddle.centery + 30:

                        right_paddle.y += AI_SPEED

                    # Move up
                    elif ball.centery < right_paddle.centery - 30:

                        right_paddle.y -= AI_SPEED


            #NORMAL AI

            elif ai_difficulty == "normal":

                # Normal AI reacts while the ball
                # is moving toward it
                if BALL_SPEED_X > 0:

                    # Move down
                    if ball.centery > right_paddle.centery + 10:

                        right_paddle.y += AI_SPEED

                    # Move up
                    elif ball.centery < right_paddle.centery - 10:

                        right_paddle.y -= AI_SPEED


            #IMPOSSIBLE AI

            elif ai_difficulty == "impossible":

                # Impossible AI follows the ball constantly

                # Move down
                if ball.centery > right_paddle.centery:

                    right_paddle.y += AI_SPEED

                # Move up
                elif ball.centery < right_paddle.centery:

                    right_paddle.y -= AI_SPEED


        #AI BOUNDARIES

        # Stop AI from leaving the top
        if right_paddle.top < 0:

            right_paddle.top = 0

        # Stop AI from leaving the bottom
        if right_paddle.bottom > HEIGHT:

            right_paddle.bottom = HEIGHT


    #BALL MOVEMENT

    # Move ball only if the game is running
    if game_started and not round_paused:

        # Move horizontally
        ball.x += BALL_SPEED_X

        # Move vertically
        ball.y += BALL_SPEED_Y


        #BALL BOUNDARY CHECKS

        # Bounce off the top
        if ball.top <= 0:

            ball.top = 0

            BALL_SPEED_Y *= -1

        # Bounce off the bottom
        if ball.bottom >= HEIGHT:

            ball.bottom = HEIGHT

            BALL_SPEED_Y *= -1


        #PADDLE COLLISIONS

        # Check left paddle
        if ball.colliderect(left_paddle):

            # Only bounce if moving left
            if BALL_SPEED_X < 0:

                BALL_SPEED_X *= -1

                # Move ball outside the paddle
                ball.left = left_paddle.right


        # Check right paddle
        if ball.colliderect(right_paddle):

            # Only bounce if moving right
            if BALL_SPEED_X > 0:

                BALL_SPEED_X *= -1

                # Move ball outside the paddle
                ball.right = right_paddle.left


        #LEFT SIDE

        # Ball leaves the left side
        if ball.left <= 0:

            # Left side loses a life
            left_lives -= 1


            #GAME OVER CHECK

            if left_lives <= 0:

                # Stop game
                game_started = False

                round_paused = False

                # Singleplayer winner
                if last_game_mode == "single":

                    winner = "COMPUTER WINS"

                # Multiplayer winner
                else:

                    winner = "PLAYER 2 WINS"

                # Go to Game Over
                current_screen = "game_over"


            else:

                # Reset ball
                ball.center = (
                    WIDTH // 2,
                    HEIGHT // 2
                )

                # Choose random direction
                BALL_SPEED_X = random.choice(
                    [-BALL_SPEED, BALL_SPEED]
                )

                BALL_SPEED_Y = random.choice(
                    [-BALL_SPEED, BALL_SPEED]
                )

                # Pause round
                round_paused = True

                # Remember when pause began
                pause_start_time = pygame.time.get_ticks()


        #RIGHT SIDE

        # Ball leaves the right side
        if ball.right >= WIDTH:

            # Right side loses a life
            right_lives -= 1


            #GAME OVER CHECK

            if right_lives <= 0:

                # Stop game
                game_started = False

                round_paused = False

                # Singleplayer winner
                if last_game_mode == "single":

                    winner = "YOU WIN"

                # Multiplayer winner
                else:

                    winner = "PLAYER 1 WINS"

                # Go to Game Over
                current_screen = "game_over"


            else:

                # Reset ball
                ball.center = (
                    WIDTH // 2,
                    HEIGHT // 2
                )

                # Choose random direction
                BALL_SPEED_X = random.choice(
                    [-BALL_SPEED, BALL_SPEED]
                )

                BALL_SPEED_Y = random.choice(
                    [-BALL_SPEED, BALL_SPEED]
                )

                # Pause round
                round_paused = True

                # Remember when pause began
                pause_start_time = pygame.time.get_ticks()


    #ROUND PAUSE

    # Check if the game is paused after a lost life
    if round_paused:

        # Get current time
        current_time = pygame.time.get_ticks()

        # Calculate how much time passed
        time_passed = current_time - pause_start_time

        # If 2 seconds passed
        if time_passed >= PAUSE_TIME:

            # End pause
            round_paused = False


    #DRAWING

    # Fill the background
    screen.fill(LIGHT_PINK)


    #MAIN MENU

    if current_screen == "menu":


        #TITLE SHADOW

        shadow_title = title_font.render(
            "PONG",
            True,
            SHADOW_PINK
        )

        screen.blit(
            shadow_title,
            shadow_title.get_rect(
                center=(
                    WIDTH // 2 + 4,
                    HEIGHT // 2 - 160 + 4
                )
            )
        )


        #TITLE

        title = title_font.render(
            "PONG",
            True,
            WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 160
                )
            )
        )


        #SUBTITLE

        subtitle = small_font.render(
            "Pick a game mode",
            True,
            DARK_PINK
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 100
                )
            )
        )


        #BUTTONS

        draw_button(
            single_button,
            "Singleplayer",
            menu_font
        )

        draw_button(
            multiplayer_button,
            "Multiplayer",
            menu_font
        )


    #DIFFICULTY SCREEN

    elif current_screen == "difficulty":


        #TITLE

        difficulty_title = title_font.render(
            "PONG",
            True,
            WHITE
        )

        screen.blit(
            difficulty_title,
            difficulty_title.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 190
                )
            )
        )


        #SUBTITLE

        difficulty_text = small_font.render(
            "Choose your difficulty",
            True,
            DARK_PINK
        )

        screen.blit(
            difficulty_text,
            difficulty_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 135
                )
            )
        )


        #DIFFICULTY BUTTONS

        draw_button(
            easy_button,
            "Easy",
            menu_font
        )

        draw_button(
            normal_button,
            "Normal",
            menu_font
        )

        draw_button(
            impossible_button,
            "Impossible",
            menu_font
        )


        #BACK BUTTON

        draw_button(
            back_button,
            "Back",
            small_font
        )


    #SINGLE PLAYER SCREEN

    elif current_screen == "single":


        #CENTER LINE

        pygame.draw.line(
            screen,
            WHITE,
            (WIDTH // 2, 0),
            (WIDTH // 2, HEIGHT),
            3
        )


        #LEFT PADDLE

        pygame.draw.rect(
            screen,
            GAME_COLOR,
            left_paddle,
            border_radius=7
        )


        #RIGHT PADDLE

        pygame.draw.rect(
            screen,
            GAME_COLOR,
            right_paddle,
            border_radius=7
        )


        #BALL

        pygame.draw.circle(
            screen,
            GAME_COLOR,
            ball.center,
            BALL_SIZE // 2
        )


    #MULTIPLAYER SCREEN

    elif current_screen == "multiplayer":


        #CENTER LINE

        pygame.draw.line(
            screen,
            WHITE,
            (WIDTH // 2, 0),
            (WIDTH // 2, HEIGHT),
            3
        )


        #LEFT PADDLE

        pygame.draw.rect(
            screen,
            GAME_COLOR,
            left_paddle,
            border_radius=7
        )


        #RIGHT PADDLE

        pygame.draw.rect(
            screen,
            GAME_COLOR,
            right_paddle,
            border_radius=7
        )


        #BALL

        pygame.draw.circle(
            screen,
            GAME_COLOR,
            ball.center,
            BALL_SIZE // 2
        )


    #GAME OVER SCREEN

    elif current_screen == "game_over":


        #GAME OVER TEXT

        game_over_text = small_font.render(
            "GAME OVER",
            True,
            DARK_PINK
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 130
                )
            )
        )


        #WINNER SHADOW

        winner_shadow = winner_font.render(
            winner,
            True,
            SHADOW_PINK
        )

        screen.blit(
            winner_shadow,
            winner_shadow.get_rect(
                center=(
                    WIDTH // 2 + 3,
                    HEIGHT // 2 - 67
                )
            )
        )


        #WINNER TEXT

        winner_text = winner_font.render(
            winner,
            True,
            WHITE
        )

        screen.blit(
            winner_text,
            winner_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 70
                )
            )
        )


        #BUTTONS

        draw_button(
            play_again_button,
            "Play Again",
            menu_font
        )

        draw_button(
            main_menu_button,
            "Main Menu",
            menu_font
        )


    #LIVES

    # Show hearts while playing
    if (
        current_screen == "single"
        or current_screen == "multiplayer"
    ):

        # Left side hearts
        draw_hearts(
            left_lives,
            WIDTH // 4
        )

        # Right side hearts
        draw_hearts(
            right_lives,
            WIDTH * 3 // 4
        )


    #PAUSE MESSAGE

    # Show Get Ready after someone loses a life
    if round_paused and (
        current_screen == "single"
        or current_screen == "multiplayer"
    ):

        ready_text = menu_font.render(
            "Get Ready!",
            True,
            DARK_PINK
        )

        screen.blit(
            ready_text,
            ready_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2
                )
            )
        )


    #START MESSAGE

    # Singleplayer start instructions
    if not game_started and current_screen == "single":

        start_text = small_font.render(
            "Press W or S to start",
            True,
            DARK_PINK
        )

        screen.blit(
            start_text,
            start_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT - 40
                )
            )
        )


    # Multiplayer start instructions
    if not game_started and current_screen == "multiplayer":

        start_text = small_font.render(
            "Press W, S or an arrow key to start",
            True,
            DARK_PINK
        )

        screen.blit(
            start_text,
            start_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT - 40
                )
            )
        )


    #BACK BUTTON

    # Show Back only before the match starts
    if (
        current_screen == "single"
        or current_screen == "multiplayer"
    ) and not game_started:

        draw_button(
            back_button,
            "Back",
            small_font
        )


    # Limit the game to 60 frames per second
    clock.tick(FPS)

    # Update everything drawn on the screen
    pygame.display.update()


pygame.quit()