CORTE, VINCO = color(255, 0, 0), color(0, 0, 255)

def setup():
    size(600, 600, P3D)

def draw():
    background(200)
    translate(300, 300)
    caixa_desdobrada(250, 150, 100)

def caixa_desdobrada(w, h, d):
        mw, mh, md =  w/2., h/2., d/2.
        face_2D(0, -h -md, w, d, "aaan")
        face_2D(0, -mh, w, h, "vvvv")
        face_2D(0, -mh + mh + md, w, d, "cncv")
        face_2D(0, +mh + d, w, h, "cncc")
        face_2D(-mw -md, -mh, d, h, "acna")
        face_2D(mw + md, -mh, d, h, "ncaa")     

def face_2D(x, y, w, h, lados):
    l0, l1, l2, l3 = lados
    mw, mh = w/2., h/2.
    pushMatrix()
    translate(x, y)
    my_line(-mw, +mh, -mw, -mh, l0)
    my_line(-mw, -mh, +mw, -mh, l1)
    my_line(+mw, -mh, +mw, +mh, l2)
    my_line(+mw, +mh, -mw, +mh, l3)
    popMatrix()
         
def my_line(x0, y0, x1, y1, tipo):
    if tipo == "n":
        return
    elif tipo == "c":
        stroke(CORTE)
    else:
        stroke(VINCO)
    line(x0, y0, x1, y1)
    if tipo == "a":
        stroke(CORTE)
        noFill()
        glue_tab((x0, y0), (x1, y1), 10)
        
def glue_tab(p1, p2, tab_w, cut_ang=QUARTER_PI/3):
    """
    draws a trapezoidal or triangular glue tab along edge defined by p1 and p2,
    with width tab_w and cut angle a
    """
    al = atan2(p1[0] - p2[0], p1[1] - p2[1])
    a1 = al + cut_ang + PI
    a2 = al - cut_ang
    # calculate cut_len to get the right tab width
    cut_len = tab_w / sin(cut_ang)
    f1 = (p1[0] + cut_len * sin(a1),
                p1[1] + cut_len * cos(a1))
    f2 = (p2[0] + cut_len * sin(a2),
                p2[1] + cut_len * cos(a2))
    edge_len = dist(p1[0], p1[1], p2[0], p2[1])

    if edge_len > 2 * cut_len * cos(cut_ang):    # 'normal' trapezoidal tab
            beginShape()
            vertex(*p1)    # vertex(p1[0], p1[1])
            vertex(*f1)
            vertex(*f2)
            vertex(*p2)
            endShape()
    else:    # short triangular tab
            fm = ((f1[0] + f2[0]) / 2, (f1[1] + f2[1]) / 2)
            beginShape()
            vertex(*p1)
            vertex(*fm)    # middle way of f1 and f2
            vertex(*p2)
            endShape()    
