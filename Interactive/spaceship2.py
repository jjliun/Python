#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : spaceship2.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-05-25
'''Game: Spaceship, implemented using `simplegui` powered by `CodeSkuptor`

I redesign the whole architecture to gain more flexibility.

Each section marked between "###...###" represents a different level of abstraction. Normally
they should be saved in separated files.
'''
import simplegui
import random
import math

########################################################################
# Physics

def angle_to_vector(ang):
    return (math.cos(ang), math.sin(ang))

def cart_to_polar(vec):
    m = vec.dist(Vector2D(0, 0))
    p = math.acos(vec[0] / m)
    return [m, p]

def polar_to_cart(polar):
    return Vector2D(* [polar[0] * p for p in angle_to_vector(polar[1])] )

#def makeCartesian(n): NOTE: I can not create a class factory on CodeSkulptor
n = 2
"""Create a class represents n-dimension coordinates"""
class Cartesian:

    def __init__(self, *vals):
        """The length limitation of vals is exactly the number of dimensions.
        """
        if len(vals) != n:
            raise TypeError, "Cartesian takes exactly %d arguments (%d given)" % (n, len(vals))

        self.vals = list(vals)

    def __add__(self, that):
        return Cartesian(*[ a + b for (a, b) in zip(self.vals, that.vals) ])

    def __getitem__(self, idx):
        return self.vals[idx]

    def __setitem__(self, idx, val):
        self.vals[idx] = val

    def __str__(self):
        return "(" + ", ".join([ str(e) for e in self.vals ]) + ")"

    def dist(self, that):
        """Cartesian distance"""
        return math.sqrt( sum([ (a - b) ** 2 for (a, b) in zip(self.vals, that.vals) ]) )

    def toList(self): # I can't understand why `canvas.draw` accept the Cartesion class as `center`
        return self.vals

#return Cartesian
#Vector2D = makeCartesian(2)
Vector2D = Cartesian

class Derivatives:
    """Derivatives in math

    If the element with index i (i >= 0), then it represents the i-th derivative.

    For example, if `value[0]` represent the displacement, then `value[1]` will
    be velocity and `value[2]` will be acceleration.

    """

    def __init__(self, *derivatives):
        """
        :derivatives: @ A unlimited length list stored current derivatives' values.

        """
        self.derivatives = list(derivatives)

    def update(self, final_delta = None):
        """Update the values to the next iteration

        Update from the last to the first.

        :final_delta: @ The delta of the last derivative
        """
        l = len(self.derivatives)

        if final_delta:
            #self.derivatives[ l - 1 ] += final_delta NOTE: not supported in CodeSkulptor
            self.derivatives[ l - 1 ] = self.derivatives[ l - 1 ] + final_delta

        for i in range(l - 2, -1, -1):
            #self.derivatives[ i ] += self.derivatives[ i + 1 ] NOTE: not supported in CodeSkulptor
            self.derivatives[ i ] = self.derivatives[ i + 1 ] + self.derivatives[ i ]

    def __getitem__(self, idx):
        return self.derivatives[idx]

    def __setitem__(self, idx, val):
        self.derivatives[idx] = val

    def __str__(self):
        return "(" + ", ".join([ str(e) for e in self.derivatives ]) + ")"

    def toList(self):
        return self.derivatives


# End of Physics
########################################################################

########################################################################
# Image Display

""" Because I cannot create a class factory on CodeSkulptor, so I
design another ugly implementation. """

