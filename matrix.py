from math import radians, cos, sin
class Matrix:
    def __init__(self, points = 0):
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
    def trns(self, a = 0, b = 0, c = 0):
        self.ident()
        self.data[0][3] = a
        self.data[1][3] = b
        self.data[2][3] = c
    def scale(self, a = 1, b = 1, c = 1):
        self.ident()
        self.data[0][0] = a
        self.data[1][1] = b
        self.data[2][2] = c
    def rotate(self, axis, deg):
        self.ident()
        rad = radians(deg)
        m = self.data
        if axis == ("x"):
            m[1][1] = cos(rad)
            m[1][2] = -sin(rad)
            m[2][1] = sin(rad)
            m[2][2] = cos(rad)
        elif axis==("y"):
            m[2][2] = cos(rad)
            m[2][0] = -sin(rad)
            m[0][2] = sin(rad)
            m[0][0] = cos(rad)
        elif axis==("z"):
            m[0][0] = cos(rad)
            m[0][1] = -sin(rad)
            m[1][0] = sin(rad)
            m[1][1] = cos(rad)
        else:
            print ("wrong input given to rotate: invalid axis")
            raise ValueError
    def mult(self, m): #m is [4x4] original = m*orginal
        for p in range(len(self.data)):
            new = [0,0,0,0]
            ori = self.data[p]
            for i in range(4):
                f = m.data[i]
                new[i] = f[0]*ori[0] + f[1]*ori[1] + f[2]*ori[2] + f[3]*ori[3]
            self.data[p] = new
    def addLine(self,x1,y1,z1,x2,y2,z2):
        self.data.append([x1,y1,z1,1])
        self.data.append([x2,y2,z2,1])
    def toScreen(self, screen):
        l = 0
        while l < len(self.data):
            screen.line(self.data[l][0],self.data[l][1], self.data[l+1][0], self.data[l+1][1],[255,255,255])
            l+=2
