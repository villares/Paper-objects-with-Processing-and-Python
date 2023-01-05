import py5

CUT_STROKE, FOLD_STROKE = py5.color(255, 0, 0), py5.color(0, 0, 255)

def frame_box(w, h, d, thick=0):
    """ draw the 3D version of the box with rectangular holes """
    mw, mh, md = w / 2., h / 2., d / 2.
    py5.translate(0, 0, -md)  # base
    face(0, 0, w, h, thick)
    py5.translate(0, 0, d)  # top
    face(0, 0, w, h, thick)
    py5.translate(0, 0, -md)  # back to 0
    py5.rotate_y(py5.HALF_PI)
    py5.translate(0, 0, -mw)  # left side
    face(0, 0, d, h, thick)
    py5.translate(0, 0, w)  # right side
    face(0, 0, d, h, thick)
    py5.translate(0, 0, -mw)  # back to middle
    py5.rotate_y(-py5.HALF_PI)  # back to 0 rotation
    py5.rotate_x(py5.HALF_PI)
    py5.translate(0, 0, -mh)  # lateral e
    face(0, 0, w, d, thick)
    py5.translate(0, 0, h)  # lateral d
    face(0, 0, w, d, thick)
    py5.translate(0, 0, -mw)  # reset translate
    py5.rotate_x(-py5.HALF_PI)  # reset rotate


def face(x, y, w, h, e):
    mw, mh = w / 2., h / 2.
    py5.push_matrix()
    py5.translate(x, y)
    py5.begin_shape()
    py5.vertex(-mw, -mh)
    py5.vertex(+mw, -mh)
    py5.vertex(+mw, +mh)
    py5.vertex(-mw, +mh)
    hole(mw, mh, e)
    py5.end_shape(py5.CLOSE)
    py5.pop_matrix()


def hole(mw, mh, e):
    if e > 0 and mw - e > 0 and mh - e > 0:
        py5.begin_contour()
        np = 24
        for i in range(np):
            ang = py5.TWO_PI / np * i
            x = py5.sin(ang) * e
            y = py5.cos(ang) * e
            py5.vertex(x, y)
        py5.end_contour()


def unfolded_frame_box(w, h, d, thick=0, draw_main=True):
    mw, mh, md = w / 2., h / 2., d / 2.
    unfolded_face(0, -h - md, w, d, "aaan", thick, draw_main)
    unfolded_face(0, -mh, w, h, "vvvv", thick, draw_main)
    unfolded_face(0, -mh + mh + md, w, d, "cncv", thick, draw_main)
    unfolded_face(0, +mh + d, w, h, "cncc", thick, draw_main)
    unfolded_face(-mw - md, -mh, d, h, "acna", thick, draw_main)
    unfolded_face(mw + md, -mh, d, h, "ncaa", thick, draw_main)


def unfolded_face(x, y, w, h, edge_types, thick=0, draw_main=True):
    e0, e1, e2, e3 = edge_types
    mw, mh = w / 2., h / 2.
    py5.push_matrix()
    py5.translate(x, y)
    if draw_main:
        edge(-mw, +mh, -mw, -mh, e0)
        edge(-mw, -mh, +mw, -mh, e1)
        edge(+mw, -mh, +mw, +mh, e2)
        edge(+mw, +mh, -mw, +mh, e3)
    if thick > 0 and mw - thick > 0 and mh - thick > 0:
        py5.stroke(CUT_STROKE)
        py5.circle(0, 0, thick * 2)
    py5.pop_matrix()


def edge(x0, y0, x1, y1, edge_type):
    if edge_type == "n":  # no edge is drawn
        return
    elif edge_type == "c":  # cut stroke selected
        py5.stroke(CUT_STROKE)
    else:
        py5.stroke(FOLD_STROKE)  # fold stroke selected for "v" and "a"
    py5.line(x0, y0, x1, y1)    # line drawn here
    if edge_type == "a":    # tab (note a fold-stroke line was already drawn)
        py5.stroke(CUT_STROKE)
        py5.no_fill()
        glue_tab((x0, y0), (x1, y1), 10)


def glue_tab(p1, p2, tab_w, cut_ang=py5.QUARTER_PI / 3):
    """
    draws a trapezoidal or triangular glue tab along edge defined by p1 and p2,
    with width tab_w and cut angle a
    """
    al = py5.atan2(p1[0] - p2[0], p1[1] - p2[1])
    a1 = al + cut_ang + py5.PI
    a2 = al - cut_ang
    # calculate cut_len to get the right tab width
    cut_len = tab_w / py5.sin(cut_ang)
    f1 = (p1[0] + cut_len * py5.sin(a1),
          p1[1] + cut_len * py5.cos(a1))
    f2 = (p2[0] + cut_len * py5.sin(a2),
          p2[1] + cut_len * py5.cos(a2))
    edge_len = py5.dist(p1[0], p1[1], p2[0], p2[1])

    if edge_len > 2 * cut_len * py5.cos(cut_ang):    # 'normal' trapezoidal tab
        py5.begin_shape()
        py5.vertex(*p1)    # vertex(p1[0], p1[1])
        py5.vertex(*f1)
        py5.vertex(*f2)
        py5.vertex(*p2)
        py5.end_shape()
    else:    # short triangular tab
        fm = ((f1[0] + f2[0]) / 2, (f1[1] + f2[1]) / 2)
        py5.begin_shape()
        py5.vertex(*p1)
        py5.vertex(*fm)    # middle way of f1 and f2
        py5.vertex(*p2)
        py5.end_shape()


