from screen import *
pic = screen(500,500)
pic.circle(100,100,0,50,21)
pic.toScreen()
pic.plot(100,100,[255,0,0])


pic.toFile("pic.ppm")
print("pic.ppm")
print("0,0 is the top left corner")
