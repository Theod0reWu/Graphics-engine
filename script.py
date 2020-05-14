import mdl
import sys
from screen import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    # tmp = matrix()
    # tmp.ident()

    # stack = [ [x[:] for x in tmp] ]
    # panel = new_panel()
    # zbuffer = new_zbuffer()
    panel = screen(500,500)
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    colors = ['red','green','blue']

    #print("symbols")
    #print(symbols)
    #print("commands")

    frames = 1
    basename = ""
    vary = False
    knobs = []
    #pass number 0 and numero yi
    for command in commands:
      op = command['op']
      args = command['args']

      if (op == "frames"):
        frames = int(args[0])
      elif (op == "basename"):
        basename = args[0]
      elif (op == "vary"):
        vary = True
        #print(args,op, command)
        knobs.append([command["knob"],args[0],args[1],args[2], args[3]])

    if vary and frames <= 1:
      sys.exit("attempting to vary with invalid number of frames")
    elif len(basename) == 0:
      print ("your basename will be pic100")
      basename = "pic100"

    knobTable = [{} for i in range(frames)]
    #print(knobs)
    for i in range(frames):
      #print(i)
      dic = knobTable[i]
      for knob in knobs:
        if i >= knob[1] and i <= knob[2]:
          knobTable[i][knob[0]] = knob[3] + (i - knob[1]) * ( (knob[4] - knob[3]) / (knob[2] - knob[1]) )
          #print (knob)
          #print(knob[0],knob[3] + (i - knob[1]) * ( (knob[4] - knob[3]) / (knob[2] - knob[1]) ) )
    #print (knobTable)
    #print (commands)
    for frame in range(frames):
      panel = screen(500,500)
      for command in commands:
        #print(command)
        op = command['op']
        args = command['args']
        if "knob" in command.keys():
          knob = command['knob']
        else:
          knob = None
        # if knob != None:
        #       kv = knobTable[frame][knob]
        reflect = '.white'
        kv = 1 #knob value

        rel = False
        if (op in "linecirclebezierhermiteboxspheretorus"):
            rel = True
            #print(op)

        if op == "line":
            
            panel.edge.addLine(float(args[0]),float(args[1]),float(args[2]),float(args[3]),float(args[4]),float(args[5]))
        elif op == "circle":
            
            panel.circle(float(args[0]),float(args[1]),float(args[2]),float(args[3]))
        elif op == "bezier": # only accepts 4 coords
            
            panel.bezier(float(args[0]),float(args[1]),float(args[6]),float(args[7]),[[float(args[2]),float(args[3])],[float(args[4]),float(args[5])]],20)
        elif op == "hermite":
            
            panel.hermite(float(args[0]),float(args[1]),float(args[2]),float(args[3]),float(args[4]),float(args[5]),float(args[6]),float(args[7]),20)
        elif op == "box":
            #print("box")
            if command['constants'] is not None:
                reflect = command['constants']
            panel.updateColor(symbols,reflect)
            panel.box(float(args[0]),float(args[1]),float(args[2]),float(args[3]),float(args[4]),float(args[5]))
        elif op == "sphere":
            if command['constants'] is not None:
                reflect = command['constants']
            panel.updateColor(symbols,reflect)
            panel.sphere(float(args[0]),float(args[1]),float(args[2]),float(args[3]))
        elif op == "torus":
            if command['constants'] is not None:
                reflect = command['constants']
            panel.updateColor(symbols,reflect)
            panel.torus(float(args[0]),float(args[1]),float(args[2]),float(args[3]),float(args[4]))
        elif op == "ident":
            panel.tfrm.ident()
            
        elif op == "scale":
            if knob != None:
              kv = knobTable[frame][knob]
            top = panel.stack[-1]
            panel.stack[-1] = matrix()
            panel.stack[-1].scale(float(args[0]) * kv,float(args[1]) * kv,float(args[2]) * kv)
            panel.stack[-1].mult(top)
        elif op == "move":
            if knob != None:
              kv = knobTable[frame][knob]
            top = panel.stack[-1]
            panel.stack[-1] = matrix()
            panel.stack[-1].trns(float(args[0]) * kv,float(args[1]) * kv,float(args[2]) * kv)
            panel.stack[-1].mult(top)
            #panel.stack[-1].mtrns(float(args[0]),float(args[1]),float(args[2]))
        elif op == "rotate":
            if knob != None:
              kv = knobTable[frame][knob]
            top = panel.stack[-1]
            panel.stack[-1] = matrix()
            panel.stack[-1].rotate(args[0],float(args[1])*kv)
            panel.stack[-1].mult(top)
            #panel.stack[-1].mrotate(float(args[0]),float(args[1]))
        elif op == "push":
            panel.push()    
        elif op == "pop":
            panel.pop()    
        #elif op == "apply":
        #    panel.updateTfrm()    
        #elif op == "display":
        #    display(panel.pixels)
        #elif op == "save":
        #    #panel.toFileAscii(args[0]+".ppm")
        #    save_ppm(panel.pixels,args[0]+".ppm")
        #elif op == "clear":
        #    panel.edge = matrix()
        #print(kv)
        panel.relative_cs()
        #print ("symbol thingy",symbols[command['constants']][1]['red'][1])
        #print(symbols[reflect])
      num = str(frame)
      num = "0" * (len(str(frames)) - len(num)) + num
      save_ppm(panel.pixels,"animation/"+basename+num+".ppm")
      print ("saved:", basename+num)



