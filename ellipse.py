from graphics import *
import sys

def wintoview(xw, yw, w, vp):

    (xwmin,ywmin,xwmax,ywmax) = w
    (xvmin,yvmin,xvmax,yvmax) = vp

    xscale = (xw - xwmin)/(xwmax - xwmin)
    xbias = xscale*(xvmax - xvmin)
    xv = round(xbias + xvmin)

    yscale = (yw - ywmin)/(ywmax - ywmin)
    ybias = yscale*(yvmax - yvmin)
    yv = ybias + yvmin
    yv = round(yvmax - yv)

    return xv, yv

def Points(x, y, a, b, win, w, vp):
    win.plotPixel(*wintoview(x+a,y+b, w, vp),"white")
    win.plotPixel(*wintoview(-x+a,y+b, w, vp),"white")
    win.plotPixel(*wintoview(x+a,-y+b, w, vp),"white")
    win.plotPixel(*wintoview(-x+a,-y+b, w, vp),"white")

def Ellipse(a, b, x0, y0, w, vp, win):
    x, y = 0, b
    asq = a*a
    bsq = b*b
    d1 = (bsq) - (asq*b) + (0.25*asq)
    dx = 2*bsq*x
    dy = 2*asq*y

    while (dx < dy):
        Points(x,y,x0,y0,win, w, vp)
        if d1 < 0:
            dx +=  (2*bsq)
            d1 += dx + bsq
        else:
            y=y-1;
            dx += (2 * bsq)
            dy -= (2 * asq)
            d1 += dx - dy + (b * b)
        x += 1
        
    d2 = ((bsq) * ((x + 0.5) * (x + 0.5))) + (asq * ((y - 1) * (y - 1))) - (asq*bsq)
    
    while y >= 0:
        Points(x, y, x0, y0, win, w, vp)
        if d2 > 0:
            dy = dy - (2 * asq)
            d2 = d2 + asq - dy
        else:
            x += 1
            dx = dx + (2 * bsq)
            dy = dy - (2 * asq)
            d2 = d2 + dx - dy + (a * a)
        y=y-1


def Viewport(filename, xvmax, yvmax, w):
    
    viewport = GraphWin(filename, xvmax, yvmax)
    viewport.setBackground(color_rgb(0, 0, 0))
    viewport.setCoords(*w)
    return viewport


def DrawAxis(viewport, w):

    xaxis = Line(Point(0, w[3]), Point(0, w[1]))
    xaxis.setOutline('red')
    xaxis.draw(viewport)

    yaxis = Line(Point(w[0], 0), Point(w[2], 0))
    yaxis.setOutline('red')
    yaxis.draw(viewport)


def main(argv):

    xvmax, yvmax = map(int, input("Input Viewport Length Breadth (xvmax, yvmax)\n").split()) 
    xwmin, ywmin = map(int, input("Input Window's min coordinate (xwmin, ywmin)\n").split())
    xwmax, ywmax = map(int, input("Input Window's max coordinate (xwmax, ywmax)\n").split())

    w = (xwmin, ywmin, xwmax, ywmax)
    vp = (0, 0, xvmax, yvmax)

    a, b = map(int, input("Input semimajor axis, semi-minor axis (a, b)\n").split())
    x1, y1 = map(int, input("Input center (x1 y1)\n").split())

    viewport = Viewport(argv, xvmax, yvmax, w)
    DrawAxis(viewport, w)

    Ellipse(a, b, x1, y1, w, vp, viewport)
    viewport.getMouse()
    viewport.close()

if __name__ == "__main__":
    main(sys.argv[0])