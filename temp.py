import math

def generate_orientations(n=10):
    """Generates n Euler coordinates representing orientations on a hemisphere"""
    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

    for i in range(n):
        y = 1 - (i / float(n - 1))  # y goes from 1 to 0
        radius = math.sqrt(1 - y*y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius

        pitch = math.acos(z)  # convert to spherical coordinates
        yaw = math.atan2(y, x)
        roll = 0  # roll is not used for orientations on a hemisphere

        points.append((pitch, yaw, roll))

    return points

orientations = generate_orientations()
for orientation in orientations:
    print(orientation)