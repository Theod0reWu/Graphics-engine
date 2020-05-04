import mdl
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
    for command in commands:
        #print(command)
        op = command['op']
        args = command['args']
        reflect = '.white'

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

            top = panel.stack[-1]
            panel.stack[-1] = matrix()
            panel.stack[-1].scale(float(args[0]),float(args[1]),float(args[2]))
            panel.stack[-1].mult(top)
        elif op == "move":
            top = panel.stack[-1]
            panel.stack[-1] = matrix()
            panel.stack[-1].trns(float(args[0]),float(args[1]),float(args[2]))
            panel.stack[-1].mult(top)
            #panel.stack[-1].mtrns(float(args[0]),float(args[1]),float(args[2]))
        elif op == "rotate":
            top = panel.stack[-1]
            panel.stack[-1] = matrix()
            panel.stack[-1].rotate(args[0],float(args[1]))
            panel.stack[-1].mult(top)
            #panel.stack[-1].mrotate(float(args[0]),float(args[1]))
        elif op == "push":
            panel.push()    
        elif op == "pop":
            panel.pop()    
        elif op == "apply":
            panel.updateTfrm()    
        elif op == "display":
            display(panel.pixels)
        elif op == "save":
            #panel.toFileAscii(args[0]+".ppm")
            save_ppm(panel.pixels,args[0]+".ppm")
        elif op == "clear":
            panel.edge = matrix()
        panel.relative_cs()
        #print ("symbol thingy",symbols[command['constants']][1]['red'][1])
        #print(symbols[reflect])


