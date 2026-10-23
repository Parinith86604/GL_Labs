import numpy as np
import matplotlib.pyplot as plt

# Define a 2D object using homogeneous coordinates
# Triangle vertices: (x, y, 1)
object_points = np.array([
    [1, 1, 1],
    [4, 1, 1],
    [2.5, 4, 1],
    [1, 1, 1]
]).T


# Transformation functions
def translation(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])


def rotation(angle):
    theta = np.radians(angle)
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])


def scaling(sx, sy):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])


def reflection_x():
    return np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])


def shearing(shx, shy):
    return np.array([
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ])


# Apply transformation to the object
def transform_object(points, matrix):
    return matrix @ points


# Plot original and transformed objects
def plot_objects(original, transformed, title):
    plt.figure(figsize=(7, 6))

    plt.plot(
        original[0], original[1],
        'bo-', linewidth=2, label="Original Object"
    )

    plt.plot(
        transformed[0], transformed[1],
        'ro-', linewidth=2, label="Transformed Object"
    )

    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.grid(True)
    plt.legend()
    plt.title(title)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.axis("equal")
    plt.show()


# Display transformation menu
while True:
    print("\n--- 2D TRANSFORMATIONS USING HOMOGENEOUS COORDINATES ---")
    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. Reflection about X-axis")
    print("5. Reflection about Y-axis")
    print("6. Shearing")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        tx = float(input("Enter translation along X: "))
        ty = float(input("Enter translation along Y: "))
        matrix = translation(tx, ty)
        title = "2D Translation"

    elif choice == '2':
        angle = float(input("Enter rotation angle in degrees: "))
        matrix = rotation(angle)
        title = "2D Rotation"

    elif choice == '3':
        sx = float(input("Enter scaling factor along X: "))
        sy = float(input("Enter scaling factor along Y: "))
        matrix = scaling(sx, sy)
        title = "2D Scaling"

    elif choice == '4':
        matrix = reflection_x()
        title = "Reflection about X-axis"

    elif choice == '5':
        matrix = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        title = "Reflection about Y-axis"

    elif choice == '6':
        shx = float(input("Enter X-shear factor: "))
        shy = float(input("Enter Y-shear factor: "))
        matrix = shearing(shx, shy)
        title = "2D Shearing"

    elif choice == '7':
        print("Program terminated.")
        break

    else:
        print("Invalid choice. Try again.")
        continue

    transformed_points = transform_object(object_points, matrix)

    print("\nTransformation Matrix:")
    print(matrix)

    print("\nTransformed Coordinates:")
    print(np.round(transformed_points.T, 2))

    plot_objects(object_points, transformed_points, title)