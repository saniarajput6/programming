import tkinter as tk
import random

width = 600
height = 400
size = 20
speed = 120

snake = [(100, 100), (80, 100), (60, 100)]
direction = "Right"

score = 0
high_score = 0
food = None
game_status = "running"
after_id = None

root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

score_label = tk.Label(root, text="Score: 0 | High Score: 0",
                       font=("Arial", 13, "bold"))
score_label.pack(pady=5)

status_label = tk.Label(root, text="Game Running",
                        font=("Arial", 10))
status_label.pack()

canvas = tk.Canvas(root, width=width, height=height, bg="black")
canvas.pack(padx=10, pady=10)


def create_food():
    global food

    while True:
        x = random.randrange(0, width, size)
        y = random.randrange(0, height, size)

        if (x, y) not in snake:
            food = (x, y)
            break


def change_direction(event):
    global direction

    new_direction = event.keysym

    if new_direction == "Up" and direction != "Down":
        direction = "Up"
    elif new_direction == "Down" and direction != "Up":
        direction = "Down"
    elif new_direction == "Left" and direction != "Right":
        direction = "Left"
    elif new_direction == "Right" and direction != "Left":
        direction = "Right"


def draw_game():
    canvas.delete("all")

    canvas.create_oval(
        food[0], food[1],
        food[0] + size, food[1] + size,
        fill="red"
    )

    for i, part in enumerate(snake):
        x, y = part

        if i == 0:
            colour = "lime green"
        else:
            colour = "green"

        canvas.create_rectangle(
            x, y, x + size, y + size,
            fill=colour, outline="black"
        )


def move_snake():
    global snake, score, high_score, speed
    global game_status, after_id

    if game_status == "running":
        x, y = snake[0]

        if direction == "Up":
            y -= size
        elif direction == "Down":
            y += size
        elif direction == "Left":
            x -= size
        elif direction == "Right":
            x += size

        new_head = (x, y)

        if new_head == food:
            snake.insert(0, new_head)
            score += 10

            if score > high_score:
                high_score = score

            speed = max(50, speed - 5)
            create_food()

        else:
            snake.insert(0, new_head)
            snake.pop()

        if (x < 0 or x >= width or y < 0 or y >= height
                or new_head in snake[1:]):
            game_status = "over"
            status_label.config(text="GAME OVER!")
            draw_game()
            canvas.create_text(
                width // 2, height // 2,
                text="GAME OVER",
                fill="red",
                font=("Arial", 28, "bold")
            )
            return

        score_label.config(
            text=f"Score: {score} | High Score: {high_score}"
        )

        draw_game()

    if game_status != "over":
        after_id = root.after(speed, move_snake)


def pause_game(event=None):
    global game_status

    if game_status == "running":
        game_status = "paused"
        status_label.config(text="Paused - Press SPACE to continue")

    elif game_status == "paused":
        game_status = "running"
        status_label.config(text="Game Running")


def restart_game():
    global snake, direction, score, speed
    global game_status, food, after_id

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "Right"
    score = 0
    speed = 120
    game_status = "running"

    score_label.config(
        text=f"Score: {score} | High Score: {high_score}"
    )

    status_label.config(text="Game Running")

    create_food()
    draw_game()
    move_snake()


root.bind("<KeyPress>", change_direction)
root.bind("<space>", pause_game)

restart_button = tk.Button(
    root,
    text="Restart Game",
    command=restart_game
)
restart_button.pack(pady=5)

restart_game()

root.mainloop()