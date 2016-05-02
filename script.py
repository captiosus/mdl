import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    stack = [ tmp ]
    screen = new_screen()

    for command in commands:
        if command[0] == 'line':
            edge = []
            add_edge( edge, command[1], command[2], command[3], command[4], command[5], command[6] )
            matrix_mult(stack[-1], edge)
            draw_lines(edge, screen, color)

        elif command[0] == 'circle':
            edge = []
            add_circle( edge, command[1], command[2], 0, command[3], .01 )
            matrix_mult(stack[-1], edge)
            draw_lines(edge, screen, color)

        elif command[0] == 'bezier':
            edge = []
            add_curve( edge, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .01, 'bezier' )
            matrix_mult(stack[-1], edge)
            draw_lines(edge, screen, color)

        elif command[0] == 'hermite':
            edge = []
            add_curve( edge, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .01, 'hermite' )
            matrix_mult(stack[-1], edge)
            draw_lines(edge, screen, color)

        elif command[0] == 'sphere':
            polygons = []
            add_sphere( polygons, command[1], command[2], command[3], command[4], 5 )
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, color)

        elif command[0] == 'torus':
            polygons = []
            add_torus( polygons, command[1], command[2], 0, command[3], command[4], 5 )
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, color)

        elif command[0] == 'box':
            polygons = []
            add_box( polygons, command[1], command[2], command[3], command[4], command[5], command[6] )
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, color)


        elif command[0] == 'scale':
            s = make_scale( command[1], command[2], command[3] )
            matrix_mult( stack[-1], s )
            stack[-1] = s

        elif command[0] == 'move':
            t = make_translate( command[1], command[2], command[3] )
            matrix_mult( stack[-1], t )
            stack[-1] = t

        elif command[0] == 'push':
            stack.append(stack[-1])

        elif command[0] == 'pop':
            stack.pop()

        elif command[0] == 'display':
            display( screen )

        elif command[0] == 'save':
            save_extension( screen, commands[c].strip() )

        elif command[0] == 'rotate':
            angle = float(command[2]) * ( math.pi / 180 )
            if command[1] == 'x':
                r = make_rotX( angle )
            elif command[1] == 'y':
                r = make_rotY( angle )
            elif command[1] == 'z':
                r = make_rotZ( angle )
            matrix_mult( stack[-1], r )
            stack[-1] = r

        elif command[0] == 'quit':
            return
