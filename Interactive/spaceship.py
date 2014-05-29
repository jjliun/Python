# program template for Spaceship
import simplegui
import math
import random

def makeSprite(url, size, animated = False, layout = "horizontal", frames = [1]):
    """Return a Sprite class with relative image attached

    :url:      @ url of image, the real data only stored here
    :size:     @ size of one FRAME (may not be size of whole image)
    :animated: @ will it iterate the frames automatically
    :layout:   @ geometry layout of frames
    :frames:   @ number of frames in each dinmensions
    """

    # Load image
    image = simplegui.load_image(url)

    # Calcluate center position from indexes
    _center = [l / 2 for l in size]

    def _compute_center(*indexes):
        return [pos + step * (idx % n_f)
           for (pos, step, idx, n_f)
           in  zip(_center, size, indexes, frames)]

    if layout == "horizontal":
        def get_center(*indexes):
            return _compute_center(indexes[0], 0)

    elif layout == "verticle":
        def get_center(*indexes):
            return _compute_center(0, indexes[0])

    elif layout == "grid":
        def get_center(*indexes):
            return _compute_center(indexes[0], indexes[1])

    else:
        raise KeyError, "'%s' is not a valid layout"

    # Set draw behavior, NOTE that the logic of animation of recycling is implemented in class
    def display(canvas, pos, ang = 0, scale = 1.0, x1 = 0, x2 = 0, *indexes):
        canvas = simplegui.Canvas
        canvas.draw_image(image,                        # I decide to just support single image for simplicity
                          get_center(x1, x2, *indexes), # get the correct position from source
                          size,                         # size of single frame of source
                          pos,                          # destination position
                          [l * scale for l in size],    # Enable scaling on destination
                          ang)                          # rotation

    class Primes: # FIXME: what's the correct name for 导数？ Make sure use '%s' to solve it
        """A List of primes, the i-th element represents the i-th prime

        :vals: @ the value of prime list
        """
        def __init__(self, *vals):
            self.vals = vals

        def update(self, final = 0):
            """update to next status

            :final: @ the delta of the final prime
            """
            l = len(self.vals)
            self.vals[l - 1] += final
            for i in range(l - 2, -1, -1):
                self.vals[i] += self.vals[i + 1]

    class Sprite:
        def __init__(self, posprimes, angprimes, radius = 0, lifespan = float('inf')):
            self.posprimes = Primes(*posprimes)
            self.angprimes = Primes(*angprimes)
            self.radius    = radius
            self.lifespan  = lifespan

        def draw(canvas):

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
                      [128, 128], radius = 17, lifespan = 24, animated = True)

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# test
def draw(canvas):
    img_ship.draw(canvas, [200, 100])
    img_ship.draw(canvas, [300, 200], 1)

frame = simplegui.create_frame("test", 800, 600)
frame.set_draw_handler(draw)

frame.start()
