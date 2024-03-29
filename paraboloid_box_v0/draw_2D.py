import py5

from draw_3D import poly_draw
from debug import debug_text

CUT_COLOR = py5.color(255, 0, 0)  # Color to mark outline cut
ENG_COLOR = py5.color(0, 0, 255)  # Color to mark folding/engraving
TAB_W = 10  # glue tab width
TAB_A = py5.radians(30)  # glue tab angle


def draw_unfolded(box_w, box_d, ab_l, cd_l, face_data):
    """
    main 2D drawing procedure
    takes 2 box dimentions, 2 top point height lists,
    and a collection of 3D points (face_data) from the 3D procedure
    then draws the unfolded version of the volume with glue tabs
    """
    ah, bh, ch, dh = ab_l[0], ab_l[-1], cd_l[0], cd_l[-1]
    ah_2d,  a0_2d = (box_w * 2 + box_d, -ah), (box_w * 2 + box_d, 0)
    bh_2d, b0_2d = (0, -bh), (0, 0)
    ch_2d, c0_2d = (box_w, -ch), (box_w, 0)
    dh_2d, d0_2d = (box_w + box_d, -dh), (box_w + box_d, 0)

    py5.no_fill()
    # Marked for folding
    py5.stroke(ENG_COLOR)
    # verticals
    line_draw(b0_2d, bh_2d)
    line_draw(c0_2d, ch_2d)
    line_draw(d0_2d, dh_2d)
    line_draw(a0_2d, ah_2d)
    debug_text("BCDA", (bh_2d, ch_2d, dh_2d, ah_2d))

    # divided top face - also draws some CUT_COLOR glue tabs!
    start_1, start_2 = bh_2d, ch_2d
    for a_3d, b_3d, c_3d, d_3d in face_data:
        start_1, start_2 = unfold_tri_face((start_1, start_2),
                                           (a_3d, b_3d, c_3d, d_3d))

    # top tab
    line_draw(start_1, start_2, tab=True)
    # floor face
    py5.rect(0, 0, box_w, box_d)

    # Marked for cutting
    py5.stroke(CUT_COLOR)
    # middle tab
    glue_tab(b0_2d, bh_2d, TAB_W, TAB_A)
    # floor tabs
    glue_tab((0, box_d), b0_2d, TAB_W, TAB_A)
    glue_tab((box_w, box_d), (0, box_d), TAB_W, TAB_A)
    glue_tab((box_w, 0), (box_w, box_d), TAB_W, TAB_A)
    # main outline cut
    num_pts = len(cd_l)
    cd_2_dpts = [(box_w + box_d * i / (num_pts - 1), -cd_l[i])
                 for i in range(num_pts)]
    ab_2_dpts = [(box_w * 2 + box_d + box_d * i / (num_pts - 1), -ab_l[i])
                 for i in range(num_pts)]
    main_outline = cd_2_dpts + ab_2_dpts + [(box_w * 2 + box_d * 2, 0), c0_2d]
    poly_draw(main_outline, closed=False)


def line_draw(p1, p2, tab=False):
    """
    sugar for drawing lines from 2 "points" (tuples or PVectors)
    may also draw a glue tab suitably marked for cutting.
    """
    py5.line(p1[0], p1[1], p2[0], p2[1])
    if tab:
        with py5.push_style():
            py5.stroke(CUT_COLOR)
            glue_tab(p1, p2, TAB_W, TAB_A)


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
    f1 = py5.Py5Vector(p1[0] + cut_len * py5.sin(a1),
                       p1[1] + cut_len * py5.cos(a1))
    f2 = py5.Py5Vector(p2[0] + cut_len * py5.sin(a2),
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


def unfold_tri_face(pts_2_d, pts_3_d):
    """
    gets a collection of 2 (B, D) starting 2D points (PVectors or tuples)
    Gets a collection of 4 (A, B, C, D) 3D points (PVectors or tuples)
    Draws the unfolded face a returns (A, C) 2D positions.
    """
    b2_d, c2_d = pts_2_d
    a3_d, b3_d, c3_d, d3_d = pts_3_d
    bd_len = py5.dist(b3_d[0], b3_d[1], b3_d[2], d3_d[0], d3_d[1], d3_d[2])
    cd_len = py5.dist(c3_d[0], c3_d[1], c3_d[2], d3_d[0], d3_d[1], d3_d[2])
    # lower triangle
    d2_d = third_point(b2_d, c2_d, bd_len, cd_len)[
        0]  # gets the first solution
    line_draw(b2_d, c2_d)
    line_draw(b2_d, d2_d)
    line_draw(d2_d, c2_d, tab=True)
    # upper triangle (fixed from 190408a)
    ab_len = py5.dist(b3_d[0], b3_d[1], b3_d[2], a3_d[0], a3_d[1], a3_d[2])
    ad_len = py5.dist(a3_d[0], a3_d[1], a3_d[2], d3_d[0], d3_d[1], d3_d[2])
    # gets the 1st solution too!
    a2_d = third_point(b2_d, d2_d, ab_len, ad_len)[0]
    line_draw(b2_d, a2_d, tab=True)
    line_draw(d2_d, a2_d)
    return (a2_d, d2_d)


def third_point(a, b, ac_len, bc_len):
    """
    Adapted from code by Monkut https://stackoverflow.com/users/24718/monkut
    at https://stackoverflow.com/questions/4001948/drawing-a-triangle-in-a-coordinate-plane-given-its-three-sides

    Returns two point c options given:
    point a, point b, ac length, bc length
    """
    class NoTrianglePossible(BaseException):
        pass

    # To allow use of tuples, creates or recreates PVectors
    a, b = py5.Py5Vector(*a), py5.Py5Vector(*b)
    # check if a triangle is possible
    ab_len = a.dist(b)
    if ab_len > (ac_len + bc_len) or ab_len < abs(ac_len - bc_len):
        raise NoTrianglePossible("The sides do not form a triangle")

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

