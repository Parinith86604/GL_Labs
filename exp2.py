import matplotlib.pyplot as plt


def midpoint_circle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r
    points = set()

    while x <= y:
        # Eight-way symmetry
        points.update([
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        ])

        if p < 0:
            p += 2 * x + 3
        else:
            p += 2 * (x - y) + 5
            y -= 1

        x += 1

    return points


# Main program
xc = int(input("Enter center X coordinate: "))
yc = int(input("Enter center Y coordinate: "))
r = int(input("Enter radius: "))

if r <= 0:
    print("Radius must be a positive integer.")
else:
    points = midpoint_circle(xc, yc, r)

    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    plt.figure(figsize=(7, 7))
    plt.scatter(x_values, y_values, color="blue", marker="s", s=30)

    plt.title("Midpoint Circle Drawing Algorithm")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.axis("equal")
    plt.show()