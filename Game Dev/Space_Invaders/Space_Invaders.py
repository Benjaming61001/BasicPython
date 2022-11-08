# Space Invaders
import turtle
import os
import math
import random
import winsound
import platform
import pygame
from pygame import mixer 

#Background Sound
pygame.mixer.init()
mixer.music.load("D:/BasicPython/Space_Invaders/EV_HeavyRain01.wav")
mixer.music.play(-1) 

# Setup Screen
wn = turtle.Screen()
wn.bgcolor("Black")
wn.title("Space Invaders")
wn.bgpic("D:/BasicPython/Space_Invaders/bg.gif")
wn.tracer(10)

# Register the shapes
wn.register_shape("D:/BasicPython/Space_Invaders/SpaceInvader_Player.gif")
wn.register_shape("D:/BasicPython/Space_Invaders/SpaceInvader_Enemy.gif")

# Draw the border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set Score to 0
score = 0
# Draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Game state
win = False
exit = False

# Draw Exit
Exit_pen = turtle.Turtle()
Exit_pen.speed(0)
Exit_pen.color("white")
Exit_pen.penup()
Exit_pen.setposition(290, -290)
Exit_string = "Press 0 to Exit"
Exit_pen.write(Exit_string, False, align="right", font=("Arial", 14, "normal"))
Exit_pen.hideturtle()

# Create Player
player = turtle.Turtle()
player.shape("D:/BasicPython/Space_Invaders/SpaceInvader_Player.gif")
player.penup()
player.speed(0)
player.setposition(0, -225)
player.setheading(90)
player.speed = 1

# Choose a number of enemies
number_of_enemies = 4
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create enemies
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 200
enemy_number = 0
enemy_remain = number_of_enemies

for enemy in enemies:
    enemy.shape("D:/BasicPython/Space_Invaders/SpaceInvader_Enemy.gif")
    enemy.penup()
    enemy.speed(9)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setposition(x, y)
    enemy.speed(0)
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

# Base speed
enemyspeed = 0.1
base_speed = enemyspeed 
# Multiply speed
enemy_speed = 1.0
step = 5
min_speed = enemy_speed
max_speed = enemy_speed*2.5
speed_per_step = max_speed/step

# Draw Enemy Speed
enemy_speed_pen = turtle.Turtle()
enemy_speed_pen.speed(0)
enemy_speed_pen.color("white")
enemy_speed_pen.penup()
enemy_speed_pen.setposition(290, 280)
enemy_speed_string = "Enemies Speed: {}".format(enemy_speed)
enemy_speed_pen.write(enemy_speed_string, False, align="right", font=("Arial", 14, "normal"))
enemy_speed_pen.hideturtle()

# Draw Enemy Remain
enemy_remain_pen = turtle.Turtle()
enemy_remain_pen.speed(0)
enemy_remain_pen.color("white")
enemy_remain_pen.penup()
enemy_remain_pen.setposition(0, 280)
enemy_remain_string = "Enemies remain: {}".format(enemy_remain)
enemy_remain_pen.write(enemy_remain_string, False, align="center", font=("Arial", 14, "normal"))
enemy_remain_pen.hideturtle()

# Player's Bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.hideturtle()
bullet.setposition(0, -300)
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
# Set bullet speed
bulletspeed = 2.5

# Define bullet state
# Ready - Ready to fire
# Fire - Bullet is firing
bulletstate = "Ready"

# Player actions
def move_left():
    player.speed = -1

def move_right():
    player.speed = 1

def move_player():
    x = player.xcor()
    x += player.speed
    if x < -270:
        player.speed *= -1
    if x > 270:
        player.speed *= -1
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate == "Ready":
        Play_Sound("D:/BasicPython/Space_Invaders/blaster-firing.wav")
        bulletstate = "Fire"
        x = player.xcor()
        y = player.ycor() +10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1 ,t2):
    distance = t1.distance(t2)
    if distance < 20:
        Play_Sound("D:/BasicPython/Space_Invaders/explosion.wav")
        return True
    else :
        return False

def Play_Sound(sound_file, time = 0):
    #Windows
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    #Linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    #Mac
    else:
        os.system("aplay {}&".format(sound_file))

