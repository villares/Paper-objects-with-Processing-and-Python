import py5


class Face:

    def __init__(self, pts, thickness, orientation=(0, 0, 0)):
        self.points = pts
        self.thickness = thickness
        self.o = orientation

    def draw_2D(self):
        draw_poly(self.points)

    def draw_3D(self, rot):
        S = 35.28

        t = self.thickness
        pts = self.points
        with py5.push_matrix():
            py5.translate(0, py5.height() / 2)
            py5.rotate_x(self.o[0] * 0 + rot)
            py5.translate(0, -py5.height() / 2)
            py5.translate(0, 0, -t/2)
            py5.fill(230)
            draw_poly(pts)
            py5.translate(0, 0, t)
            py5.fill(170)
            draw_poly(pts)
            py5.fill(250)
            for p1, p2 in pairwise(tuple(pts) + (pts[0],)):
                # print((p1, p2))
                py5.begin_shape(py5.QUAD_STRIP)
                py5.vertex(p1[0]*S, p1[1]*S, 0)
                py5.vertex(p1[0]*S, p1[1]*S, -t)
                py5.vertex(p2[0]*S, p2[1]*S, 0)
                py5.vertex(p2[0]*S, p2[1]*S, -t)
                py5.end_shape()

    def edges(self):
        return pairwise(tuple(self.points) + (self.points[0],))


def draw_poly(pts, closed=True):
    S = 35.28
    py5.begin_shape()
    for p in pts:
        py5.vertex(p[0]*S, p[1]*S, 0)
    if closed:
        py5.end_shape(py5.CLOSE)
    else:
        py5.end_shape()


def pairwise(iterable):
    import itertools
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def glue_tab(p1, p2, tab_w=10, cut_ang=py5.QUARTER_PI/2):
    """
    draws a trapezoidal or triangular glue tab
    along edge defined by p1 and p2, with provided
    width (tab_w) and cut angle (cut_ang)
    """
    a1 = py5.atan2(p1[0] - p2[0], p1[1] - p2[1]) + cut_ang + py5.PI
    a2 = py5.atan2(p1[0] - p2[0], p1[1] - p2[1]) - cut_ang
    # calculate cut_len to get the right tab width
    cut_len = tab_w / py5.sin(cut_ang)
    f1 = (p1[0] + cut_len * py5.sin(a1),
          p1[1] + cut_len * py5.cos(a1))
    f2 = (p2[0] + cut_len * py5.sin(a2),
          p2[1] + cut_len * py5.cos(a2))
    edge_len = py5.dist(p1[0], p1[1], p2[0], p2[1])

    if edge_len > 2 * cut_len * py5.cos(cut_ang):  # 'normal' trapezoidal tab
        with py5.begin_shape():
            py5.vertex(*p1)  # vertex(p1[0], p1[1])
            py5.vertex(*f1)
            py5.vertex(*f2)
            py5.vertex(*p2)
    else:  # short triangular tab
        fm = ((f1[0] + f2[0]) / 2, (f1[1] + f2[1]) / 2)
        with py5.begin_shape():
            py5.vertex(*p1)
            py5.vertex(*fm)  # middle way of f1 and f2
            py5.vertex(*p2)


