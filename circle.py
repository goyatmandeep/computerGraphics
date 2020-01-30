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
    

def Circle(r, cx, cy, w, vp, win):
    x=0
    y=r
    d=1.25-r
    while(x<y):
        win.plotPixel(*wintoview(cx+x,cy+y, w, vp), "white")
        win.plotPixel(*wintoview(cx+y,cy+x, w, vp), "white")
        win.plotPixel(*wintoview(cx-x,cy+y, w, vp), "white")
        win.plotPixel(*wintoview(cx+x,cy-y, w, vp), "white")
        win.plotPixel(*wintoview(cx-x,cy-y, w, vp), "white")
        win.plotPixel(*wintoview(cx+y,cy-x, w, vp), "white")
        win.plotPixel(*wintoview(cx-y,cy+x, w, vp), "white")
        win.plotPixel(*wintoview(cx-y,cy-x, w, vp), "white")

        if(d<0):
            x=x+1
            d=d+2*x+3
        else:
            x=x+1
            y=y-1
            d=d+2*x-2*y+5


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
    xwmin, ywmin = map(int, input("Input Window's min coordinates (xwmin, ywmin)\n").split())
    xwmax, ywmax = map(int, input("Input Window's max coordinates (xwmax, ywmax)\n").split())
    r, x1, y1 = map(int, input("Input radius and center (r, x1 y1)\n").split())


    w = (xwmin, ywmin, xwmax, ywmax)
    vp = (0, 0, xvmax, yvmax)
    
    viewport = Viewport(argv, xvmax, yvmax, w)

    DrawAxis(viewport, w)
    
    Circle(r, x1, y1, w, vp, viewport)
    viewport.getMouse()
    viewport.close()

if __name__ == "__main__":
    main(sys.argv[0])