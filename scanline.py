from graphics import *
import math
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

def Viewport(filename, xvmax, yvmax, w):
    
    viewport = GraphWin(filename, xvmax, yvmax)
    viewport.setBackground(color_rgb(0, 0, 0))
    viewport.setCoords(*w)
    return viewport

def inverseSlope(x1, y1, x2, y2):
    if x2-x1 == 0:
        return 0
    if y2-y1 == 0:
        return float('inf')

    return (x2-x1)/(y2-y1)


def createEdgeTable(vertices):

    edgeTable = dict()
    n = len(vertices)

    for i in range(n):
        x1, y1 = vertices[i%n]
        x2, y2 = vertices[(i+1)%n]
        y = min(y1, y2)
        if y2 - y1 == 0:
            continue
        #maxy, 1/m, min x1
        temp = [max(y1, y2), inverseSlope(x1, y1, x2, y2), x1 if y1 < y2 else x2]
        if y in edgeTable:
            edgeTable[y].append(temp)
        else:
            edgeTable[y] = [temp]

    return edgeTable

def ScanLine(win, vertices, w, vp):
    
    edgeTable = createEdgeTable(vertices)
    y = min(vertices, key= lambda x: x[1])[1]
    ymax = max(vertices, key=lambda x:x[1])[1]

    #ymax = max(temps, key=lambda x: x[0])
    #initialize aet
    aET = []
    while y < ymax:

        if y in edgeTable:
            for item in edgeTable[y]:
                aET.append(item)
            aET.sort(key = lambda x: x[2])

        for i in range(0, len(aET), 2):
            try:
                x1, x2 = math.ceil(aET[i][2]), math.floor(aET[i+1][2])
            except:
                break
            l = Line(Point(x1, y), Point(x2, y))
            l.setOutline('yellow')
            l.draw(win)
            aET[i][2] += aET[i][1]
            aET[i+1][2] += aET[i+1][1]

        y += 1

        for i, item in enumerate(aET):
            if item[0] < y:
                aET[i] = 0

        while 0 in aET:
            aET.remove(0)


def DrawAxis(viewport, w):

    xaxis = Line(Point(0, w[3]), Point(0, w[1]))
    xaxis.setOutline('red')
    xaxis.draw(viewport)

    yaxis = Line(Point(w[0], 0), Point(w[2], 0))
    yaxis.setOutline('red')
    yaxis.draw(viewport)

def main(argv):

    # xvmax, yvmax = map(int, input("Input Viewport Length Breadth (xvmax, yvmax)\n").split())
    # xwmin, ywmin = map(int, input("Input Window's min coordinates - (xwmin, ywmin)\n").split())
    # xwmax, ywmax = map(int, input("Input Window's max coordinates - (xwmax, ywmax)\n").split())
    print("Viewport 1000X1000")
    print("Window -500, -500, 500, 500")
    xvmax, yvmax, xwmin, ywmin = 1000, 1000, -500, -500
    xwmax, ywmax = 500, 500
    n = int(input("Enter the number of vertices of polygon\n"))
    vertices = []
    for i in range(n):
        x1, y1 = map(int, input("Input point (x1 y1)\n").split())
        vertices.append((x1, y1))

    w = (xwmin, ywmin, xwmax, ywmax)
    vp = (0, 0, xvmax, yvmax)

    viewport = Viewport(argv, xvmax, yvmax, w)

    DrawAxis(viewport, w)

    for i in range(n):
        l = Line(Point(vertices[i][0], vertices[i][1]), Point(vertices[(i+1)%n][0], vertices[(i+1)%n][1]))
        l.setOutline("white")
        l.draw(viewport)

    ScanLine(viewport, vertices, w, vp)

    viewport.getMouse()
    viewport.close()

if __name__ == "__main__":
    main(sys.argv[0])
