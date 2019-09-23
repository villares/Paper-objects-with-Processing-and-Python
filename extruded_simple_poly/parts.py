

class Face:

    def __init__(self, points, thickness, orientation = (0, 0, 0)):
        self.points = points
        self.thickness = thickness
        self.o = orientation    
        
    def draw_2D(self):
        draw_poly(self.points)

    def draw_3D(self, rot):
        S = 35.28 

        t = self.thickness
        pts = self.points
        with pushMatrix():
            translate(0, height/2)
            rotateX(self.o[0] * 0 + rot)
            translate(0, -height/2)
            translate(0, 0, -t/2)
            fill(230)
            draw_poly(pts)
            translate(0, 0, t)
            fill(170)
            draw_poly(pts)
            fill(250)
            for p1, p2 in pairwise(tuple(pts) + (pts[0],)):
                # print((p1, p2))
                beginShape(QUAD_STRIP)
                vertex(p1[0]*S, p1[1]*S, 0)
                vertex(p1[0]*S, p1[1]*S, -t)
                vertex(p2[0]*S, p2[1]*S, 0)
                vertex(p2[0]*S, p2[1]*S, -t)
                endShape()
    
    def edges(self):
         return pairwise(tuple(self.points) + (self.points[0],))
     
def draw_poly(points, closed=True):
        S = 35.28 
        beginShape()
        for p in points:
            vertex(p[0]*S, p[1]*S, 0)                    
        if closed:
            endShape(CLOSE)
        else:
            endShape()
            

def pairwise(iterable):
    import itertools
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)     
   
def glue_tab(p1, p2, tab_w=10, cut_ang=QUARTER_PI/2):
    """
    draws a trapezoidal or triangular glue tab
    along edge defined by p1 and p2, with provided
    width (tab_w) and cut angle (cut_ang)
    """
    a1 = atan2(p1[0] - p2[0], p1[1] - p2[1]) + cut_ang + PI
    a2 = atan2(p1[0] - p2[0], p1[1] - p2[1]) - cut_ang
    # calculate cut_len to get the right tab width
    cut_len = tab_w / sin(cut_ang)
    f1 = (p1[0] + cut_len * sin(a1),
          p1[1] + cut_len * cos(a1))
    f2 = (p2[0] + cut_len * sin(a2),
          p2[1] + cut_len * cos(a2))
    edge_len = dist(p1[0], p1[1], p2[0], p2[1])

    if edge_len > 2 * cut_len * cos(cut_ang):  # 'normal' trapezoidal tab
        beginShape()
        vertex(*p1)  # vertex(p1[0], p1[1])
        vertex(*f1)
        vertex(*f2)
        vertex(*p2)
        endShape()
    else:  # short triangular tab
        fm = ((f1[0] + f2[0]) / 2, (f1[1] + f2[1]) / 2)
        beginShape()
        vertex(*p1)
        vertex(*fm)  # middle way of f1 and f2
        vertex(*p2)
        endShape()        
