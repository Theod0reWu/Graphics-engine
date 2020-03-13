from matrix import *
from subprocess import Popen, PIPE
from os import remove
from math import cos, sin, pi, factorial
class screen:
    DEFAULT = [0,0,0]
    DRAW = [255,255,255]
    def __init__(self, h, w):
        self.pixels = [[screen.DEFAULT[:] for i in range(w)] for i in range(h)]
        self.height = h
        self.width = w
        #master matrices
        self.tfrm = matrix()
        self.tfrm.ident()
        self.edge = matrix()
    def clear(self):
        for h in range(self.height):
            for w in range(self.width):
                self.pixels[h][w] = screen.DEFAULT[:]
        self.edge.data = []
        self.tfrm.ident()
    def toFile(self,file):
        enter = "P6\n{} {}\n255\n".format(self.height, self.width)
        with open(file, "wb") as f:
            f.write(enter.encode())
            for h in range(self.height):
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
    def plot(self,w, h,color):
        #print(h,w)
        try:
            self.pixels[int(h)][int(w)] = color[:]
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
    def circle(self,x,y,z,r,steps):
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
    def box(self,x,y,z,length, height, depth):
        self.edge.addLine(x,y,z,x+length,y,z)
        self.edge.addLine(x,y,z,x,y,z+depth)
        self.edge.addLine(x,y,z,x,y-height,z)
        self.edge.addLine(x+length,y,z,x+length,y-height,z)
        self.edge.addLine(x+length,y,z,x+length,y,z+depth)
        self.edge.addLine(x,y-height,z,x+length,y-height,z)
        self.edge.addLine(x,y,z+depth,x+length,y,z+depth)
        self.edge.addLine(x,y-height,z+depth,x,y,z+depth)
        self.edge.addLine(x,y-height,z+depth,x+length,y-height,z+depth)
        self.edge.addLine(x+length,y-height,z+depth,x+length,y,z+depth)
        self.edge.addLine(x,y-height,z,x,y-height,z+depth)
        self.edge.addLine(x+length,y-height,z,x+length,y-height,z+depth)
    def toScreen(self):
        l = 0
        while l < len(self.edge.data):
            self.line(self.edge.data[l][0],self.edge.data[l][1], self.edge.data[l+1][0], self.edge.data[l+1][1],screen.DRAW[:])
            l+=2
    def updateTfrm(self):
        self.edge.mult(self.tfrm)
    def parse(self, args): #args are seperated my \n
        l = args.lower().split("\n")
        a = 0
        while a < len(l):
            #print(l[a])
            if l[a] == "line":
                data = [int(i) for i in l[a+1].split(" ")]
                self.edge.addLine(data[0],data[1],data[2],data[3],data[4],data[5])
            elif l[a] == "circle":
                data = [int(i) for i in l[a+1].split(" ")]
                self.circle(data[0],data[1],data[2],data[3],30)
            elif l[a] == "bezier": # only accepts 4 coords
                data = [int(i) for i in l[a+1].split(" ")]
                self.bezier(data[0],data[1],data[6],data[7],[[data[2],data[3]],[data[4],data[5]]],20)
            elif l[a] == "hermite":
                data = [int(i) for i in l[a+1].split(" ")]
                self.hermite(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],20)
            elif l[a] == "box":
                data = [int(i) for i in l[a+1].split(" ")]
                self.box(data[0],data[1],data[2],data[3],data[4],data[5])
            elif l[a] == "ident":
                self.tfrm.ident()
                a-=1
            elif l[a] == "scale":
                data = [int(i) for i in l[a+1].split(" ")]
                self.tfrm.mscale(data[0],data[1],data[2])
            elif l[a] == "move":
                data = [int(i) for i in l[a+1].split(" ")]
                self.tfrm.mtrns(data[0],data[1],data[2])
            elif l[a] == "rotate":
                data = l[a+1].split(" ")
                data[1] = int(data[1])
                self.tfrm.mrotate(data[0],data[1])
            elif l[a] == "apply":
                self.updateTfrm()
                a-=1
            elif l[a] == "display":
                #display(self)
                a-=1
            elif l[a] == "save":
                self.toScreen()
                self.toFileAscii(l[a+1])
            else:
                a-=1
            a+=2
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
def display( screen ):
    ppm_name = 'pic.ppm'
    screen.toFileAscii(ppm_name)
    p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

