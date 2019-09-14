"""
Alexandre B A Villares - https://abav.lugaralgum.com/

Unfolding Prism or Pyramideal Solid

https://github.com/villares/Paper-objects-with-Processing-and-Python
For Processing Python Mode - https://py.processing.org
"""

from geometry import poly_draw, line_draw, unfold_tri_face, glue_tab

CUT_STROKE = color(255, 0, 0)
FOLD_STROKE = color(0, 0, 255)

p_height = 100
base_radius, top_radius = 50, 50
sides = 5

def setup():
    size(600, 600, P3D)
    hint(ENABLE_DEPTH_TEST)
    hint(ENABLE_DEPTH_SORT)

def draw():
    background(240)
    pushMatrix()
    translate(width / 2, height / 4 + 50)
    rotateX(radians(45))
    rotateZ(radians(frameCount / 3.))
    fill(255, 200)
    stroke(0)
    strokeWeight(2)
    # draw 3D piramid and get points
    base, top, face = prism_3D(sides, p_height, base_radius, top_radius)
    popMatrix()
    # draw unfolded 2D
    translate(width / 2, height * 3 / 4 - 50)
    prism_2D(base, top, face)

def prism_3D(np, h, base_r, top_r):
    # calculando os points
    base_points = []
    for i in range(np):
        ang = radians(i * 360. / np)
        x = sin(ang) * base_r
        y = cos(ang) * base_r
        base_points.append((x, y, 0))
    # edges da base
    o_base_points = base_points[1:] + [base_points[0]]
    base_edges = zip(base_points, o_base_points)
    top_points = []
    for i in range(np):
        ang = radians(i * 360. / np)
        x = sin(ang) * top_r
        y = cos(ang) * top_r
        top_points.append((x, y, h))
    # edges da base
    o_top_points = top_points[1:] + [top_points[0]]
    top_edges = zip(top_points, o_top_points)
    # edges
    for base_edge, top_edge in zip(base_edges, top_edges):
        (p1x, p1y, p1z), (p2x, p2y, p2z) = base_edge
        (p1tx, p1ty, p1tz), (p2tx, p2ty, p2tz) = top_edge
        beginShape()
        vertex(p1x, p1y, p1z)
        vertex(p1tx, p1ty, p1tz)
        vertex(p2tx, p2ty, p2tz)
        vertex(p2x, p2y, p2z)
        endShape(CLOSE)
    # one face
    (p1x, p1y, p1z), (p2x, p2y, p2z) = base_edges[0]
    (p1tx, p1ty, p1tz), (p2tx, p2ty, p2tz) = top_edges[0]
    face = [(p2x, p2y, p2z),
            (p1x, p1y, p1z),
            (p1tx, p1ty, p1tz),
            (p2tx, p2ty, p2tz),
            ]
    # draw base and top
    poly_draw(top_points)
    poly_draw(base_points)

    return base_points, top_points, face

def prism_2D(base, top, face):
    with pushMatrix():
        translate(150, -300)
        poly_draw(top, force_z=0)
    with pushMatrix():
        translate(-150, -300)
        poly_draw(base, force_z=0)
    x0, y0, z0 = face[1]
    x2, y2, z2 = face[2]
    d = dist(x0, y0, z0, x2, y2, z2)
    side = ((150, d - 150), (150, -150))
    for i in range(sides):
        side = unfold_tri_face(side, face[::-1])
    stroke(CUT_STROKE)
    line_draw(side[0], side[1])
    glue_tab((150, -150), (150, d - 150))


def keyPressed():
    global base_radius, top_radius, p_height, sides
    if keyCode == UP:
        p_height += 5
    if keyCode == DOWN:
        p_height -= 5
    if keyCode == LEFT:
        base_radius += 5
    if keyCode == RIGHT:
        base_radius -= 5
    if key == "w":
        sides += 1
    if key == "s" and sides > 3:
        sides -= 1
    if key == "a" and top_radius > 0:
        top_radius -= 5
    if key == "d":
        top_radius += 5
    if key == "g":
       saveFrame(SKETCH_NAME + ".gif")

def settings():
    from os import path
    global SKETCH_NAME
    SKETCH_NAME = path.basename(sketchPath())
