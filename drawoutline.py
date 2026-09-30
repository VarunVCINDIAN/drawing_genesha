import cv2
import turtle
import urllib.request
import numpy as np

# Helper function to prompt the user and handle defaults
def get_user_input(prompt_msg, default_value, is_number=True):
    # Ask the user, showing the default value in brackets
    user_input = input(f"{prompt_msg} [Default: {default_value}]: ").strip()
    
    # If the user just pressed Enter, return the default
    if not user_input:
        return default_value
        
    # If a number is expected, try to convert it
    if is_number:
        try:
            return int(user_input)
        except ValueError:
            print(f"  -> Invalid number. Using default: {default_value}")
            return default_value
            
    return user_input

print("=== Python Turtle Image Drawer ===")
print("Type your desired value and press ENTER. To use the default, just press ENTER.\n")

# 1. Collect values at runtime with prompts and defaults
default_url = 'https://img.freepik.com/premium-photo/lord-ganesha-full-hd-high-resolution-with-lighting_849906-13194.jpg?w=2000'

url = get_user_input("1. Enter image URL", default_url, is_number=False)
blur_val = get_user_input("2. Enter blur level (odd number like 3, 5, 7)", 3)
lower_thresh = get_user_input("3. Enter lower detail threshold", 30)
upper_thresh = get_user_input("4. Enter upper detail threshold", 90)
min_length = get_user_input("5. Enter minimum line length", 5)

print("\nDownloading and processing image...")

# 2. Fetch image directly from online URL
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
arr = np.asarray(bytearray(response.read()), dtype=np.uint8)

# 3. Decode into grayscale
img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)

# 4. Resize to fit the screen
width, height = 600, 600
img = cv2.resize(img, (width, height))

# 5. Smooth image and detect outlines using user inputs
blurred = cv2.GaussianBlur(img, (blur_val, blur_val), 0)
edges = cv2.Canny(blurred, lower_thresh, upper_thresh)

# 6. Extract contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 7. Turtle setup
t = turtle.Turtle()
t.speed(0)
t.pensize(1)
t.pencolor("black")

screen = turtle.Screen()
screen.setup(width=width + 50, height=height + 50)
screen.title("Interactive Image Drawing")
screen.tracer(2)

# 8. Draw outlines using user input for line length
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