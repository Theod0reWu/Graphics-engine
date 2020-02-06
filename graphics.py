class Pixel:
    DEFAULT = [0,0,0]
    def __init__(self, r = DEFAULT[0], g = DEFAULT[0], b = DEFAULT[0]):
        self.color = [r,g,b]
    def setColor(self, r = -1, g = -1, b = -1, color = []):
        if len(color) == 3:
            self.color = color[:]
            return
        for h in range(3):
            if [r,g,b][h] != -1:
                self.color[h] = [r,g,b][h]
    def getColor(self):
        return "{} {} {}".format(self.color[0], self.color[1], self.color[2])
class Screen:
    def __init__(self, h, w):
        self.pixels = [[Pixel() for i in range(w)] for i in range(h)]
        self.height = h
        self.width = w
    def clear(self):
        for h in self.pixels:
            for w in h:
                w.color = Pixel.DEFAULT[:]
    def toFile(self,file):
        enter = "P6\n{} {}\n255\n".format(self.height, self.width)
        with open(file+".ppm", "wb") as f:
            f.write(enter.encode())
            for i in self.pixels:
                for p in i:
                    f.write(bytes(p.color))
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
        for r in self.pixels:
            for c in r:
                funct(c)
    def allPixCoord(self, funct):
        for h in range(self.height):
            for w in range(self.width):
                funct(w,h,self.pixels[w][h])
    def plot(self,w, h, color, r = 0, g = 0, b = 0):
        self.pixels[h][w].setColor(r,g,b,color)
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
        a = y2 - y1
        b = -(x2-x1)
        d = a + 2*b
        while x1 < x2:
            self.plot(x1,y1,color)
            if d < 0:
                x1+=1
                d+=2*a
            y1 += 1
            d += 2*b
    def line(self,x1,y1,x2,y2,color):
        m = 2
        if (x2 != x1):
            m = (y2-y1)/(x2-x1)
        if (m <= 1 and m > 0):
            self._Q1(x1,y1,x2,y2,color)
        elif(m > 1):
            self._Q2(x1,y1,x2,y2,color)
        elif(m > -1):
            self._Q3(x1,y1,x2,y2,color)
        else:
            self._Q4(x1,y1,x2,y2,color)
image = Screen(500,500)
image.line(0,0,500,50,[255,255,255])
image.line(0,0,0,500,[255,255,255])
#Pixel.DEFAULT = [255,255,255]
#image.clear()
image.toFile("test")
