"""
Box with rectangular holes
based on face_2D
"""

def setup():
    size(500, 500, P3D)

def draw():
    background(200)
    # Face
    face_2D(250, 100, 250, 150, 15)
    # Caixa
    translate(250, 300)
    rotateX(QUARTER_PI)
    caixa(250, 150, 100, 15)
    
def face_2D(x, y, w, h, e=0, closed=True):
    mw, mh = w/2., h/2.
    pushMatrix()
    translate(x, y)
    beginShape()
    vertex(-mw, -mh)
    vertex(+mw, -mh)
    vertex(+mw, +mh)
    vertex(-mw, +mh)
    if e > 0 and mw - e > 0 and mh - e > 0:
        mw -= e
        mh -= e
        beginContour()
        vertex(-mw, -mh)
        vertex(-mw, +mh)        
        vertex(+mw, +mh)
        vertex(+mw, -mh)
        endContour()
    if closed:
        endShape(CLOSE)
    else:
        endShape()
    popMatrix()
    
    
def caixa(w, h, d, e=0):
     mw, mh, md = w/2., h/2., d/2.
     translate(0, 0, -md) # base
     face_2D(0, 0, w, h, e)
     translate(0, 0, d) # topo
     face_2D(0, 0, w, h, e)
     translate(0, 0, -md) # volta
     rotateY(HALF_PI)
     translate(0, 0, -mw) # lateral e
     face_2D(0, 0, d, h, e)
     translate(0, 0, w) # lateral d
     face_2D(0, 0, d, h, e)
     translate(0, 0, -mw) # volta    
     rotateY(-HALF_PI)  # volta
     rotateX(HALF_PI)
     translate(0, 0, -mh) # lateral e
     face_2D(0, 0, w, d, e)
     translate(0, 0, h) # lateral d
     face_2D(0, 0, w, d, e)
     translate(0, 0, -mw) # volta         
     rotateX(-HALF_PI)
     
def keyPressed():
    saveFrame("#.png")
