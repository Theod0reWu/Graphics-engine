from screen import *
pic = screen(500,500)
# lines = pic.edge
# lines.addLine(0,0,0,250,0,0)
# lines.addLine(0,0,0,0,250,0)
# lines.addLine(0,250,0,250,250,0)
# lines.addLine(250,0,0,250,250,0)
# lines.addLine(0,0,0,0,0,-250)
# lines.addLine(0,0,-250,250,0,-250)
# lines.addLine(250,0,-250,250,0,0)
# lines.addLine(0,0,-250,0,250,-250)
# lines.addLine(0,250,-250,0,250,0)
# lines.addLine(250,250,0,250,250,-250)
# lines.addLine(250,0,-250,250,250,-250)
# lines.addLine(0,250,-250,250,250,-250)

# #pic.tfrm.mscale(.1,.1,.1)
# pic.tfrm.mscale(.5,.5,.5)
# pic.tfrm.mrotate("z",20)
# pic.tfrm.mrotate("x",20)
# pic.tfrm.mrotate("y",20)

# pic.tfrm.mtrns(200,200)

# pic.edge.print()
# pic.tfrm.print()
# pic.updateTfrm()
# pic.edge.print()
# pic.toScreen()
# pic.toFile("pic.ppm")
pic.read("cube.txt")

