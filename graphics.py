class pixel:
    def __init__(self, r = 0, g = 0, b = 0):
        self.color = [r,g,b]
    def setColor(self, r = -1, g = -1, b = -1, color = []):
        if len(color) == 3:
            self.color = color
            return
        for h in range(3):
            if [r,g,b][h] != -1:
                self.color[h] = [r,g,b][h]
    def getColor(self):
        return "{} {} {}".format(self.color[0], self.color[1], self.color[2])
class image:
    def __init__(self, h, w):
        self.pixels = [[pixel() for i in range(w)] for i in range(h)]
        self.height = h
        self.width = w
    def toFile(self,file):
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
    def plot(self,w, h, r = 0, g = 0, b = 0, color = []):
        self.pixels[h][w].setColor(r,g,b,color)

