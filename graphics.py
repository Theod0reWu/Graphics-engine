class Screen:
    DEFAULT = [0,0,0]
    def __init__(self, h, w):
        self.pixels = [[Screen.DEFAULT[:] for i in range(w)] for i in range(h)]
        self.height = h
        self.width = w
    def clear(self):
        for h in self.height:
            for w in self.width:
                self.pixels[h][w] = Screen.DEFAULT[:]
    def toFile(self,file):
        enter = "P6\n{} {}\n255\n".format(self.height, self.width)
        with open(file+".ppm", "wb") as f:
            f.write(enter.encode())
            for h in range(self.height):
                for w in range(self.width):
                    c = self.pixels[h][w]
                    f.write(bytes(c))
    def toFileAscii(self,file):
        enter = "P3\n{} {}\n255\n".format(self.height, self.width)
        for i in self.pixels:
            row = ""
            for p in i:
                row += p.getColor() + " "
            enter += row + "\n"
        with open(file+".ppm", "w+") as f:
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
        self.pixels[h][w] = color[:]
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
class Matrix:
    def __init__(self, points = 4):
        c = [0,0,0,1]
        self.data = [c[:] for i in range(points)]
        self.id = False
    def print(self):
        one,two,three, four = "","","", ""
        for i in self.data:
            one+=str(i[0]) + " "
            two+=str(i[1]) + " "
            three+=str(i[2]) + " "
            four+=str(i[3]) + " "
        print(one+"\n"+two+"\n"+three + "\n"+four)
    def ident(self):#convert to an identity matrix
        self.data = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]][::-1]
        self.id = True
    def mult(self, m): #m is [4x4]
        for p in range(len(self.data)):
            new = [0,0,0,0]
            ori = self.data[p]
            for i in range(4):
                f = m.data[i]
                new[i] = f[0]*ori[i] + f[1]*ori[i] + f[2]*ori[i] + f[3]*ori[i]
            self.data[p] = new
        
print("making an identity matrix")
ident = Matrix()
ident.ident()
ident.print()
print("making a blank matrix with 10 columns")
lines = Matrix(10)
lines.print() 
image = Screen(500,500)
print("filling the matrix with random stuff")
import random
for i in range(3):
    for w in range(10):
        lines.data[w][i] = random.randint(0,9)
lines.print()
print("multiplying by identity matrix")
lines.mult(ident)
lines.print()
print("changing identity matrix")
ident.data[0][0] = 2
ident.print()
print("multiplying again")
lines.mult(ident)
lines.print()

image.toFile("pic")
print("pic.ppm")
