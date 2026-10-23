import tkinter as tk

# Window dimensions
WIDTH = 1000
HEIGHT = 600

root = tk.Tk()
root.title("Experiment 1 - DDA and Bresenham Line Drawing")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()


# Plot a single pixel
def plot_pixel(x, y, offset_x, origin_y, color):
    canvas.create_rectangle(
        offset_x + x, origin_y - y,
        offset_x + x + 3, origin_y - y + 3,
        fill=color, outline=color
    )


# DDA Line Drawing Algorithm
def dda(x1, y1, x2, y2, offset_x, origin_y, color):
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    if steps == 0:
        plot_pixel(x1, y1, offset_x, origin_y, color)
        return

    x_increment = dx / steps
    y_increment = dy / steps

    x = x1
    y = y1

    for _ in range(steps + 1):
        plot_pixel(round(x), round(y), offset_x, origin_y, color)
        x += x_increment
        y += y_increment


# Bresenham's Line Drawing Algorithm
def bresenham(x1, y1, x2, y2, offset_x, origin_y, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    error = dx - dy

    while True:
        plot_pixel(x1, y1, offset_x, origin_y, color)

        if x1 == x2 and y1 == y2:
            break

        error2 = 2 * error

        if error2 > -dy:
            error -= dy
            x1 += sx

        if error2 < dx:
            error += dx
            y1 += sy


# Display headings
canvas.create_text(
    250, 35, text="DDA Algorithm",
    font=("Arial", 18, "bold"), fill="blue"
)

canvas.create_text(
    750, 35, text="Bresenham Algorithm",
    font=("Arial", 18, "bold"), fill="red"
)

# Draw a separator
canvas.create_line(500, 60, 500, 550, fill="gray", width=2)

# Draw lines using both algorithms
dda(50, 50, 300, 400, 70, 520, "blue")

bresenham(50, 50, 300, 400, 570, 520, "red")

# Display endpoint information
canvas.create_text(
    250, 560, text="Line: (50, 50) to (300, 400)",
    font=("Arial", 11)
)

canvas.create_text(
    750, 560, text="Line: (50, 50) to (300, 400)",
    font=("Arial", 11)
)

root.mainloop()