def incEnemyspd():
    global enemy_speed
    if enemy_speed < max_speed:
        enemy_speed += speed_per_step
        if enemy_speed > max_speed:
            enemy_speed = max_speed
    
def decEnemyspd():
    global enemy_speed
    if enemy_speed > min_speed:
        enemy_speed -= speed_per_step
        if enemy_speed < min_speed:
            enemy_speed = min_speed

def change_enemy_speed():
    global enemyspeed, enemy_speed
    if enemyspeed < 0:
        enemyspeed = (base_speed * enemy_speed) * -1
    else:
        enemyspeed = (base_speed * enemy_speed)
    enemy_speed_string = "Enemies Speed: {}".format(enemy_speed)
    enemy_speed_pen.clear()
    enemy_speed_pen.write(enemy_speed_string, False, align="right", font=("Arial", 14, "normal"))

def Win():
    global exit
    Play_Sound("D:/BasicPython/Space_Invaders/TP_Fanfare_SmallItem.wav")
    win_pen = turtle.Turtle()
    win_pen.speed(0)
    win_pen.color("white")
    win_pen.penup()
    win_pen.setposition(0, -20)
    win_string = "WIN"
    win_pen.write(win_string, False, align="center", font=("Arial", 48, "bold"))
    win_pen.hideturtle()
    print ("WIN")
    exit = True

def game_over(t1):
    global exit
    if t1 != "EXIT":
        t1 = "GAME OVER"
    gameover_pen = turtle.Turtle()
    gameover_pen.speed(0)
    gameover_pen.color("white")
    gameover_pen.penup()
    gameover_pen.setposition(0, -20)
    gameover_string = t1
    gameover_pen.write(gameover_string, False, align="center", font=("Arial", 48, "bold"))
    gameover_pen.hideturtle()
    print (t1)
    Play_Sound("D:/BasicPython/Space_Invaders/SeResourceStd2nd_00000000_00000678.wav")
    exit = True

def Exit():
    global exit
    game_over("EXIT")
    exit = True

# Key binding
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")
wn.onkeypress(incEnemyspd, "+")
wn.onkeypress(decEnemyspd, "-")
wn.onkeypress(Win, "1")
wn.onkeypress(Exit, "0")

# Main game loop
while True:

    wn.update()
    move_player()
    change_enemy_speed()

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += (enemyspeed * enemy_speed)
        enemy.setx(x)

        # Move the enemy Back and Down
        # Hit right border
        if enemy.xcor() > 280:
            for e in enemies:
                y = e.ycor()
                y -= 30
                e.sety(y)
            enemyspeed *= -1
        # Hit left border
        if enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 30
                e.sety(y)
            enemyspeed *= -1

        # Lose condition
        # Enemy touch bottom of the screen
        if enemy.ycor() < -280:
            for e in enemies:
                enemy.hideturtle()
                enemy.setposition(0, 0)
                enemyspeed = 0
            player.hideturtle()
            game_over(0)
            break
        # Enemy touch player
        if isCollision(player, enemy):
            for e in enemies:
                enemy.hideturtle()
                enemy.setposition(0, 0)
                enemyspeed = 0
            player.hideturtle()
            player.speed = 0
            game_over(0)
            break

        # Check Collision between player/bullet/enemy
        if isCollision(bullet, enemy):
            # Reset bullet
            bullet.hideturtle()
            bulletstate = "Ready"
            bullet.setposition(0, -400)
            # Reset enemy       
            enemy.setposition(0, 2000)
            enemy.hideturtle
            # Update score
            score += 10*enemy_speed
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
            # Update enemy remain
            enemy_remain -= 1
            enemy_remain_string = "Enemies remain: {}".format(enemy_remain)
            enemy_remain_pen.clear()
            enemy_remain_pen.write(enemy_remain_string, False, align="center", font=("Arial", 14, "normal"))
            enemy_remain_pen.hideturtle()

        # Win Condition
        if enemy_remain == 0:
            for e in enemies:
                enemy.hideturtle()
                player.hideturtle()
                bullet.hideturtle()
            Win()
            break

    # Move the bullet
    if bulletstate == "Fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "Ready"

    # Exit
    if exit == True:
        break

wn.mainloop()