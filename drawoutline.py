import cv2
import turtle
import urllib.request
import numpy as np

# 1. Fetch image directly from online URL with browser headers
url = 'https://img.freepik.com/premium-photo/lord-ganesha-full-hd-high-resolution-with-lighting_849906-13194.jpg?w=2000'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
arr = np.asarray(bytearray(response.read()), dtype=np.uint8)

# 2. Decode into grayscale
img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)

# 3. Resize to fit the screen
width, height = 600, 600
img = cv2.resize(img, (width, height))

# 4. Smooth image and detect outlines
blurred = cv2.GaussianBlur(img, (3, 3), 0)
edges = cv2.Canny(blurred, 30, 90)

# 5. Extract contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 6. Turtle setup
t = turtle.Turtle()
t.speed(0)
t.pensize(1)
t.pencolor("black")

screen = turtle.Screen()
screen.setup(width=width + 50, height=height + 50)
screen.title("Lord Ganesha Drawing")
screen.tracer(2)

# 7. Draw outlines
min_length = 5
for contour in contours:
    if len(contour) < min_length:
        continue
    t.penup()
    for i, point in enumerate(contour):
        x = point[0][0] - (width // 2)
        y = (height // 2) - point[0][1]
        t.goto(x, y)
        if i == 0:
            t.pendown()

screen.update()
turtle.done()