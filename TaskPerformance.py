# Instructions:
# Move the turtle left or right using the arrow keys (Left, Right).
# The goal is to avoid falling shapes (obstacles: square, triangle, circle). If the turtle collides with an obstacle, it loses 1 health.
# The turtle starts with 3 health. If health reaches 0 or the timer reaches 0, the game ends.
# There are multiple falling obstacles of different shapes. When they hit the bottom of the screen or the turtle,
# they disappear and reappear at the top as a new random shape.

import turtle
import random
import time

# Setup screen
screen = turtle.Screen()
screen.title("Turtle Sideways Movement Avoidance Game")
screen.bgcolor("lightblue")
screen.setup(width=600, height=600)
screen.tracer(0)  # Disable automatic screen updates for smoother animations

# Create the player turtle
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.penup()
player.goto(0, -250)  # Centered horizontally, at the bottom of the screen

# Player's health
health = 3

# Create health display turtle (aligned to top-left)
health_display = turtle.Turtle()
health_display.penup()
health_display.hideturtle()
health_display.goto(-280, 260)
health_display.write(f"Health: {health}", align="left", font=("Arial", 16, "normal"))

# Create timer display turtle (aligned to top-right)
timer_display = turtle.Turtle()
timer_display.penup()
timer_display.hideturtle()
timer_display.goto(200, 260)

# Timer countdown
time_left = 60  # Start with 60 seconds

# List of possible obstacle shapes
shapes = ["square", "triangle", "circle"]

# Create multiple falling obstacles with random shapes
num_obstacles = 5  # Number of obstacles
obstacles = []

for _ in range(num_obstacles):
    obstacle = turtle.Turtle()
    obstacle.shape(random.choice(shapes))  # Random shape
    obstacle.color(random.choice(["red", "blue", "yellow"]))  # Random color
    obstacle.penup()
    obstacle.goto(random.randint(-280, 280), random.randint(100, 300))
    obstacles.append(obstacle)

# Move functions (player only moves left and right)
def move_left():
    x = player.xcor()
    if x > -280:
        player.setx(x - 30)

def move_right():
    x = player.xcor()
    if x < 280:
        player.setx(x + 30)

# Keyboard bindings
screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

# Update health display
def update_health_display():
    health_display.clear()
    health_display.write(f"Health: {health}", align="left", font=("Arial", 16, "normal"))

# Blink effect after collision
def blink_player():
    for _ in range(6):  # Blink 3 times (on/off)
        player.hideturtle()
        screen.update()
        time.sleep(0.1)
        player.showturtle()
        screen.update()
        time.sleep(0.1)

# Check for collision with any obstacle
def check_collision():
    global health
    for obstacle in obstacles:
        if player.distance(obstacle) < 20:  # If collision occurs
            health -= 1
            update_health_display()
            blink_player()  # Trigger the blink effect when damaged
            reset_obstacle(obstacle)
            if health <= 0:
                return False
    return True

# Reset an obstacle to the top with a new random shape and position
def reset_obstacle(obstacle):
    obstacle.shape(random.choice(shapes))  # Random shape
    obstacle.color(random.choice(["red", "blue", "yellow"]))  # Random color
    obstacle.goto(random.randint(-280, 280), 280)

# Move obstacles downward smoothly
def move_obstacles():
    for obstacle in obstacles:
        y = obstacle.ycor()
        y -= random.uniform(2, 4)  # Move the obstacle down at a random speed
        obstacle.sety(y)
        if y < -300:  # If the obstacle goes off-screen, reset it
            reset_obstacle(obstacle)

# Update timer display
def update_timer_display():
    timer_display.clear()
    timer_display.write(f"Time: {time_left}s", align="right", font=("Arial", 16, "normal"))

# Main game loop
game_running = True
last_time = time.time()

update_timer_display()  # Initial timer display

while health > 0 and time_left > 0 and game_running:
    screen.update()  # Manually update the screen for smoother animations
    move_obstacles()
    game_running = check_collision()

    # Timer countdown
    current_time = time.time()
    if current_time - last_time >= 1:  # Reduce time by 1 every second
        time_left -= 1
        update_timer_display()
        last_time = current_time

    time.sleep(0.02)  # Adjust the delay to control the speed of the game

# Game over screen
player.goto(0, 0)
if health <= 0:
    player.write("Game Over! Out of Health", align="center", font=("Arial", 24, "normal"))
elif time_left <= 0:
    player.write("Game Over! Time's Up", align="center", font=("Arial", 24, "normal"))

screen.update()
screen.mainloop()
