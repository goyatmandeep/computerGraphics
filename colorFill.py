from graphics import *
filled = set()
stack = []
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


def line(x0, y0, x1, y1, win, w, vp):

    if(x1-x0 == 0):
        slope = None
        (x0,y0) = (y0,x0)
        (x1,y1) = (y1,x1)
    else:
        slope = (y1-y0)/(x1-x0)
        if(slope >= 0) and (abs(slope) > 1):
            (x0,y0) = (y0,x0)
            (x1,y1) = (y1,x1)
        elif(slope < 0) and (abs(slope) <= 1):
            (x0,y0) = (-x0,y0)
            (x1,y1) = (-x1,y1)
        elif(slope < 0) and (abs(slope) > 1):
            (x0,y0) = (y0,-x0)
            (x1,y1) = (y1,-x1)
    if(x0 > x1):
        (xt,yt) = (x0,y0)
        (x0,y0) = (x1,y1)
        (x1,y1) = (xt,yt)
    
    a = y1 - y0
    b = x0-x1
    E, NE = a, a + b

    d = a + (b/2)
    x = x0 ; y = y0
   
    while(x <= x1):
        if(slope is None):
            (xp,yp) = (y,x)
        elif(slope >= 0) and (abs(slope) > 1):
            (xp,yp) = (y,x)
        elif(slope < 0) and (abs(slope) <= 1):
            (xp,yp) = (-x,y)
        elif(slope < 0) and (abs(slope) > 1):
            (xp,yp) = (-y,x)
        else:
            (xp,yp) = (x,y)
        xp, yp = wintoview(xp, yp, w, vp)
        win.plotPixel(xp, yp,"white")
        filled.add((xp, yp))
       
        if(d<0):
            d = d + E
        else:
            d = d + NE
            y = y + 1
        x = x + 1

def Viewport(filename, xvmax, yvmax, w):
    
    viewport = GraphWin(filename, xvmax, yvmax)
    viewport.setBackground(color_rgb(0, 0, 0))
    viewport.setCoords(*w)
    return viewport

def FloodFill(win, x, y, w, vp):
    stack.append((x, y))
    while len(stack) != 0:
        x, y = stack.pop()
        if (x, y) not in filled:
            win.plotPixel(x, y, "yellow")
            filled.add((x, y))
            if (x+1, y) not in filled:
                stack.append((x+1, y))
            if (x, y+1) not in filled:
                stack.append((x, y+1))
            if (x-1, y) not in filled:
                stack.append((x-1, y))
            if (x, y-1) not in filled:
                stack.append((x, y-1))
    

def DrawAxis(viewport, w):

    xaxis = Line(Point(0, w[3]), Point(0, w[1]))
    xaxis.setOutline('red')
    xaxis.draw(viewport)

    yaxis = Line(Point(w[0], 0), Point(w[2], 0))
    yaxis.setOutline('red')
    yaxis.draw(viewport)

def main(argv):

    xvmax, yvmax = map(int, input("Input Viewport Length Breadth (xvmax, yvmax)\n").split())
    xwmin, ywmin = map(int, input("Input Window's min coordinates - (xwmin, ywmin)\n").split())
    xwmax, ywmax = map(int, input("Input Window's max coordinates - (xwmax, ywmax)\n").split())
    n = int(input("Enter the number of edges of polygon\n"))
    edges = []
    for i in range(n):
        x1, y1 = map(int, input("Input point (x1 y1)\n").split())
        edges.append((x1, y1))

    xs, ys = map(int, input("Enter a point within the polygon").split())

    w = (xwmin, ywmin, xwmax, ywmax)
    vp = (0, 0, xvmax, yvmax)

    viewport = Viewport(argv, xvmax, yvmax, w)

    DrawAxis(viewport, w)

    for i in range(n-1):
        line(edges[i][0], edges[i][1], edges[i+1][0], edges[i+1][1], viewport, w, vp)
    line(edges[-1][0], edges[-1][1], edges[0][0], edges[0][1], viewport, w, vp)

    xs, ys = wintoview(xs, ys, w, vp)
    FloodFill(viewport, xs, ys, w, vp)

    viewport.getMouse()
    viewport.close()

if __name__ == "__main__":
    main(sys.argv[0])
