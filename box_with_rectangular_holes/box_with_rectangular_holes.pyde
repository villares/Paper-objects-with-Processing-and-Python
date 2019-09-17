"""
Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day

Box with rectangular holes
"""

from frame_box import frame_box, unfolded_frame_box

w, h, d, thick = 250, 150, 100, 30
modes = [-1, 0, 1] # click mouse to switch modes

def setup():
    size(600, 600, P3D)

def draw():
    background(200)
    translate(300, 300)
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
    if key == "s":
        saveFrame("a###.png")
    
