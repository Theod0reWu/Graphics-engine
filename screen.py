from matrix import *
class screen:
    DEFAULT = [0,0,0]
    def __init__(self, h, w):
        self.pixels = [[screen.DEFAULT[:] for i in range(w)] for i in range(h)]
        self.height = h
        self.width = w
        #master matrices
        self.tfrm = matrix()
        self.tfrm.ident()
        self.edge = matrix()
    def clear(self):
        for h in self.height:
            for w in self.width:
                self.pixels[h][w] = Screen.DEFAULT[:]
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

    def toScreen(self):
        l = 0
        while l < len(self.edge.data):
            self.line(self.edge.data[l][0],self.edge.data[l][1], self.edge.data[l+1][0], self.edge.data[l+1][1],[255,255,255])
            l+=2
    def updateTfrm(self):
        self.edge.mult(self.tfrm)
    def parse(self, args): #args are seperated my \n
        l = args.lower().split("\n")
        a = 0
        while a < len(l):
            if l[a] == "line":
                data = [int(i) for i in l[a+1].split(" ")]
                self.edge.addLine(data[0],data[1],data[2],data[3],data[4],data[5])
            elif l[a] == "ident":
                self.tfrm.ident()
            elif l[a] == "scale":
                data = [int(i) for i in l[a+1].split(" ")]
                self.tfrm.mscale(data[0],data[1],data[2])
            elif l[a] == "move":
                data = [int(i) for i in l[a+1].split(" ")]
                self.tfrm.mtrns(data[0],data[1],data[2])
            elif l[a] == "rotate":
                data = [int(i) for i in l[a+1].split(" ")]
                self.tfrm.mrotate(data[0],data[1])
            elif l[a] == "apply":
                self.clear()
                self.toScreen()
            elif l[a] == "display":
                None
            elif l[a] == "save":
                data = [int(i) for i in l[a+1].split(" ")]
                self.toFile(data[0])
