import tkinter as tk
import random

# Game settings
WIDTH = 600
HEIGHT = 400
SIZE = 20
SPEED = 120

snake = [(100, 100), (80, 100), (60, 100)]
direction = "Right"

score = 0
high_score = 0
game_speed = SPEED
game_status = "running"
food = None


# Create game window
root = tk.Tk()
root.title("Snake Game - Version 2.0")
root.resizable(False, False)

score_label = tk.Label(root, text="Score: 0 | High Score: 0",
                       font=("Arial", 14, "bold"))
score_label.pack(pady=5)

status_label = tk.Label(root, text="Game Running",
                        font=("Arial", 11))
status_label.pack()

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack(padx=10, pady=10)


# Generate food
def create_food():

    global food

    while True:
        x = random.randrange(0, WIDTH, SIZE)
        y = random.randrange(0, HEIGHT, SIZE)

        if (x, y) not in snake:
            food = (x, y)
            break


# Change direction
def change_direction(event):

    global direction

    opposites = {
        "Up": "Down",
        "Down": "Up",
        "Left": "Right",
        "Right": "Left"
    }

    new_direction = event.keysym

    if new_direction in opposites:
        if new_direction != opposites[direction]:
            direction = new_direction


# Move snake
def move_snake():

    global snake, score, high_score
    global game_speed, game_status

    if game_status == "running":

        x, y = snake[0]

        if direction == "Up":
            y -= SIZE
        elif direction == "Down":
            y += SIZE
        elif direction == "Left":
            x -= SIZE
        elif direction == "Right":
            x += SIZE

        new_head = (x, y)

        eating = new_head == food

        body = snake if eating else snake[:-1]

        # Check collisions
        if (x < 0 or x >= WIDTH or
                y < 0 or y >= HEIGHT or
                new_head in body):

            game_status = "game_over"
            status_label.config(text="GAME OVER!")
            draw_game()

            canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                text="GAME OVER",
                fill="red",
                font=("Arial", 28, "bold")
            )

            return

        snake.insert(0, new_head)

        if eating:

            score += 10
            high_score = max(score, high_score)

            # Increase difficulty
            game_speed = max(50, game_speed - 5)

            create_food()

        else:
            snake.pop()

        score_label.config(
            text=f"Score: {score} | High Score: {high_score}"
        )

        draw_game()

    if game_status != "game_over":
        root.after(game_speed, move_snake)


# Draw game objects
def draw_game():

    canvas.delete("all")

    # Draw food
    canvas.create_oval(
        food[0], food[1],
        food[0] + SIZE, food[1] + SIZE,
        fill="red"
    )

    # Draw snake
    for index, (x, y) in enumerate(snake):

        colour = "lime green" if index == 0 else "green"

        canvas.create_rectangle(
            x, y, x + SIZE, y + SIZE,
            fill=colour,
            outline="black"
        )


# Pause and resume
def pause_game(event=None):

    global game_status

    if game_status == "running":
        game_status = "paused"
        status_label.config(text="PAUSED - Press SPACE to resume")

    elif game_status == "paused":
        game_status = "running"
        status_label.config(text="Game Running")


# Restart game
def restart_game():

    global snake, direction, score
    global game_speed, game_status, food

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "Right"

    score = 0
    game_speed = SPEED
    game_status = "running"

    score_label.config(
        text=f"Score: {score} | High Score: {high_score}"
    )

    status_label.config(text="Game Running")

    create_food()
    draw_game()

    move_snake()


# Keyboard controls
root.bind("<KeyPress>", change_direction)
root.bind("<space>", pause_game)


# Restart button
tk.Button(
    root,
    text="RESTART GAME",
    command=restart_game,
    font=("Arial", 11, "bold")
).pack(pady=5)


# Start application
restart_game()

root.mainloop()