class ImageInfo:
    """Meta data about drawing a image (a tiled image)"""

    def __init__(self, url, size, animated = False, layout = "horizontal", n_tiled = [1]):
        """The data like size, animated, etc. are not valid for another image source, so
why not integrate the image url into the class.

        :url:      @ imaage url
        :size:     @ size of one tiled image, may not be the full size of image source
        :animated: @ will it automatically iterate through tiled images when drawing
        :layout:   @ geometry indexing of tiled images
        :n_tiled:  @ number of tiled images in each dimensions

        get_center(*indexes) @ get the center coordinates according to indexes
        draw(canvas, pos, output_size, *indexes) @ draw image on canvas at pos with output_size.

        """
        self.img      = simplegui.load_image(url)
        self.size     = size
        self._center  = [l // 2 for l in size]
        self.animated = animated
        self.layout   = layout
        self.n_tiled  = n_tiled

        if animated: # cache the current displayed tiled image's index
            self.tiled_pos = [0] * len(n_tiled)

        if len(self.n_tiled) < len(self.size): # because I can't use izip_longest
            self.n_tiled += [float('inf')] * (len(self.size) - len(self.n_tiled))


    def _compute_center(self, *indexes):
        return [pos + step * (idx % n_f)
           for (pos, step, idx, n_f)
           in  zip(self._center, self.size, indexes, self.n_tiled)]

    def _center_horizontal(self, x = 0):
        return self._compute_center(x, 0)

    def _center_vertical(self, y = 0):
        return self._compute_center(0, y)

    def _compute_grid(self, x = 0, y = 0):
        return self._compute_center(x, y) # That's the layout of BlackJack cards

    def get_center(self, *indexes):
        """The advantage of function factory is that is can handle many
conditional determination beforehand. Take this function as example, if
the closure is fully supported in CodeSkulptor, we can create different
`get_center` function according to the value of `layout` so as not to
run if-else determination everytime invoking this function """
        if self.layout == "horizontal":
            return self._center_horizontal(*indexes)
        elif self.layout == "verticle":
            return self._center_vertical(*indexes)
        elif self.layout == "grid":
            return self._compute_grid(*indexes)
        else:
            """Another advantage is that if you pass a wrong layout value,
we will know right after the instance's built but not when invoking the function."""
            raise KeyError, "invalid layout: %r" % self.layout

    def draw(self, canvas, pos, output_size, rotation = 0, *indexes):
        if self.animated:
            src_pos = self.tiled_pos
        else:
            src_pos = indexes

        canvas.draw_image(self.img, self.get_center(*src_pos), self.size, pos, output_size, rotation)

        if self.animated:
            if self.layout in ['horizontal', 'verticle']:
                self._iter_1D()
            elif self.layout == 'grid':
                self._iter_2D()
            else:
                raise KeyError, "invalid layout: %r" % self.layout


    def _iter_1D(self):
        self.tiled_pos[0] += 1

    def _iter_2D(self):
        pass

# End of Image Display
########################################################################

########################################################################
# Defination of Sprites

class SpriteInfo:
    """ Integrated meta data about one kind of sprite """

    def __init__(self, size, radius = 0, lifespan = float('inf'), sound_url = None):
        """All the resuable data

        :size:      @ output size of image
        :radius:    @ for collision determination
        :lifespan:  @ automatically disappear if not infinite, count in drawing frames
        :sound_url: @ sound file url

        """
        self.size     = size
        self.radius   = radius
        self.lifespan = lifespan

        self.sound = simplegui.load_sound(sound_url) if sound_url else None

class Sprite:
    """ The instance of a sprite """

    def __init__(self, pos_derivatives, ang_derivatives, imginfo, spriteinfo, scale = 1.0, sound_on = True):
        """
        :pos_derivatives: @ status of displacement, passed as list
        :ang_derivatives: @ status of angle, passed as list
        :imginfo:         @ instance of a ImageInfo
        :spriteinfo:      @ meta data of this kind of sprite
        """
        self.pos    = Derivatives(*pos_derivatives)
        self.ang    = Derivatives(*ang_derivatives)
        self.img    = imginfo
        self.meta   = spriteinfo

        self.size   = [round(s * scale) for s in self.meta.size]
        self.radius = self.meta.radius * scale
        self.life   = 1
        self.isDead = False

        if self.meta.sound and sound_on:
            self.meta.sound.play()

    def draw(self, canvas, *indexes):
        # I have to use toList method for CodeSkulptor `canvas.draw` doesn't accept Vector2D class
        if not self.isDead:
            self.img.draw(canvas, self.pos[0].toList(), self.size, self.ang[0], *indexes)

    def update(self):
        if self.isDead:
            return

        self.pos.update()
        self.ang.update()

        self.pos[0][0] %= WIDTH
        self.pos[0][1] %= HEIGHT

        """about lifespan"""
        if self.meta.lifespan != float('inf'):
            self.life += 1

            if self.life > self.meta.lifespan:
                self.isDead = True

    def collide(self, that):
        return self.pos[0].dist( that.pos[0] ) < self.radius + that.radius

# Still, this also can't work on CodeSkulptor :(
#def makeSprite(spriteinfo, *imginfos):
    #def maker(pos_derivatives, ang_derivatives):
        #return Sprite(
          #Derivatives(*pos_derivatives),
          #Derivatives(*ang_derivatives),
          #random.choice(imginfos), spriteinfo)
    #return maker

# define sprite makers
img_nebula = ImageInfo(
  "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png",
  [800, 600])

img_debris = ImageInfo(
  "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png",
  [640, 480])

img_splash = ImageInfo(
  "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png",
  [400, 300])

# ship image
img_ship = ImageInfo(
  "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png",
  [90, 90], n_tiled = [2])

meta_ship = SpriteInfo([90, 90], radius = 35,
  sound_url = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")

## Ship creator
class Ship(Sprite):
    """Add some functions for ships"""

    ANGEL_VEL = 0.07
    ACC = 0.45
    FRI = 0.05

    def __init__(self, pos_derivatives, ang_derivatives):
        Sprite.__init__(self, pos_derivatives, ang_derivatives, img_ship, meta_ship, sound_on = False)
        self.isThrust = False

    def update(self):
        # I don't know why i can't iterate my class even I've implemented __iter__
        self.pos[1][0] *= (1 - Ship.FRI)
        self.pos[1][1] *= (1 - Ship.FRI)

        if self.isThrust:
            self.pos[2] = Vector2D(* [Ship.ACC * c for c in angle_to_vector(self.ang[0])] ) # acceleration
        else:
            self.pos[2] = Vector2D(0, 0)

        Sprite.update(self)

    def draw(self, canvas):
        if hasShield:
            canvas.draw_circle(self.pos[0].toList(), self.radius + 3, 6, "silver")
            canvas.draw_circle(self.pos[0].toList(), self.radius + 2, 4, "gray")
            canvas.draw_circle(self.pos[0].toList(), self.radius, 2, "white")

        idx = 1 if self.isThrust else 0
        Sprite.draw(self, canvas, idx)

    def shoot(self):
        MULTI = 10

        pos = self.pos[0].vals
        vel = self.pos[1].vals
        angle = self.ang[0]

        missile = Missile([
          Vector2D(* [p + self.radius * c for (p, c) in zip(pos, angle_to_vector(angle))] ),
          Vector2D(* [v + MULTI * a for (v, a) in zip(vel, angle_to_vector(angle))] ),
          ],
          [0, 0],
          scale = missile_scale
        )

        missiles.add(missile)

    """ Use factories to return controller as keyboard handler """
    def angle_control(self, stat):

        if stat == "stop":
            def controller():
                self.ang[1] = 0

        elif stat == "ccw":
            def controller():
                self.ang[1] = -Ship.ANGEL_VEL

        elif stat == "cw":
            def controller():
                self.ang[1] = Ship.ANGEL_VEL

        else:
            raise KeyError, "%s is not a valid stat in Ship.angle_control()" % stat

        return controller

    def thrust_on(self, on):

        if on:
            def controller():
                self.isThrust = True
                self.meta.sound.play()
        else:
            def controller():
                self.isThrust = False
                self.meta.sound.rewind()

        return controller

# missile image - shot1.png, shot2.png, shot3.png
imgs_missile = [ ImageInfo(
  "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot%d.png" % i,
  [10, 10]) for i in range(1, 4) ]

meta_missile = SpriteInfo([10, 10], radius = 3, lifespan = 50,
  sound_url = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")

meta_missile.sound.set_volume(.5)

class Missile(Sprite):
    def __init__(self, pos_derivatives, ang_derivatives, scale = 1.0):
        img = random.choice(imgs_missile)
        Sprite.__init__(self, pos_derivatives, ang_derivatives, img, meta_missile, scale = scale)

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
imgs_asteroid = [ ImageInfo(
  "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_%s.png" % clr,
  [90, 90]) for clr in ['blue', 'brown', 'blend'] ]

meta_asteroid = SpriteInfo([90, 90], radius = 40)

class Asteroid(Sprite):
    def __init__(self, pos_derivatives, ang_derivatives, scale = 1, color_idx = 0,
                 doSplit = False, split_level = 2):
        img = imgs_asteroid[ color_idx % len(imgs_asteroid) ]
        Sprite.__init__(self, pos_derivatives, ang_derivatives, img, meta_asteroid, scale = scale)

        self.scale     = scale
        self.color_idx = color_idx

        self.doSplit     = doSplit
        self.split_level = split_level

    def split(self):
        """ Return the splited asteroids as list """
        if self.split_level <= 0:
            self.doSplit = False
            return []
        else:
            vel_polar = cart_to_polar(self.pos[1])

            ang1 = vel_polar[1] + math.pi / 4
            ang2 = vel_polar[1] - math.pi / 4

            vel1 = polar_to_cart( [vel_polar[0] * 1.5, ang1] )
            vel2 = polar_to_cart( [vel_polar[0] * 1.5, ang2] )

            offset1 = polar_to_cart( [self.radius, ang1] )
            offset2 = polar_to_cart( [self.radius, ang2] )

            pos1 = self.pos[0] + offset1
            pos2 = self.pos[0] + offset2

            return [ Asteroid([pos1, vel1], [self.ang[0] + 0.01, self.ang[1] * 1.5],
                              scale       = self.scale / 1.4,
                              color_idx   = self.color_idx,
                              doSplit     = True,
                              split_level = self.split_level - 1
                     ),
                     Asteroid([pos2, vel2], [self.ang[0] - 0.01, -self.ang[1] * 1.5],
                              scale       = self.scale / 1.4,
                              color_idx   = self.color_idx,
                              doSplit     = True,
                              split_level = self.split_level - 1
                     )
                   ]

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
imgs_explosion = [ ImageInfo(
  "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_%s.png" % clr,
  [128, 128], animated = True, n_tiled = [24]) for clr in ['blue', 'orange', 'blue2', 'alpha'] ]

meta_explosion = SpriteInfo([128, 128], radius = 17, lifespan = 24,
  sound_url = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

class Explosion(Sprite):
    def __init__(self, pos_derivatives, ang_derivatives, scale = 1.0, color_idx = 0):
        img = imgs_explosion[ color_idx % len(imgs_explosion) ]
        Sprite.__init__(self, pos_derivatives, ang_derivatives, img, meta_explosion, scale = scale)

        self.scale = scale
        self.color_idx = color_idx

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")

# Extensions
class Bonus(Sprite):
    def __init__(self, pos_derivatives, imginfo, spriteinfo, scale):
        Sprite.__init__(self, pos_derivatives, [0], imginfo, spriteinfo, scale)

    def draw(self, canvas):
        remain = self.meta.lifespan - self.life
        # blingbling at the last 5 second
        if (remain < 300 and (remain // 20) % 2 == 0) or (remain >= 300):
            Sprite.draw(self, canvas)

    def activate(self):
        raise NotImplementedError

    #def draw(self, canvas): # blingbling at last 5 second

# XXX by who?
img_clock = ImageInfo("http://storage.googleapis.com/ricerock-bonus/clock.png", [400, 400])
meta_clock = SpriteInfo([400, 400], radius = 400 * 0.12, lifespan = 1500)
class BonusClock(Bonus):
    """ Shut down all rocks """
    def __init__(self, pos_derivatives):
        Bonus.__init__(self, pos_derivatives, img_clock, meta_clock, scale = 0.12)

    def activate(self):
        global freezeTime
        freezeTime = True
        freeze_timer.start()

# by caleb7447
img_shield = ImageInfo("http://storage.googleapis.com/ricerock-bonus/shield_237x290.png", [237, 290])
meta_shield = SpriteInfo([237, 290], radius = 48, lifespan = 1500)
class BonusShield(Bonus):
    """ Protect from one damage """
    def __init__(self, pos_derivatives):
        Bonus.__init__(self, pos_derivatives, img_shield, meta_shield, scale = 48.0 / 237.0)

    def activate(self):
        global hasShield
        hasShield = True

img_nuclear = ImageInfo("http://storage.googleapis.com/ricerock-bonus/nuclear.png", [64, 64])
meta_nuclear = SpriteInfo([64, 64], radius = 48, lifespan = 1500)
class BonusNuclear(Bonus):
    """ Destroy all asteroids """
    def __init__(self, pos_derivatives):
        Bonus.__init__(self, pos_derivatives, img_nuclear, meta_nuclear, scale = 48.0 / 64.0)

    def activate(self):
        global asteroids
        for a in asteroids:
            explosions.add( Explosion([a.pos[0]], [0], scale = a.scale, color_idx = a.color_idx) )
        asteroids = set([])

img_life = ImageInfo("http://storage.googleapis.com/ricerock-bonus/life_375x360.png", [375, 360])
meta_life = SpriteInfo([375, 360], radius = 48, lifespan = 1500)
class BonusLife(Bonus):
    """ Gain one life """
    def __init__(self, pos_derivatives):
        Bonus.__init__(self, pos_derivatives, img_life, meta_life, scale = 48.0 / 360.0)

    def activate(self):
        global lives
        lives += 1

img_upgrade = ImageInfo("http://storage.googleapis.com/ricerock-bonus/upgrade_79x80.png", [79, 80])
meta_upgrade = SpriteInfo([79, 80], radius = 48, lifespan = 1500)
class BonusUpgrade(Bonus):
    def __init__(self, pos_derivatives):
        Bonus.__init__(self, pos_derivatives, img_upgrade, meta_upgrade, scale = 48.0 / 80.0)

    def activate(self):
        global missile_scale
        missile_scale *= 1.5 # I can set a limit of the maximum scale, but I don't want to!!! LOL

# By my good friend Lai Wuning
img_slowdown = ImageInfo("http://storage.googleapis.com/ricerock-bonus/slowdown.png", [46, 26])
meta_slowdown = SpriteInfo([46, 26], radius = 50, lifespan = 1500)
class BonusSlowdown(Bonus):
    def __init__(self, pos_derivatives):
        Bonus.__init__(self, pos_derivatives, img_slowdown, meta_slowdown, scale = 1.0)

    def activate(self):
        speedup_asteroids(0.7)

# End of Definition of Sprites
########################################################################
########################################################################
# Frame architecture
WIDTH, HEIGHT = img_nebula.size

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

def draw(canvas):
    # background
    global time
    img_nebula.draw(canvas, [WIDTH // 2, HEIGHT // 2], [WIDTH, HEIGHT])

    time += 1
    wtime = (time / 4) % WIDTH
    img_debris.draw(canvas, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    img_debris.draw(canvas, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if isResume:
        if resumeBling:
            ship.draw(canvas)
    else:
        ship.draw(canvas)

    ship.update()

    for e in explosions:
        e.draw(canvas)
        e.update()

    for m in missiles:
        m.draw(canvas)
        m.update()

    set_to_remove = set([])
    for a in asteroids:
        a.draw(canvas)
        if not freezeTime: # Extension: Bonus Freeze time
            a.update()

        if not isResume and ship.collide(a):
            set_to_remove.add(a)
            explosions.add( Explosion([a.pos[0]], [0], scale = a.scale, color_idx = a.color_idx) )

            global hasShield
            if hasShield:
                hasShield = False
            else:
                oops()
    asteroids.difference_update(set_to_remove)

    set_to_remove = set([])
    for b in bonus:
        b.draw(canvas)
        b.update()

        if ship.collide(b):
            set_to_remove.add(b)
            b.activate()
    bonus.difference_update(set_to_remove)

    shoot_collision()
    upgrade_level()

    canvas.draw_text("score: %05d" % score, [WIDTH - 180, 40], 30, level_colors[level])
    canvas.draw_text("lives: %d" % lives, [10, 40], 30, get_life_color())
    canvas.draw_text("level: %d" % level, [WIDTH - 100, HEIGHT - 40], 30, level_colors[level])
    if playername == "Yang Leo":
        canvas.draw_text("King of the world", [10, HEIGHT - 40], 30, "red")
    else:
        canvas.draw_text(playername, [10, HEIGHT - 40], 30, level_colors[hallOfHonor[playername]])

    if not gameStarted:
        cron_spawn.stop()
        draw_records(canvas)
        img_splash.draw(canvas, [WIDTH // 2, HEIGHT // 2], img_splash.size)
    else:
        cron_spawn.start()


def clickSplash(pos): # no need to check if pos in the area of img_splash
    global gameStarted
    gameStarted = True
    record_timer.stop()
    init()

def spawn_asteroid():
    from random import randint
    color_idx = randint(0, len(imgs_asteroid) - 1)

    pos = Vector2D( randint(0, WIDTH), randint(0, HEIGHT) )
    while (pos.dist( ship.pos[0] ) < ship.radius * 3): # keep a distance from the ship
        pos = Vector2D( randint(0, WIDTH), randint(0, HEIGHT) )

    # Enhance 1: faster as level increased
    speed = randint(50, 150) / 400.0 * (level + 1)
    ang_speed = randint(3, 6) / 100.0 * math.sqrt(level + 1)

    # Enhance 2: some extraordinary fast rocks
    odd = random.random()
    if odd < 0.05:
        speed *= 2
        ang_speed *= 1.5

    vel = Vector2D(* [speed * d for d in angle_to_vector(randint(0, 628) / 100.0)] )

    # Enhance 3: some of the rocks will break asunder
    odd = random.random()
    prob = 0.10 + 0.10 * level
    split = True if odd < prob else False

    asteroids.add( Asteroid([pos, vel], [0, ang_speed], color_idx = color_idx, doSplit = split) )

def oops():
    """If game over, return true"""
    global asteroids, gameStarted, bonus
    global lives, last_record
    global ship, isResume, resumeBling

    lives -= 1
    if lives <= 0:
        last_record = (score, playername)
        records.append(last_record)
        records.sort(lambda x, y: y - x, key = lambda tup: tup[0])
        record_timer.start()

        notch = score_to_level(score)
        if notch > hallOfHonor[playername]:
            hallOfHonor[playername] = notch

        gameStarted = False
        asteroids = set([])
        bonus = set([])
        cron_spawn.stop()

        soundtrack.rewind() # It's annoying!

    ship = Explosion([ship.pos[0]], [0], color_idx = 3)

    isResume = True
    resumeBling = True
    resume_timer.start()
    bling_timer.start()
    respawn_timer.start()

def resume_ship():
    global isResume
    isResume = False
    resume_timer.stop()
    bling_timer.stop()

def respawn_ship():
    global ship
    ship = shipbackup
    ship.pos = Derivatives( Vector2D(WIDTH // 2, HEIGHT // 2), Vector2D(0, 0), Vector2D(0, 0) )
    ship.ang = Derivatives( 0, 0 )
    respawn_timer.stop()

def blingbling():
    global resumeBling
    resumeBling = not resumeBling

def shoot_collision():
    # The reason I don't use group_group_collision is because it's hard to change the inner
    # logic from outside. The flexibility is important in imporve the gmae
    global score
    a_to_remove = set([])
    a_to_add    = set([])

    for a in asteroids:
        for m in list(missiles):
            if m.collide(a):

                if playername == "Yang Leo": # NOTE: I'm the KING of the world!
                    score += 11111
                else:
                    score += 10 * (level + 1)

                missiles.remove(m)
                a_to_remove.add(a)
                explosions.add( Explosion([a.pos[0]], [0], scale = a.scale, color_idx = a.color_idx) )

                if a.doSplit:
                    a_to_add.update(a.split())

                # Extension: sometimes yield a bonus
                vel = Vector2D(* [v * 0.3 for v in a.pos[1].toList()] )

                ## Upgrade missile!!
                odd = random.random()
                if odd < 0.015:
                    bonus.add( BonusUpgrade([a.pos[0], vel]) )
                    break

                ## Shield!
                odd = random.random()
                if odd < 0.02:
                    bonus.add( BonusShield([a.pos[0], vel]) )
                    break

                ## Freeze!
                odd = random.random()
                if odd < 0.02:
                    bonus.add( BonusClock([a.pos[0], vel]) )
                    break

                ## Slowdown!
                odd = random.random()
                if odd < 0.03:
                    bonus.add( BonusSlowdown([a.pos[0], vel]) )
                    break

                ## Nuclear bomb!
                odd = random.random()
                if odd < 0.02:
                    bonus.add( BonusNuclear([a.pos[0], vel]) )
                    break

                ## Life!!!
                odd = random.random()
                if odd < 0.01:
                    bonus.add( BonusLife([a.pos[0], vel]) )
                    break

                break

    asteroids.difference_update(a_to_remove)
    asteroids.update(a_to_add)

def cleanup():
    """ Clean up useless missiles """
    for s in [missiles, explosions, bonus]:

        set_to_remove = set([])
        for m in s:
            if m.isDead:
                set_to_remove.add(m)

        s.difference_update(set_to_remove)

def upgrade_level():
    global level
    if level >= len(level_notches) - 1:
        return

    if score >= level_notches[level]:
        level += 1
        speedup_asteroids( (level + 1) / float(level) )

def speedup_asteroids(scale):
    global asteroids
    new_list = []
    for a in asteroids:
        vel = Vector2D( a.pos[1][0] * scale, a.pos[1][1] * scale )
        ang_vel = a.ang[1] * math.sqrt(scale)

        new_list.append( Asteroid(
                           [ a.pos[0], vel],
                           [ a.ang[0], ang_vel],
                           scale     = a.scale,
                           color_idx = a.color_idx)
        )

    asteroids = set(new_list)

def score_to_level(s):
    for idx, notch in enumerate(level_notches):
        if s <= notch:
            return idx
    else:
        return len(level_notches) - 1

def draw_records(canvas):
    if len(records) == 0:
        return

    canvas.draw_text("Hall of Honor", [30, 80], 24, "green")
    canvas.draw_text("Rank", [10, 110], 20, "green")
    canvas.draw_text("Score", [60, 110], 20, "green")
    canvas.draw_text("Player", [120, 110], 20, "green")

    for idx, tup in enumerate(records):
        if idx > 15:
            break

        if tup is last_record and recordBling:
            continue

        score, name = tup
        canvas.draw_text("%2d" % (idx + 1), [15, 140 + 25 * idx], 20, "green")
        canvas.draw_text("%5d" % score,   [60, 140 + 25 * idx], 20, level_colors[score_to_level(score)])
        canvas.draw_text("%s"  % name,    [120, 140 + 25 * idx], 20, level_colors[hallOfHonor[name]])

def change_name(text):
    global playername
    playername = text

    if not hallOfHonor.has_key(playername):
        hallOfHonor[playername] = 0

def record_bling():
    global recordBling
    recordBling = not recordBling

def freeze_over():
    global freezeTime
    freezeTime = False
    freeze_timer.stop()

# End of Frame architecture
########################################################################

########################################################################
# Initialization & Run
shipbackup = Ship([Vector2D(400, 300), Vector2D(0, 0), Vector2D(0, 0)], [0, 0])
time = 0

isResume    = False
resumeBling = False
gameStarted = False

level_notches = [100, 300, 1500, 5000, 10000, 20000, 35000, 50000, 60000, 75000]
level_colors  = ["gray", "silver", "teal", "blue", "aqua", "lime", "yellow", "orange", "purple", "red"]
lives_colors  = ["gray", "red", "yellow", "white"]

def get_life_color():
    if 0 <= lives <= 3:
        return lives_colors[lives]
    else:
        return "green"

# Records
last_record = None
recordBling = False
records = [(99999, "Yang Leo (jeremyrobturtle@gmail.com)"),
           (75000, "Anakin Skywalker"),
           (60000, "Obiwan Konobi"),
           (50000, "Padme Amidala"),
           (35000, "Master Yoda"),
           (20000, "Mace Windu"),
           (10000, "Luke Skywalker"),
           (5000,  "Darth Vader"),
           (1500,  "Han Solo"),
           (300,   "Leia Organa"),
          ]
playername = "Player"

hallOfHonor = {
  "Yang Leo (jeremyrobturtle@gmail.com)": 9,
  "Anakin Skywalker": 9,
  "Obiwan Konobi": 8,
  "Padme Amidala": 7,
  "Master Yoda": 6,
  "Mace Windu": 5,
  "Luke Skywalker": 4,
  "Darth Vader": 3,
  "Han Solo": 2,
  "Leia Organa": 1,
  "Player": 0
}

def init():
    global ship, missiles, asteroids, explosions, bonus
    global lives, score, gameStarted, level
    ship = shipbackup
    ship.pos = Derivatives( Vector2D(WIDTH // 2, HEIGHT // 2), Vector2D(0, 0), Vector2D(0, 0) )
    ship.ang = Derivatives( 0, 0 )

    missiles   = set([])
    asteroids  = set([])
    explosions = set([])
    bonus      = set([])

    lives = 3
    score = 0
    level = 0

    soundtrack.rewind()
    soundtrack.play()

    # Extension: Bonus
    global freezeTime, hasShield, missile_scale
    freezeTime = False
    hasShield  = False
    missile_scale = 1.0

# Controllers
DEVENTS = {
  "left"  : shipbackup.angle_control("ccw"),
  "right" : shipbackup.angle_control("cw"),
  "up"    : shipbackup.thrust_on(True),
  "space" : shipbackup.shoot
}

UEVENTS = {
  "left"  : shipbackup.angle_control("stop"),
  "right" : shipbackup.angle_control("stop"),
  "up"    : shipbackup.thrust_on(False)
}

# timers
cron_clean    = simplegui.create_timer(meta_missile.lifespan * 3, cleanup)
cron_spawn    = simplegui.create_timer(1500, spawn_asteroid)

resume_timer  = simplegui.create_timer(4000, resume_ship)
bling_timer   = simplegui.create_timer(50, blingbling)
respawn_timer = simplegui.create_timer(1000, respawn_ship)
record_timer  = simplegui.create_timer(100, record_bling)

freeze_timer = simplegui.create_timer(5000, freeze_over)

frame = simplegui.create_frame("Spaceship", WIDTH, HEIGHT)

frame.set_draw_handler(draw)
frame.set_keydown_handler(make_keyhandler(DEVENTS))
frame.set_keyup_handler(make_keyhandler(UEVENTS))
frame.set_mouseclick_handler(clickSplash)

frame.add_input("Enter player's name:", change_name, 150)

init()
frame.start()
cron_clean.start()
# End of Initialization & Run
########################################################################
