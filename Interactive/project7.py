#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : project7.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-05-29
'''program template for Spaceship
'''
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class Image:

    class Entity:
        """ data relative with physics engine """
        def __init__(self, radius, lifespan):
            self.radius = radius
            self.lifespan = lifespan

    class Info:
        """ data prompting how to display the image """
        def __init__(self, size, animated = False, layout = "horizontal"):
            self.center   = [s // 2 for s in size]
            self.size     = size
            self.animated = animated
            self.layout   = layout

            # about get i-th tiled image
            def center_pos(*indexes):
                return [center + size * index for (center, size, index) in zip(self.center, self.size, indexes)]

            if layout == "horizontal":
                def center_finder(*indexes):
                    return center_pos(indexes[0], 0)

            elif layout == "verticle":
                def center_finder(*indexes):
                    return center_pos(0, indexes[0])

            elif layout == "grid":
                def center_finder(*indexes):
                    return center_pos(indexes[0], indexes[1])

            self._center_finder = center_finder

        def get_center(self, x = 0, y = 0, *indexes):
            return self._center_finder(x, y, *indexes)


    def __init__(self, url, size, animated = False, layout = "horizontal", radius = 0, lifespan = float('inf')):
        self.img = simplegui.load_image(url)
        self.info = Image.Info(size, animated, layout)
        self.entity = Image.Entity(radius, lifespan)

    def draw(self, canvas, pos, x = 0, y = 0, *indexes):
        canvas = simplegui.Canvas
        canvas.draw_image(self.img,
                          self.info.get_center(x, y, *indexes),
                          self.info.size, pos, self.info.size)


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
img_debris = Image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png", [640, 480])

# nebula images - nebula_brown.png, nebula_blue.png
img_nebula = Image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png", [800, 600])

# splash image
img_splash = Image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png", [400, 300])

# ship image
img_ship = Image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png", [90, 90], radius = 35)

# missile image - shot1.png, shot2.png, shot3.png
img_missile = Image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png", [10, 10], radius = 3, lifespan = 50)

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
img_asteroid = Image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png", [90, 90], radius = 40)

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
img_explosion = Image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png",
                      [128, 128], raiuds = 17, lifespan = 24, animated = True)

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    ANGEL_ACC = 0.06
    ACC = 0.15
    FRI = 0.02

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.center
        self.image_size = info.size
        self.radius = info.radius

    def draw(self,canvas):
        # XXX: capsulate part selection and show
        #      def drawtiled(idx)
        if self.thrust:
            src_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
        else:
            src_center = self.image_center

        canvas.draw_image(self.image,
                          src_center, self.image_size,
                          self.pos, self.image_size,
                          self.angle)

    def update(self):
        # XXX: obviously Ship can derive from Sprite
        self.angle += self.angle_vel
        self.pos = [(pos + vel) % limit for (pos, vel, limit) in zip(self.pos, self.vel, [WIDTH, HEIGHT])]

        # XXX: store constants in parent class
        self.vel = [v * (1 - Ship.FRI) for v in self.vel]
        if self.thrust:
            self.vel = [v + Ship.ACC * compo for (v, compo) in zip(self.vel, angle_to_vector(self.angle))]

    def shoot(self):
        global a_missile

        MULTI = 10

        a_missile = Sprite(
          [pos + self.radius * c for (pos, c) in zip(self.pos, angle_to_vector(self.angle))],
          [v + MULTI * a for (v, a) in zip(self.vel, angle_to_vector(self.angle))],
          0, 0,
          img_missile.img, img_missile.info, missile_sound
        )


    """ Use factories to return controller as keyboard handler """
    def angle_control(self, stat):

        if stat == "stop":
            def controller():
                self.angle_vel = 0

        elif stat == "ccw":
            def controller():
                self.angle_vel -= Ship.ANGEL_ACC

        elif stat == "cw":
            def controller():
                self.angle_vel += Ship.ANGEL_ACC

        else:
            raise KeyError, "%s is not a valid stat in Ship.angle_control()" % stat

        return controller

    def thrust_on(self, on):

        sound_control = ship_thrust_sound.play if on else ship_thrust_sound.rewind
        def controller():
            self.thrust = on
            sound_control()

        return controller


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.center
        self.image_size = info.size
        self.radius = info.radius
        self.lifespan = info.lifespan
        self.animated = info.animated
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.pos = [(pos + vel) % limit for (pos, vel, limit) in zip(self.pos, self.vel, [WIDTH, HEIGHT])]


def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.center
    size = debris_info.size
    canvas.draw_image(nebula_image, nebula_info.center, nebula_info.size, [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

    # lives & scores
    canvas.draw_text("lives : %d" % lives, [10, 30], 24, "white")
    canvas.draw_text("score: %03d"  % score, [WIDTH - 120, 30], 24, "white")

def uniform(a, b): # why there is no uniform
    return random.random() * (b - a) + a

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    from random import randint, choice

    speed = [0, 0]
    while speed == [0, 0]:
        speed = [randint(-3, 3), randint(-3, 3)]

    a_rock = Sprite(
      [ WIDTH * uniform(0.0, 1.0),
        HEIGHT * uniform(0.0, 1.0)], # Position
      speed,                           # speed
      uniform(-2 * math.pi, 2 * math.pi),       # angle
      uniform(0.01, 0.04) * choice([-1, 1]),           # angle velocity
      asteroid_image, asteroid_info    # image and image info
    )

# keyboard handler
def make_keyhandler(events):
    """ Create a key handler from dictionary

    Example:
        events = { "up": foo, "s": bar }
        where foo and bar are 0-parameter callables
    """
    def handler(key):
        for k in events:
            if key == simplegui.KEY_MAP[k]:
                events[k]()
    return handler


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.02, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

DEVENTS = {"left": my_ship.angle_control("ccw"), "right": my_ship.angle_control("cw"), "up": my_ship.thrust_on(True), "space": my_ship.shoot}
UEVENTS = {"left": my_ship.angle_control("stop"), "right": my_ship.angle_control("stop"), "up": my_ship.thrust_on(False)}

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(make_keyhandler(DEVENTS))
frame.set_keyup_handler(make_keyhandler(UEVENTS))

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

