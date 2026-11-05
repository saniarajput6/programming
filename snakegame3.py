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

score_label = tk.Label(
    root, text="Score: 0 | High Score: 0",
    font=("Arial", 13, "bold")
)
score_label.pack(pady=5)

status_label = tk.Label(root, text="Game Running")
status_label.pack()

canvas = tk.Canvas(
    root, width=width, height=height,
    bg="#17251d", highlightthickness=0
)
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


def draw_game(parts=None):
    canvas.delete("all")

    canvas.create_oval(
        food[0] + 3, food[1] + 3,
        food[0] + size - 3, food[1] + size - 3,
        fill="#ff4444", outline="#ffaaaa", width=2
    )

    if parts is None:
        parts = snake

    for i, part in enumerate(parts):
        x, y = part

        if i == 0:
            colour = "#a6ff4d"
        else:
            colour = "#43c96b"

        canvas.create_rectangle(
            x + 1, y + 1,
            x + size - 1, y + size - 1,
            fill=colour, outline="#17251d"
        )

    # Snake's eyes
    x, y = parts[0]

    if direction == "Right":
        eyes = [(x + 14, y + 5), (x + 14, y + 14)]
    elif direction == "Left":
        eyes = [(x + 5, y + 5), (x + 5, y + 14)]
    elif direction == "Up":
        eyes = [(x + 5, y + 5), (x + 14, y + 5)]
    else:
        eyes = [(x + 5, y + 14), (x + 14, y + 14)]

    for eye in eyes:
        canvas.create_oval(
            eye[0] - 2, eye[1] - 2,
            eye[0] + 2, eye[1] + 2,
            fill="black"
        )


def animate_snake(old_parts, new_parts, frame=0):
    global after_id

    if game_status == "over":
        return

    if game_status == "paused":
        after_id = root.after(
            20, animate_snake, old_parts, new_parts, frame
        )
        return

    frames = 6
    moving_parts = []

    for i in range(len(new_parts)):
        if i < len(old_parts):
            start_x, start_y = old_parts[i]
        else:
            start_x, start_y = old_parts[-1]

        end_x, end_y = new_parts[i]

        x = start_x + (end_x - start_x) * frame / frames
        y = start_y + (end_y - start_y) * frame / frames

        moving_parts.append((x, y))

    draw_game(moving_parts)

    if frame < frames:
        after_id = root.after(
            20, animate_snake,
            old_parts, new_parts, frame + 1
        )
    else:
        after_id = root.after(1, move_snake)


def move_snake():
    global snake, score, high_score
    global game_status, after_id

    after_id = None

    if game_status != "running":
        return

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
    eating = new_head == food

    if eating:
        body = snake
    else:
        body = snake[:-1]

    if (x < 0 or x >= width or y < 0 or y >= height
            or new_head in body):

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

    old_snake = snake.copy()

    snake.insert(0, new_head)

    if eating:
        score += 10

        if score > high_score:
            high_score = score

        create_food()
    else:
        snake.pop()

    score_label.config(
        text=f"Score: {score} | High Score: {high_score}"
    )

    animate_snake(old_snake, snake.copy())


def pause_game(event=None):
    global game_status

    if game_status == "running":
        game_status = "paused"
        status_label.config(text="Paused - Press SPACE to continue")

    elif game_status == "paused":
        game_status = "running"
        status_label.config(text="Game Running")


def restart_game():
    global snake, direction, score
    global game_status, food, after_id

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "Right"
    score = 0
    game_status = "running"

    score_label.config(
        text=f"Score: {score} | High Score: {high_score}"
    )

    status_label.config(text="Game Running")

    create_food()
    draw_game()

    after_id = root.after(speed, move_snake)


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