"""
Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day

Box with circular holes

based on https://github.com/villares/sketch-a-day/tree/master/2019/sketch_190918a)
"""

from frame_box import frame_box, unfolded_frame_box

DIMENSION_KEYS = (('a', 'd'),
                  ('w', 's'),
                  (LEFT, RIGHT),
                  (UP, DOWN))
dimensions = [250, 150, 100, 30]
modes = [-1, 0, 1]  # click mouse to switch modes

def setup():
    size(600, 600, P3D)

def draw():
    background(200)
    translate(300, 300)
    w, h, d, thick = dimensions
    if modes[0] >= 0:
        fill(255)
        stroke(0)
        push_matrix()
        translate(0, 0, 200)
        rotate_x(HALF_PI / 2)
        frame_box(w, h, d, thick)
        pop_matrix()
    if modes[0] <= 0:
        unfolded_frame_box(w, h, d, thick)

def mouse_pressed():
    modes[:] = modes[1:] + [modes[0]]

def key_pressed():
    if key == 'p':
        save_frame("a###.png")
    if key == ' ':
        dimensions[:] = [250, 150, 100, 30]

    k = key_code if key == CODED else key
    for i, (plus, minus) in enumerate(DIMENSION_KEYS):
        if k == plus:
            dimensions[i] += 1
        elif k == minus:
            dimensions[i] -= 1
