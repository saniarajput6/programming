import tkinter as tk
import random

# Game settings
WIDTH = 600
HEIGHT = 400
SIZE = 20
SPEED = 120

score = 0
direction = "Right"
game_over = False

snake = [(100, 100), (80, 100), (60, 100)]
food = None


# Create game window
root = tk.Tk()
root.title("Snake Game")

score_label = tk.Label(root, text="Score: 0", font=("Arial", 16, "bold"))
score_label.pack()

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()


# Generate food
def create_food():

    global food

    while True:
        x = random.randrange(0, WIDTH, SIZE)
        y = random.randrange(0, HEIGHT, SIZE)

        if (x, y) not in snake:
            food = (x, y)
            break

    canvas.create_oval(
        food[0], food[1],
        food[0] + SIZE, food[1] + SIZE,
        fill="red"
    )


# Change snake direction
def change_direction(event):

    global direction

    new_direction = event.keysym

    opposites = {
        "Up": "Down",
        "Down": "Up",
        "Left": "Right",
        "Right": "Left"
    }

    if new_direction in opposites:
        if new_direction != opposites[direction]:
            direction = new_direction


# Move the snake
def move_snake():

    global snake, score, game_over

    if game_over:
        return

    head_x, head_y = snake[0]

    if direction == "Up":
        head_y -= SIZE
    elif direction == "Down":
        head_y += SIZE
    elif direction == "Left":
        head_x -= SIZE
    elif direction == "Right":
        head_x += SIZE

    new_head = (head_x, head_y)

    eating = new_head == food

    # Check collision with walls
    if (head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT):
        end_game()
        return

    # Check collision with itself
    body = snake if eating else snake[:-1]

    if new_head in body:
        end_game()
        return

    snake.insert(0, new_head)

    if eating:
        score += 10
        score_label.config(text=f"Score: {score}")
        create_food()
    else:
        snake.pop()

    draw_game()

    root.after(SPEED, move_snake)


# Draw the game
def draw_game():

    canvas.delete("all")

    for x, y in snake:
        canvas.create_rectangle(
            x, y, x + SIZE, y + SIZE,
            fill="lime green",
            outline="black"
        )

    if food:
        canvas.create_oval(
            food[0], food[1],
            food[0] + SIZE, food[1] + SIZE,
            fill="red"
        )


# End game
def end_game():

    global game_over

    game_over = True

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="GAME OVER",
        fill="white",
        font=("Arial", 28, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 40,
        text="Press RESTART to play again",
        fill="yellow",
        font=("Arial", 13)
    )


# Restart game
def restart_game():

    global snake, direction, score, game_over, food

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "Right"
    score = 0
    game_over = False
    food = None

    score_label.config(text="Score: 0")

    create_food()
    draw_game()

    move_snake()


# Controls
root.bind("<KeyPress>", change_direction)

restart_button = tk.Button(
    root,
    text="RESTART",
    command=restart_game
)
restart_button.pack(pady=10)


# Start game
restart_game()

root.mainloop()