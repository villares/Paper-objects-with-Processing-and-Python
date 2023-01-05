import py5

CUT_STROKE = py5.color(255, 0, 0)


def unfold_tri_face(pts_2D, pts_3D):
    """
    gets a collection of 2 (B, C) starting 2D points (Py5Vectors or tuples)
    gets a collection of 4 (A, B, C, D) 3D points (p_vectors or tuples)
    draws the unfolded face and returns (A, D) 2D positions.
    """
    b2D, c2D = pts_2D
    a3D, b3D, c3D, d3D = pts_3D
    bd_len = py5.dist(b3D[0], b3D[1], b3D[2], d3D[0], d3D[1], d3D[2])
    cd_len = py5.dist(c3D[0], c3D[1], c3D[2], d3D[0], d3D[1], d3D[2])
    # lower triangle
    d2D = third_point(b2D, c2D, bd_len, cd_len)[
        0]  # gets the first solution
    line_draw(b2D, c2D)
    line_draw(d2D, c2D, tab=True)
    # upper triangle (fixed from 190408a)
    ab_len = py5.dist(b3D[0], b3D[1], b3D[2], a3D[0], a3D[1], a3D[2])
    ad_len = py5.dist(a3D[0], a3D[1], a3D[2], d3D[0], d3D[1], d3D[2])
    # gets the 1st solution too!
    a2D = third_point(b2D, d2D, ab_len, ad_len)[0]
    line_draw(b2D, a2D, tab=True)
    # line_draw(d2D, a2D)
    return (a2D, d2D)


def third_point(a, b, ac_len, bc_len):
    """
    Adapted from code by monkut https://stackoverflow.com/users/24718/monkut
    at https://stackoverflow.com/questions/4001948/drawing-a-triangle-in-a-coordinate-plane-given-its-three-sides
    for use with processing python mode - using p_vectors

    returns two point c options given:
    point a, point b, ac length, bc length
    """
    class NoTrianglePossible(BaseException):
        pass

    # To allow use of tuples, creates or recreates PVectors
    a, b = py5.Py5Vector(*a), py5.Py5Vector(*b)
    # check if a triangle is possible
    ab_len = a.dist(b)
    if ab_len > (ac_len + bc_len) or ab_len < abs(ac_len - bc_len):
        raise no_triangle_possible("The sides do not form a triangle")

    # get the length to the vertex of the right triangle formed,
    # by the intersection formed by circles a and b
    ad_len = (ab_len ** 2 + ac_len ** 2 - bc_len ** 2) / (2.0 * ab_len)
    # get the height of the line at a right angle from a_len
    h = py5.sqrt(abs(ac_len ** 2 - ad_len ** 2))

    # Calculate the mid point d, needed to calculate point c(1|2)
    d = py5.Py5Vector(a.x + ad_len * (b.x - a.x) / ab_len,
                      a.y + ad_len * (b.y - a.y) / ab_len)
    # get point c locations
    c1 = py5.Py5Vector(d.x + h * (b.y - a.y) / ab_len,
                       d.y - h * (b.x - a.x) / ab_len)
    c2 = py5.Py5Vector(d.y + h * (b.x - a.x) / ab_len,
                       d.x - h * (b.y - a.y) / ab_len)
    return c1, c2


def line_draw(p1, p2, tab=False):
    """
    sugar for drawing lines from 2 "points" (tuples or p_vectors)
    may also draw a glue tab suitably marked for cutting.
    """
    py5.line(p1[0], p1[1], p2[0], p2[1])
    if tab:
        with py5.push_style():
            py5.stroke(CUT_STROKE)
            glue_tab(p1, p2)


def glue_tab(p1, p2, tab_w=10, cut_ang=py5.QUARTER_PI):
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
        line_draw(p1, f1)
        line_draw(f1, f2)
        line_draw(f2, p2)
    else:  # short triangular tab
        fm = ((f1[0] + f2[0]) / 2, (f1[1] + f2[1]) / 2)
        line_draw(p1, fm)
        line_draw(fm, p2)

DEBUG = True

def debug_text(name, pts, enum=False):
    if DEBUG:
        for i, p in enumerate(pts):
            with py5.push():

                py5.fill(255, 0, 0)
                if enum:
                    py5.translate(0, -5, 10)
                    py5.text(name + "-" + str(i), *p)
                else:
                    py5.translate(10, 10, 10)
                    py5.text(name[i], *p)


def poly_draw(pts, force_z=None, closed=True):
    """ sugar for face drawing """
    py5.begin_shape()
    for p in pts:
        if force_z is None:
            py5.vertex(*p)
        else:
            py5.vertex(p[0], p[1], force_z)
    if closed:
        py5.end_shape(py5.CLOSE)
    else:
        py5.end_shape()


def triangulated_face(*args):
    if len(args) == 4:
        a, b, c, d = args
        print("face")
    else:
        a, b, c, d = args[0]
    # two triangles - could be with a diferent diagonal!
    # TODO: let one choose diagonal orientation
    py5.stroke(0)
    poly_draw((a, b, d))
    poly_draw((b, d, c))


def test():
    #size(600, 400, P3D)
    p3D = [(50, 100, 0), (200, 100, 0), (200, 200, 0), (100, 300, -100)]
    debug_text("ABCD", p3D)
    py5.begin_shape()
    for p in p3D:
        py5.vertex(*p)
    py5.end_shape(py5.CLOSE)
    x0, y0, z0 = p3D[1]
    x2, y2, z2 = p3D[3]
    py5.line(x0, y0, z0, x2, y2, z2)
    print(py5.dist(x0, y0, z0, x2, y2, z2))

    p2D = [(250, 100), (250, 200)]
    bx, by = p2D[0]
    debug_text("BC", p2D)
    for i in range(1):
        p2D = unfold_tri_face(p2D, p3D)
    print(p2D)
    debug_text("AD", p2D)
    dx, dy, _ = p2D[1]
    print(py5.dist(bx, by, dx, dy))

