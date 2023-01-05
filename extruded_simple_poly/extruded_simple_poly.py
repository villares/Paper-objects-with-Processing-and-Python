# Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day
"""
Unfold simple extrusion (no holes)
"""

from parts import Face, glue_tab

faces = []
THICK = 20

def setup():
    size(740, 480, P3D)
    zig = [(2.5, 3.5), (5.5, 3.5), (2.5, 5.5),
           # (5.5, 5.5), (2.5, 7.5), (5.5, 7.5),
           # (3.5, 9.5), (8.5, 6.5), (5.5, 6.5),
           (8.5, 4.5), (5.5, 4.5), (8.5, 2.5),
           # (5.5, 2.5), (7.5, 0.5)
           ]
    faces.append(Face(zig, THICK))


def draw():
    background(200, 210, 220)
    for f in faces:
        fill(255)
        stroke(0)
        f.draw_3D(-QUARTER_PI)
        no_fill()
        stroke(255, 0, 0)
        translate(200, 0)
        f.draw_2D()
        translate(200, 0)
        f.draw_2D()
        x, y = 25, 350
        translate(-400, 0)
        for p1, p2 in f.edges():
            d = dist(p1[0], p1[1], p2[0], p2[1]) * 35
            glue_tab((x, y), (x + d, y))
            glue_tab((x + d, y + THICK),( x, y + THICK))
            stroke(0, 0, 255)
            rect(x, y , d, THICK)
            x += d
            stroke(255, 0, 0)
            if x > width - d:
                glue_tab((x, y), (x, y + THICK))
                x = 25
                y += THICK * 2.2
        else: # a for else...
            glue_tab((x, y), (x, y + THICK))
