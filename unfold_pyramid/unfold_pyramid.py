"""
Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day

- Unfolding pyramids
"""

CUT_STROKE = color(255, 0, 0)
FOLD_STROKE = color(0, 0, 255)

outer_radius, inner_radius = 100, 50
sides = 5


def setup():
    size(400, 600, P3D)
    hint(ENABLE_DEPTH_TEST)
    hint(ENABLE_DEPTH_SORT)


def draw():
    background(240)
    push_matrix()
    translate(width / 2, height / 4 + 50)
    rotate_x(radians(45))
    rotate_z(radians(frame_count / 3.))
    fill(255, 200)
    stroke(0)
    stroke_weight(2)
    # draw 3D pyramid and get pts
    pts = pyramid_3_d(sides, outer_radius, inner_radius)
    pop_matrix()
    # draw unfolded 2D
    translate(width / 2, height * 3 / 4 - 50)
    pyramid_2_d(pts)


def pyramid_3_d(np, ext_r, base_r):
    # calculando os pts
    pts = []
    n = np * 2
    for i in range(n):
        ang = radians(i * 360. / n)
        if i % 2 == 0:
            r = base_r
        else:
            r = ext_r
        x = sin(ang) * r
        y = cos(ang) * r
        pts.append((x, y))
    # edges da base
    base_pts = pts[::2]
    o_base_pts = base_pts[1:] + [base_pts[0]]
    base_edges = zip(base_pts, o_base_pts)
    # calculo da altura
    (p0x, p0y), (p1x, p1y) = pts[0], pts[1]
    side = dist(p0x, p0y, p1x, p1y)
    h_squared = side * side - base_r * base_r
    if h_squared > 0:  # se a altura viavel
        h = sqrt(h_squared)
        for edge in base_edges:
            p1, p2 = edge
            begin_shape()
            vertex(*p1)
            vertex(*p2)
            vertex(0, 0, h)
            end_shape(CLOSE)
    # always draws base
    begin_shape()
    for pt in base_pts:
        vertex(*pt)
    end_shape(CLOSE)
    # return pts for 2D!
    return pts


def pyramid_2_d(pts):
    no_fill()
    # base fold lines
    stroke(FOLD_STROKE)
    begin_shape()
    for pt in pts[::2]:
        vertex(*pt)
    end_shape(CLOSE)
    # lateral edges
    o_pts = pts[1:] + [pts[0]]
    edges = zip(pts, o_pts)
    for i, edge in enumerate(edges):
        p1, p2 = edge
        stroke(CUT_STROKE)
        if i % 2 == 0:
            # abas de cola
            glue_tab(p2, p1, 10, )
            # FOLD_STROKE
            stroke(FOLD_STROKE)
            line(p2[0], p2[1], p1[0], p1[1])
        else:
            # outra edge cortada
            line(p1[0], p1[1], p2[0], p2[1])


def glue_tab(p1, p2, tab_w, cut_ang=QUARTER_PI / 3):
    """
    draws a trapezoidal or triangular glue tab along edge defined by p1 and p2,
    with width tab_w and cut angle a
    """
    al = atan2(p1[0] - p2[0], p1[1] - p2[1])
    a1 = al + cut_ang + PI
    a2 = al - cut_ang
    # calculate cut_len to get the base_rght tab width
    cut_len = tab_w / sin(cut_ang)
    f1 = (p1[0] + cut_len * sin(a1),
          p1[1] + cut_len * cos(a1))
    f2 = (p2[0] + cut_len * sin(a2),
          p2[1] + cut_len * cos(a2))
    edge_len = dist(p1[0], p1[1], p2[0], p2[1])

    if edge_len > 2 * cut_len * cos(cut_ang):    # 'normal' trapezoidal tab
        begin_shape()
        vertex(*p1)    # vertex(p1[0], p1[1])
        vertex(*f1)
        vertex(*f2)
        vertex(*p2)
        end_shape()
    else:    # short triangular tab
        fm = ((f1[0] + f2[0]) / 2, (f1[1] + f2[1]) / 2)
        begin_shape()
        vertex(*p1)
        vertex(*fm)    # middle way of f1 and f2
        vertex(*p2)
        end_shape()


def key_pressed():
    global inner_radius, outer_radius, sides
    if key_code == UP:
        outer_radius += 5
    if key_code == DOWN:
        outer_radius -= 5
    if key_code == LEFT:
        inner_radius += 5
    if key_code == RIGHT:
        inner_radius -= 5
    if key == "+" or key == "=":
        sides += 1
    if key == "-" and sides > 3:
        sides -= 1
