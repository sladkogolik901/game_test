import turtle
import math
import keyboard
import random
import time

# Initial settings
screen = turtle.Screen()
cursor = turtle.Turtle()
gun = turtle.Turtle()
bullet = turtle.Turtle()
circles_list = []
widht_screen = 0
height_screen = 0


def init_set():
    # Set screensize
    turtle.screensize(330, 230)
    turtle.setup(350, 250)
    global widht_screen
    widht_screen = screen.screensize()[0]
    global height_screen
    height_screen = screen.screensize()[1]
    # Cursor
    cursor.penup()
    cursor.speed(0)
    # Gun
    gun.penup()
    gun.color('green')
    # Fire
#    bullet.shape('circle')
    bullet.color('red')
    bullet.penup()
    bullet.speed(3)



def canplace(x, y, r):
    for item in circles_list:
        x1 = item[0]
        y1 = item[1]
        r1 = item[2]*10.5
        x2 = x1 - x
        y2 = y1 - y
        d = math.sqrt(x2**2 + y2**2)
        if d < (r*10.5 + r1):
            return False
    return True


def create_gun():
    x = random.randint(-widht_screen/2, widht_screen/2)
    y = random.randint(-height_screen/2, height_screen/2)
    gun.setpos(x, y)
    gun.shape("turtle")


def rotate_gun(curx, cury, gunx, guny):
    diffx = curx - gunx
    diffy = cury - guny
    radianl = math.atan2(diffy, diffx)
    degreesl = radianl* 180/math.pi
    gun.settiltangle(degreesl)


def fire(step):
    bullet.forward(step)
    if bullet.xcor() <= -widht_screen/2 - 1:
        bullet.setx(gun.xcor())
    if bullet.xcor() >= widht_screen/2:
        bullet.setx(gun.xcor())
    if bullet.ycor() >= height_screen/2:
        bullet.sety(gun.ycor())
    if bullet.ycor() <= -height_screen/2 - 1:
        bullet.sety(gun.ycor())


def create_circles(n):
    i = 0
    while i < n:
        x = random.randint(-widht_screen/2, widht_screen/2)
        y = random.randint(-height_screen/2, height_screen/2)
        radius = random.randint(1, 3)
        while not canplace(x, y, radius):
            x = random.randint(-widht_screen / 2, widht_screen / 2)
            y = random.randint(-height_screen / 2, height_screen / 2)
            radius = random.randint(1, 3)
        data = (x, y, radius)
        circles_list.append(data)
        cursor.setx(x)
        cursor.sety(y)
        cursor.shape("circle")
        cursor.shapesize(radius)
        cursor.stamp()
        cursor.shapesize(1)
        i += 1


def can_go(step):
    degrees = cursor.heading()
    radians = degrees * math.pi/180
    x2 = step * math.cos(radians) + cursor.xcor()
    y2 = step * math.sin(radians) + cursor.ycor()
    #f_cursor.setpos(x2, y2)
    for item in circles_list:
        x1 = item[0]
        y1 = item[1]
        r = item[2]*10.5
        x = x2 - x1
        y = y2 - y1
        r_next = math.sqrt(x**2+y**2)
        if r_next < r:
            return False
    return True

def move_forward(step):
    if can_go(step):
        cursor.forward(step)
        if cursor.ycor() >= height_screen/2:
            cursor.sety(-height_screen/2)
        if cursor.ycor() <= -height_screen/2 - 1:
            cursor.sety(height_screen/2)
        if cursor.xcor() >= widht_screen/2:
            cursor.setx(-widht_screen/2)
        if cursor.xcor() <= -widht_screen/2 - 1:
            cursor.setx(widht_screen/2)
#    return cursor.xcor(), cursor.ycor()


def move_left(step):
    cursor.left(step)


def move_right(step):
    cursor.right(step)

init_set()
create_circles(5)
create_gun()
cursor.shape('classic')
cursor.setpos(0, 0)
bullet.setpos(gun.xcor(), gun.ycor())



keyboard.add_hotkey('up', move_forward, args=[15])
keyboard.add_hotkey('down', move_forward, args=[-15])
keyboard.add_hotkey('left', move_left, args=[15])
keyboard.add_hotkey('right', move_right, args=[15])


def mainloop():
    rotate_gun(cursor.xcor(), cursor.ycor(), gun.xcor(), gun.ycor())
    m_angle = gun.tiltangle()
    bullet.tiltangle(-m_angle)
    bullet.setheading(m_angle)
    fire(4)
    screen.ontimer(mainloop, 33)
    #turtle.mainloop()


screen.ontimer(mainloop, 33)
turtle.exitonclick()
