from screen import *
pic = screen(500,500)
#pic.add_poly(499,0,0,0,0,0,0,499,0)
print (pic.poly.data)
pic.toScreen()
#print("0,0 is the top left corner")

#save_extension(pic, "try.png")
pic.toFileAscii("pic.ppm")
#display(pic)
