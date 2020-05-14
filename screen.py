from matrix import *
from vector import *
from subprocess import Popen, PIPE
from os import remove
from math import cos, sin, atan2, pi, factorial, pow
import copy 
import random
class screen:
    DEFAULT = [255,255,255]
    DRAW = [0,0,0]
    AMBIENT = [.5,.5,.5]
    DIFFUSE = [.5,.5,.5]
    SPECULAR = [.4,.4,.4]
    AMBCOLOR = [50,50,50]
    SCOLOR = [255,255,255]
    LSOURCE = [499,490,20]
    VIEW = vector(0,0,1)
    SPEC = 3
    def updateColor(self,symbols,reflect):
        colors = ['red','green','blue']
        r = symbols[reflect][1]
        for c in range(3):
            screen.AMBIENT[c]=r[colors[c]][0]
            screen.DIFFUSE[c]=r[colors[c]][1]
            screen.SPECULAR[c]=r[colors[c]][2]
        #print ("set",screen.AMBIENT,screen.DIFFUSE,screen.SPECULAR)
    def __init__(self, h=500, w=500):
        self.pixels = [[screen.DEFAULT[:] for i in range(w)] for i in range(h)]
        self.zbuff = [[float("-inf") for i in range(w)] for i in range(h)]
        self.height = h
        self.width = w
        #master matrices
        self.tfrm = matrix()
        self.stack = [self.tfrm]
        self.tfrm.ident()
        self.edge = matrix()

        self.poly = matrix()
    def clear(self):
        for h in range(self.height):
            for w in range(self.width):
                self.pixels[h][w] = screen.DEFAULT[:]
        self.edge.data = []
        self.tfrm.ident()
        self.poly.data = []
    def toFile(self,file):
        enter = "P6\n{} {}\n255\n".format(self.height, self.width)
        with open(file, "wb") as f:
            f.write(enter.encode())
            for h in range(self.height)[::-1]:
                for w in range(self.width):
                    c = self.pixels[h][w]
                    f.write(bytes(c))
    def toFileAscii(self,file):
        enter = "P3\n{} {}\n255\n".format(self.height, self.width)
        for i in self.pixels[::-1]:
            row = ""
            for p in i:
                row += str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + " " #the color of the pixel
            enter += row + "\n"
        with open(file, "w+") as f:
            f.write(enter)
    def printIt(self):
        enter = "P3\n{} {}\n255\n".format(self.height, self.width)
        for i in self.pixels:
            row = ""
            for p in i:
                row += p.getColor() + " "
            enter += row + "\n"
        print(enter)
    def allPix(self, funct): #funct is a function that takes in a pixel and modifies it
        for h in self.height:
            for w in self.width:
                funct(self.pixels[h][w])
    def allPixCoord(self, funct):
        for h in range(self.height):
            for w in range(self.width):
                funct(w,h,self.pixels[w][h])
    def plot(self,w,h,z=0,color = None):
        #print(h,w)
        if color == None:
            color = screen.DRAW[:]
        try:
            if (z > self.zbuff[int(h)][int(w)]) and int(w) > 0 and int(h) > 0:
                #print (w,h)
                self.pixels[int(h)][int(w)] = color[:]
                self.zbuff[int(h)][int(w)] = z
                #if w < 0 or h < 0: 
                #    print ("uh oh")
        except IndexError:
            #print("ERROR:",h,w)
            None
    def plotL(self,l,color = DEFAULT[:]):
        try:
            if (int(l[0]) > 0 and l[1] > 0):
                self.pixels[int(l[0])][int(l[1])] = color[:]
        except IndexError:
            print("ERROR:",h,w)
    def _Q1(self,x1,y1,x2,y2,color):
        a = y2 - y1
        b = -(x2-x1)
        d = 2*a + b
        while x1 < x2:
            self.plot(x1,y1,color)
            if d > 0:
                y1 += 1
                d += 2*b
            x1+=1
            d+=2*a
    def _Q2(self,x1,y1,x2,y2,color):
        a = y2 - y1
        b = -(x2-x1)
        d = a + 2*b
        while y1 < y2:
            self.plot(x1,y1,color)
            if d < 0:
                x1+=1
                d+=2*a
            y1 += 1
            d += 2*b
    def _Q3(self,x1,y1,x2,y2,color):
        #print("Q3")
        a = y2 - y1
        b = -(x2-x1)
        d = a - 2*b
        #print(a,b,d)
        while y1 > y2:
            self.plot(x1,y1,color)
            if d > 0:
                x1+=1
                d+=2*a
            y1 -= 1
            d -= 2*b
    def _Q4(self,x1,y1,x2,y2,color):
        #print("q4")
        a = y2 - y1
        b = -(x2-x1)
        d = 2*a - b
        while x1 < x2:
            #print("({},{})".format(x1,y1))
            #print(d)
            self.plot(x1,y1,color)
            if d < 0:
                y1 -= 1
                d -= 2*b
            x1+=1
            d+=2*a
    def line(self,x1,y1,x2,y2,color):
        c = [[x1,y1], [x2,y2]]
        c.sort()

        x1,x2 = c[0][0],c[1][0]
        y1,y2 = c[0][1],c[1][1]

        #print("({},{}) ({},{})".format(x1,y1,x2,y2))
        m = 2
        if (x2 != x1):
            m = (y2-y1)/(x2-x1)
        #print(m)
        if (m <= 1 and m > 0):
            self._Q1(x1,y1,x2,y2,color)
        elif(m > 1):
            self._Q2(x1,y1,x2,y2,color)
        elif(m < -1):
            self._Q3(x1,y1,x2,y2,color)
        else:
            self._Q4(x1,y1,x2,y2,color)
    def circle(self,x,y,z,r,steps = 35):
        step = 1/steps
        t = 0
        p1 = [x,y,z]
        p2 = [x + r * cos(2*pi * t), y + r * sin(2*pi * t),z]
        for i in range(steps+1):
            p1 = p2[:]
            p2 = [x + r * cos(2*pi * t), y + r * sin(2*pi * t),z]
            t+=step
            self.edge.addLine(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2])
    def bezier(self,x0,y0,x1,y1,influence,steps):
        #influence is a list of points in the form [x,y]
        step = 1/steps
        t = 0
        p1 = []
        p2 = [x0,y0]
        influence.append([x1,y1])
        influence.insert(0,[x0,y0])
        pwr = len(influence) - 1
        if (len(influence) == 1):
            None
        #elif pwr == 3:
        #    ax = (-x0 + 3
        else:
            for i in range(steps+1):
                #print(t)
                p1 = p2[:]
                p2 = [0,0]
                for n in range(2):
                    #print("***")
                    for p in range(len(influence)):
                        p2[n] += self.__nCr(pwr,p) * ((1-t)**(pwr-p)) * ((t)**(p)) * influence[p][n]
                        #print(self.__nCr(pwr,p),pwr-p, p,n )
                self.edge.addLine(p1[0],p1[1],0,p2[0],p2[1],0)
                t+=step
    def hermite(self, x0, y0, x1, y1, rx0, ry0, rx1, ry1, steps):
        step = 1/steps
        t = 0
        
        ax = 2*x0 - 2*x1 + rx0 + rx1
        ay = 2*y0 - 2*y1 + ry0 + ry1
        bx = -3*x0 + 3*x1 - 2*rx0 - rx1
        by = -3*y0 + 3*y1 - 2*ry0 - ry1
        cx = rx0
        cy = ry0
        dx = x0
        dy = y0
        p1 = []
        p2 = [x0,y0]
        for i in range(steps+1):
            #print(t)
            p1 = p2[:]
            p2 = [ax*t**3 + bx*t**2 + cx*t + dx,ay*t**3 + by*t**2 + cy*t + dy]
            self.edge.addLine(p1[0],p1[1],0,p2[0],p2[1],0)
            t+=step
    def box(self,x,y,z,l, h, d): #length height depth
        x1 = x + l
        y1 = y - h
        z1 = z - d
        
        self.add_poly_direct(x,y,z,x,y1,z,x1,y,z)
        self.add_poly_direct(x,y1,z,x1,y1,z,x1,y,z)
        
        self.add_poly_direct(x,y,z1,x1,y,z1,x,y1,z1)
        self.add_poly_direct(x,y1,z1,x1,y,z1,x1,y1,z1)
        
        self.add_poly_direct(x,y,z1,x,y1,z1,x,y1,z)
        self.add_poly_direct(x,y,z1,x,y1 ,z,x,y,z)
        
        self.add_poly_direct(x1,y,z,x1,y1,z,x1,y,z1)
        self.add_poly_direct(x1,y,z1,x1,y1,z,x1,y1,z1)
        
        self.add_poly_direct(x,y,z1,x,y,z,x1,y,z1)
        self.add_poly_direct(x,y,z,x1,y,z,x1,y,z1)
  
        self.add_poly_direct(x1,y1,z1,x1,y1,z,x,y1,z)
        self.add_poly_direct(x,y1,z,x,y1,z1,x1,y1,z1)


    def sphere(self,x,y,z,radius,steps = 30):
        points = self._spherePoints(x,y,z,radius,steps).data
        ps = len(points)
        for semi in range(steps):
            for p in range(semi * (steps+1),(semi+1) * (steps+1)):
                if p == semi * (steps+1):
                    self.add_polyL(points[p],points[p+1],points[(p+steps+1)%ps])
                elif p ==  (semi+1) * (steps+1) - 1:
                    self.add_polyL(points[p],points[(p+steps+1)%ps],points[(p+steps)%ps])
                else:
                    self.add_polyL(points[p],points[p+1],points[(p+steps+1)%ps])
                    self.add_polyL(points[p],points[(p+steps+1)%ps],points[(p+steps)%ps])
        # while p < len(points):
        #     while p < smc * steps:
        #         if p-1 % ps == 0 or p == 0:
        #             self.add_polyL(points[p],points[p+1],points[(p+steps+1)%ps])
        #         elif p+1 % steps == 0:
        #             self.add_polyL(points[p],points[(p+steps+1)%ps],points[(p+steps)%ps])
        #         else:
        #             self.add_polyL(points[p],points[p+1],points[(p+steps+1)%ps])
        #             self.add_polyL(points[p],points[(p+steps+1)%ps],points[(p+steps)%ps])
        #         p+=1
        #     p+=1
        #     smc += 1
    def _spherePoints(self,x,y,z,radius,steps):
        points = matrix()

        step = 1/steps
        r = radius
        for phi in range(steps):
            p = phi * step * 2 * pi
            for theta in range(steps + 1):
                the = theta * step * pi
                hx =  r*cos(the) + x
                hy = r*sin(the)*cos(p) + y
                hz = r*sin(the)*sin(p) + z
                points.addPoint(hx,hy,hz) 
        return points
    def pointySphere(self,x,y,z,radius,steps):
        step = 1/steps
        r = radius
        for phi in range(steps):
            p = phi * step * 2 * pi
            for theta in range(steps + 1):
                the = theta * step * pi
                hx =  r*cos(the) + x
                hy = r*sin(the)*cos(p) + y
                hz = r*sin(the)*sin(p) + z
                self.edge.addLine(hx+1,hy+1,hz+1,hx,hy,hz) 
    def pointyTorus(self,x,y,z,r1,r2,steps = 40):
        step = 1/steps
        for phi in range(steps + 1):
            p = phi * step * 2 * pi
            for theta in range(steps + 1):
                the = theta * step * 2 * pi
                hx =  cos(p) * (r1*cos(the) + r2) + x
                hy = r1*sin(the) + y
                hz = -1 * sin(p) * (r1*cos(the) + r2) + z
                self.edge.addLine(hx+1,hy+1,hz+1,hx,hy,hz) 
    def torus(self,x,y,z,r1,r2,steps = 28):
        points =self.__torusPoints(x,y,z,r1,r2,steps).data
        ps = len(points)
        for semi in range(steps):
            for p in range(semi * (steps+1), (semi+1) * (steps+1)):
                #self.add_polyL(points[p],points[p+1],points[(p+steps+1)%ps])
                #self.add_polyL(points[p],points[(p+steps+1)%ps],points[(p+steps)%ps])
                self.add_polyL(points[p+1],points[p],points[(p+steps+1)%ps])
                self.add_polyL(points[(p+steps+1)%ps],points[p],points[(p+steps)%ps])
    def __torusPoints(self,x,y,z,r1,r2,steps):
        points = matrix()
        step = 1/steps
        for phi in range(steps + 1):
            p = phi * step * 2 * pi
            for theta in range(steps + 1):
                the = theta * step * 2 * pi
                hx =  cos(p) * (r1*cos(the) + r2) + x
                hy = r1*sin(the) + y
                hz = -1 * sin(p) * (r1*cos(the) + r2) + z
                points.addPoint(hx,hy,hz) 
        return points
    def add_polyL(self,p1,p2,p3):
        self.add_poly_direct(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
    def add_poly_direct(self,x1,y1,z1,x2,y2,z2,x3,y3,z3):
        self.poly.addPoint(x1,y1,z1)
        self.poly.addPoint(x2,y2,z2)
        self.poly.addPoint(x3,y3,z3)
    def add_poly(self, x1,y1,z1,x2,y2,z2,x3,y3,z3,axis = "z", pos = True):
        #sort counterclockwise
        self.poly.addPoint(x1,y1,z1)
        if axis == "z":
            #print("2:",atan2((y2-y1),(x2-x1)),"3:", atan2((y3-y1),(x3-x1)))
            fact2 = atan2((y2-y1),(x2-x1))
            fact3 = atan2((y3-y1),(x3-x1))
            #print("2:",fact2,"3:", fact3)
        elif axis == "x":
            fact2 = atan2((z2-z1),(y2-y1))
            fact3 = atan2((z3-z1),(y3-y1))
        elif axis == "y":
            fact2 = atan2((x2-x1),(z2-z1))
            fact3 = atan2((x3-x1),(z3-z1))
        fact2 = fact2  if fact2 >= 0 else (2*pi - fact2)
        fact3 = fact3  if fact3 >= 0 else (2*pi - fact3)
        if fact2 < fact3 and pos:
            self.poly.addPoint(x2,y2,z2)
            self.poly.addPoint(x3,y3,z3)
        else:
            self.poly.addPoint(x3,y3,z3)
            self.poly.addPoint(x2,y2,z2)
    def __scanLine(self, x1,z1,x2,z2,y, color = None):
        ps = [[x1,z1],[x2,z2]]
        ps.sort()
        s = ps[0][0]
        e = ps[1][0]
        #print (s,e)
        #print(ps[1][1],ps[0][1])
        dz = (ps[1][1] - ps[0][1]) / (e-s+1)
        #if s < 0:
        #    s = 0
        for i in range(int(s),int(e+1)):
            self.plot(int(i),int(y),ps[0][1],color)
            ps[0][1] += dz
        if s == e:
            self.plot(int(s),int(y),z1,color)
    def draw_poly(self):
        view = screen.VIEW

        l = 0
        polys = self.poly.data
        while l < len(polys):
            A = vector(polys[l+1][0]-polys[l][0],polys[l+1][1]-polys[l][1],polys[l+1][2]-polys[l][2])
            B = vector(polys[l+2][0]-polys[l][0],polys[l+2][1]-polys[l][1],polys[l+2][2]-polys[l][2])
            N = A.cross(B)

            if N.dot(view) > 0 and polys[l] != polys[l+1] and polys[l+1] != polys[l+2] and polys[l] != polys[l+2]:
            # where the triangle is drawn
            # endpoits poly[l] through l[+2]
                points = [polys[i] for i in range(l,l+3)]
                for p in points:
                    p[0] = int(p[0])
                    p[1] = int(p[1])
                for p in points:
                    p[0],p[1] = p[1],p[0]
                points.sort()
                for p in points:
                    p[0],p[1] = p[1],p[0]
                #points = [points[i][::-1] for i in range(3)]
                #print(points)
                lines = points[2][1] - points[0][1] + 1

                dx0 = (points[2][0] - points[0][0]) / lines
                try:
                    dx1 = (points[1][0] - points[0][0]) / (points[1][1] - points[0][1])
                except ZeroDivisionError:
                    dx1 = 0
                try:
                    dx2 = (points[2][0] - points[1][0]) / (points[2][1] - points[1][1])
                except ZeroDivisionError:
                    dx2 = 0

                dz0 = (points[2][2] - points[0][2]) / lines
                try:
                    dz1 = (points[1][2] - points[0][2]) / (points[1][1] - points[0][1])
                except ZeroDivisionError:
                    dz1 = 0
                try:
                    dz2 = (points[2][2] - points[1][2]) / (points[2][1] - points[1][1])
                except ZeroDivisionError:
                    dz2 = 0
                xs = points[0][0]
                xe = points[0][0]

                zs = points[0][2]
                ze = points[0][2]
                if points[1][1] == points[0][1]:
                    xe = points[1][0]
                    ze = points[1][2]
                #print (points)
                # = [random.randint(0,255) for i in range(3)]
                #print(c)

                #COLOR!!!!!!!!
                lambient = [screen.AMBCOLOR[i] * screen.AMBIENT[i] for i in range(3)]
                

                N.normalize()
                L = [(polys[l][i] + polys[l+1][i] + polys[l+2][i]) / 3 for i in range(3)]
                L = [screen.LSOURCE[i] - L[i] for i in range(3)]
                L = vector(L[0],L[1],L[2])
                L.normalize()
                cosine = N.dot(L)
                if cosine > pi/2 or cosine < -pi/2:
                    cosine = 0

                ldiffuse = [screen.SCOLOR[i] * screen.DIFFUSE[i] * cosine for i in range(3)]
                #ldiffuse = [0,0,0]
                for i in range(3):
                    if ldiffuse[i] < 0:
                        ldiffuse[i] = 0
                    elif ldiffuse[i] > 255:
                        ldiffuse[i] = 255

                #T = [N[i] * nl for i in range(3)]
                #T = vector(T[0],T[1],T[2])
                #S = [N[i] * nl - L[i] for i in range(3)]
                # r = t + s
                ndata = [N.x,N.y,N.z]
                ldata = [L.x,L.y,L.z]
                R = [2*ndata[i] * cosine - ldata[i] for i in range(3)]
                R = vector(R[0],R[1],R[2])
                rv = pow(R.dot(screen.VIEW), screen.SPEC)
                lspecular = [screen.SCOLOR[i] * screen.SPECULAR[i] * rv for i in range(3)]
                #print(rv)
                for i in range(3):
                    if lspecular[i] < 0:
                        lspecular[i] = 0
                    elif lspecular[i] > 255:
                        lspecular[i] = 255
                
                light = [int(lambient[i] + ldiffuse[i] + lspecular[i]) for i in range(3)]
                #screen.DRAW = light[:]
                #print("0:",lambient[0],ldiffuse[0],lspecular[0])
                #print("1:",lambient[1],ldiffuse[1],lspecular[1])
                #print("2:",lambient[2],ldiffuse[2],lspecular[2])
                #print ("in",screen.AMBIENT,screen.DIFFUSE,screen.SPECULAR)
                for i in range(3):
                    if light[i] < 0:
                        light[i] = 0
                    elif light[i] > 255:
                        light[i] = 255

                for y in range(int(points[0][1]),int(points[2][1]+1)):
                    #print(xs,xe)
                    self.__scanLine(xs,zs,xe,ze,y,light)
                    xs += dx0
                    zs += dz0
                    # xe += dx1
                    # if y == points[1][1]:
                    #     dx1 = dx2
                    #     xe = points[1][0]
                    if y < points[1][1]:
                        xe += dx1
                        ze += dz1
                    else:
                        xe += dx2
                        ze += dz2
                # self.line(polys[l][0],polys[l][1],polys[l+1][0],polys[l+1][1], screen.DRAW[:])
                # self.line(polys[l+2][0],polys[l+2][1],polys[l+1][0],polys[l+1][1], screen.DRAW[:])
                # self.line(polys[l][0],polys[l][1],polys[l+2][0],polys[l+2][1], screen.DRAW[:])
            
                #self.plot(polys[l][0],polys[l][1],[255,0,0])
                #self.plot(polys[l+1][0],polys[l+1][1],[0,255,0])
            
            l+=3
    def toScreen(self):
        self.draw_poly()
        l = 0 # lines
        while l < len(self.edge.data):
            self.line(self.edge.data[l][0],self.edge.data[l][1], self.edge.data[l+1][0], self.edge.data[l+1][1],screen.DRAW[:])
            l+=2
    def updateTfrm(self):
        self.edge.mult(self.stack[-1])
        self.poly.mult(self.stack[-1])
    def push(self):
        self.stack.append(copy.deepcopy(self.stack[-1]))
    def pop(self):  
        self.stack.pop()
    def parse(self, args): #args are seperated my \n
        l = args.lower().split("\n")
        a = 0
        #print(l)
        while a < len(l):
            #print(l[a])
            #print(self.stack[-1].data)
            rel = False
            if (l[a] in "linecirclebezierhermiteboxspheretorus"):
                rel = True
                #print(l[a])

            if l[a] == "line":
                data = [int(i) for i in l[a+1].split(" ")]
                self.edge.addLine(data[0],data[1],data[2],data[3],data[4],data[5])
            elif l[a] == "circle":
                data = [int(i) for i in l[a+1].split(" ")]
                self.circle(data[0],data[1],data[2],data[3])
            elif l[a] == "bezier": # only accepts 4 coords
                data = [int(i) for i in l[a+1].split(" ")]
                self.bezier(data[0],data[1],data[6],data[7],[[data[2],data[3]],[data[4],data[5]]],20)
            elif l[a] == "hermite":
                data = [int(i) for i in l[a+1].split(" ")]
                self.hermite(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],20)
            elif l[a] == "box":
                #print("box")
                data = [int(i) for i in l[a+1].split(" ")]
                self.box(data[0],data[1],data[2],data[3],data[4],data[5])
            elif l[a] == "sphere":
                data = [int(i) for i in l[a+1].split(" ")]
                self.sphere(data[0],data[1],data[2],data[3])
            elif l[a] == "torus":
                data = [int(i) for i in l[a+1].split(" ")]
                self.torus(data[0],data[1],data[2],data[3],data[4])
            elif l[a] == "ident":
                self.tfrm.ident()
                a-=1
            elif l[a] == "scale":
                data = [i for i in l[a+1].split(" ")]
                data[0] = int(data[0])
                data[1] = int(data[1])
                data[2] = float(data[2])

                top = self.stack[-1]
                self.stack[-1] = matrix()
                self.stack[-1].scale(data[0],data[1],data[2])
                self.stack[-1].mult(top)
            elif l[a] == "move":
                data = [int(i) for i in l[a+1].split(" ")]
                top = self.stack[-1]
                self.stack[-1] = matrix()
                self.stack[-1].trns(data[0],data[1],data[2])
                self.stack[-1].mult(top)
                #self.stack[-1].mtrns(data[0],data[1],data[2])
            elif l[a] == "rotate":
                data = l[a+1].split(" ")
                data[1] = int(data[1])
                top = self.stack[-1]
                self.stack[-1] = matrix()
                self.stack[-1].rotate(data[0],data[1])
                self.stack[-1].mult(top)
                #self.stack[-1].mrotate(data[0],data[1])
            elif l[a] == "push":
                self.push()
                a-=1
            elif l[a] == "pop":
                self.pop()
                a-=1
            elif l[a] == "apply":
                self.updateTfrm()
                a-=1
            elif l[a] == "display":
                #display(self)
                a-=1
            elif l[a] == "save":
                self.toScreen()
                self.toFileAscii(l[a+1])
                a-=1
            elif l[a] == "clear":
                self.edge = matrix()
                a-=1
            elif l[a] == "color":
                data = [int(i) for i in l[a+1].split(" ")]
                screen.DRAW = data
                #print (screen.DRAW)
            elif l[a] == "shade":
                data = [int(i) for i in l[a+1].split(" ")]
                screen.AMBIENT = [i / 255 for i in data]
                screen.DIFFUSE = [i / 255 for i in data]
            else:
                a-=1
            a+=2
            self.relative_cs()
    def read(self, file):
        with open(file, "r") as f:
            self.parse(f.read())
    # def display(self):
    #     ppm_name = "pic.ppm"
    #     self.toFileAscii(ppm_name)
    #     p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    #     p.communicate()
    #     remove(ppm_name)
    def __nCr(self, n, r):
        return factorial(n) / (factorial(r) * factorial(n-r))
    def __dotProduct(self):
        None
    def relative_cs(self):
        #print ("relative_cs")
        #print(self.poly.data)
        self.updateTfrm()
        #print(self.poly.data)
        self.toScreen()
        self.edge.data = []
        self.poly.data = []
    def display(self):
        screen = self.pixels
        ppm_name = 'pic.ppm'
        self.toFile(ppm_name)
        p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
        p.communicate()
        remove(ppm_name)
    def save_extension(self, fname ):
        screen = self.pixels
        ppm_name = fname[:fname.find('.')] + '.ppm'
        self.toFile(ppm_name)
        p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
        p.communicate()
        remove(ppm_name)

def display( screen ):
    ppm_name = 'pic.ppm'
    save_ppm( screen, ppm_name )
    p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)
def save_extension( screen, fname ):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm( screen, ppm_name )
    p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)
def save_ppm( screen, fname ):
    f = open( fname, 'wb' )
    ppm = 'P6\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(255) +'\n'
    f.write(ppm.encode())
    for y in range( len(screen) )[::-1]:
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            #print(pixel)
            f.write( bytes(pixel) )
    f.close()