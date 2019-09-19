"""
Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day

Box with circular holes

based on https://github.com/villares/sketch-a-day/tree/master/2019/sketch_190918a)
"""

from frame_box import frame_box, unfolded_frame_box

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
        pushMatrix()
        translate(0, 0, 200)
        rotateX(HALF_PI / 2)
        frame_box(w, h, d, thick)
        popMatrix()
    if modes[0] <= 0:
        unfolded_frame_box(w, h, d, thick)

def mousePressed():
    modes[:] = modes[1:] + [modes[0]]

def keyPressed():
    if key == 'p':
        saveFrame("a###.png")
    if key == ' ':
        dimensions[:] = [250, 150, 100, 30]

    DIMENSION_KEYS = (('a', 'd', key),
                      ('w', 's', key),
                      (LEFT, RIGHT, keyCode),
                      (UP, DOWN, keyCode))

    for i, (plus, minus, k) in enumerate(DIMENSION_KEYS):
        if k == plus:
            dimensions[i] += 1
        elif k == minus:
            dimensions[i] -= 1
