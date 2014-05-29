#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : project4.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-05-29
'''Implementation of classic arcade game Pong
'''
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

PADDLE_SPEED = 2
KEY_S = simplegui.KEY_MAP["s"]
KEY_W = simplegui.KEY_MAP["w"]
KEY_D = simplegui.KEY_MAP["down"]
KEY_U = simplegui.KEY_MAP["up"]

bling_colors = ["Red", "White"]
bling_times = 8
goal_pausing = False
right_win = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    vx = random.randrange(2, 4)
    vy = random.randrange(1, 3)

    if direction:
        ball_vel = [vx, -vy]
    else:
        ball_vel = [-vx, -vy]

    global game_ready, count_down
    game_ready = True
    count_down = 3
    timer_ready.start()

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    # I use upper-left point to represent the pos of paddle
    paddle1_pos = [0,                 HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH - PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]

    paddle1_vel = paddle2_vel = 0 # down if > 0, up if < 0

    score1 = score2 = 0

    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global goal_pausing, right_win
    _SPEEDUP_RATE = 0.1

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    if goal_pausing:
        if right_win:
            canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, bling_colors[bling_times % 2])
        else:
            canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, bling_colors[bling_times % 2])

    elif game_ready:
        canvas.draw_text(str(count_down), [WIDTH / 2 - 5, HEIGHT / 2 + 5], 24, "Red")

    else:
        ball_pos = map(sum, zip(ball_pos, ball_vel))

        if ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
            if paddle2_pos[1] < ball_pos[1] < paddle2_pos[1] + PAD_HEIGHT:
                ball_vel[0] = -ball_vel[0]
                ball_speedup(_SPEEDUP_RATE)
            else:
                score1 += 1
                goal_pausing = True
                right_win = False
                timer_goal.start()

        if ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
            if paddle1_pos[1] < ball_pos[1] < paddle1_pos[1] + PAD_HEIGHT:
                ball_vel[0] = -ball_vel[0]
                ball_speedup(_SPEEDUP_RATE)
            else:
                score2 += 1
                goal_pausing = True
                right_win = True
                timer_goal.start()

        if not BALL_RADIUS < ball_pos[1] < HEIGHT - BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White")

    # update paddle's vertical position, keep paddle on the screen
    for pos, vel in [(paddle1_pos, paddle1_vel), (paddle2_pos, paddle2_vel)]:

        if pos[1] + vel < 0:
            pos[1] = 0

        elif pos[1] + vel > HEIGHT - PAD_HEIGHT:
            pos[1] = HEIGHT - PAD_HEIGHT

        else:
            pos[1] += vel

    # draw paddles
    draw_paddle(canvas, paddle1_pos)
    draw_paddle(canvas, paddle2_pos)

    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 4, HEIGHT / 4], 32, "White");
    canvas.draw_text(str(score2), [WIDTH * 3 / 4, HEIGHT / 4], 32, "White");

def draw_paddle(canvas, upper_left):
    canvas.draw_polygon([upper_left,
                         [upper_left[0] + PAD_WIDTH, upper_left[1]],
                         [upper_left[0] + PAD_WIDTH, upper_left[1] + PAD_HEIGHT],
                         [upper_left[0],             upper_left[1] + PAD_HEIGHT]
                        ], 2, "White");

def ball_speedup(rate):
    global ball_vel
    ball_vel[0] *= 1 + rate
    ball_vel[1] *= 1 + rate

def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == KEY_S:
        paddle1_vel = PADDLE_SPEED

    elif key == KEY_W:
        paddle1_vel = -PADDLE_SPEED

    elif key == KEY_D:
        paddle2_vel = PADDLE_SPEED

    elif key == KEY_U:
        paddle2_vel = -PADDLE_SPEED

def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == KEY_S or key == KEY_W:
        paddle1_vel = 0

    elif key == KEY_U or key == KEY_D:
        paddle2_vel = 0

def game_begin():
    global count_down, game_ready
    count_down -= 1
    if count_down == 0:
        game_ready = False
        count_down = 3
        timer_ready.stop()

def goal_pause():
    global bling_times, goal_pausing, bling_colors
    bling_times -= 1
    if bling_times == 0:
        goal_pausing = False
        bling_times = 8
        timer_goal.stop()
        spawn_ball(right_win)


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("Restart", new_game)
timer_ready = simplegui.create_timer(1000, game_begin)
timer_goal = simplegui.create_timer(100, goal_pause)

# start frame
new_game()
frame.start()

