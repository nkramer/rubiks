import numpy as np
# import random

# shuffle
# #x = ["L", "L'", "R", "R'"]
# x = "L L' R R'".split(" ")
# path = [random.choice(x) for i in range(20)]
# print( " ".join(path) )

# axes = (up/down, left/right, back/front, faces)
# faces = the colors of (up/down, left/right, back/front)

top    = 0, slice(0,3), slice(0,3), 0 # == cube[0,:,:,0]
bottom = 2, slice(0,3), slice(0,3), 0 
left   = slice(0,3), 0, slice(0,3), 1
right  = slice(0,3), 2, slice(0,3), 1
front  = slice(0,3), slice(0,3), 0, 2
back   = slice(0,3), slice(0,3), 2, 2

def new_cube():
    a = np.zeros(3*3*3*3, dtype='str').reshape([3,3,3,3])
    a[:,:,:,:] = '-'
    a[top] = 'W'
    a[bottom] = 'Y'
    a[left] = 'O'  
    a[right] = 'R' 
    a[front] = 'G' 
    a[back] = 'B'  
    # faces = [top, bottom, left, front, right, back]
    # for (face, color) in zip(faces, "WYORGB"):
    #      a[face] = color
    return a

a = new_cube()

def new_test_cube():
    a = new_cube()
    letters = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [chr(i) for i in range(ord('0'), ord('9') + 1)]
    #letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    for i in range(len([top, bottom, left, front, right, back])):
        face = [top, bottom, left, front, right, back][i]
        a[face] = np.array(letters[9*i:9*(i+1)]).reshape([3,3])
    # for i in range(len(faces)):
    #     a[faces[i]] = np.array(letters[9*i:9*(i+1)]).reshape([3,3])
    return a

a = new_test_cube()

def cube_to_string(a): # Convert cube to string representation
    blank = np.zeros(3*3, dtype='str').reshape([3,3]); blank[:,:] = ' '  # blank grid
    strip = np.zeros(3*1, dtype='str').reshape([3,1]); strip[:,:] = ' '  # blank column
    c = np.concatenate((
        np.concatenate((blank, strip, np.flip(np.transpose(a[top]), axis=0), strip, blank, strip, blank), axis=1),
        np.concatenate((np.flip(a[left], axis=1), strip, a[front], strip, a[right], strip, np.flip(a[back], axis=1)), axis=1),
        np.concatenate((blank, strip, np.transpose(a[bottom]), strip, blank, strip, blank), axis=1)
    ))
    return '\n'.join([' '.join(c[i,:]) for i in range(c.shape[0])])

def p(a): # Print the cube
    print(cube_to_string(a))

def cube_to_4d_string(a): # Convert 4D hypercube to string representation
    row = np.zeros(3*3 + 2, dtype='str').reshape([1,11]); row[:,:] = ' '   # blank row
    col = np.zeros(3*1, dtype='str').reshape([3,1]); col[:,:] = ' '        # blank column
    c = np.concatenate((
        np.concatenate([a[0,0,:,:], col, a[0,1,:,:], col, a[0,2,:,:]], axis=1), row,
        np.concatenate([a[1,0,:,:], col, a[1,1,:,:], col, a[1,2,:,:]], axis=1), row,
        np.concatenate([a[2,0,:,:], col, a[2,1,:,:], col, a[2,2,:,:]], axis=1)
    ))
    return '\n'.join([' '.join(c[i]) for i in range(c.shape[0])])

def p4(a): # Print the 4D hypercube as a 3x3 grid of 3x3 grids
    print(cube_to_4d_string(a))

# Rotate the top clockwise
def rotate_top(cube):
    b = cube.copy()
    b[0,:,:,:] = np.rot90(b[0,:,:,:], axes=[0, 1], k=-1)
    c=b.copy()
    c[0,:,:,1] = b[0,:,:,2]
    c[0,:,:,2] = b[0,:,:,1]
    return c

def reorient(cube, newTop):
    match newTop:
        case 'U': ax=[0,1]; k=0
        case 'D': ax=[1,0]; k=2
        case 'L': ax=[1,0]; k=1
        case 'R': ax=[1,0]; k=3
        case 'F': ax=[2,0]; k=1
        case 'B': ax=[2,0]; k=3
        #ax = dict(zip("UDLRFB", [1,1,1,1,2,2]))[newTop]
        #k = dict(zip("UDLRFB", [0,2,1,3,1,3]))[newTop]
    cube = np.rot90(cube, k=k, axes=ax)
    old = cube.copy() # Eliminate
    cube = cube.copy()
    match newTop:  # Reorient the fourth/faces dimension
        case 'L' | 'R': 
            cube[:,:,:,0] = old[:,:,:,1]
            cube[:,:,:,1] = old[:,:,:,0]
        case 'F' | 'B': 
            cube[:,:,:,0] = old[:,:,:,2]
            cube[:,:,:,2] = old[:,:,:,0]
    # cube[:,:,:,0] = old[:,:,:,ax]
    # cube[:,:,:,ax] = old[:,:,:,0]

    return cube

#L = Clockwise, L' = counterclockwise
def perm(face, cube):
    match face[0]:
        case 'U': x=('U', 'U')
        case 'D': x=('D', 'D')
        case 'L': x=('L', 'R')
        case 'R': x=('R', 'L')
        case 'F': x=('F', 'B')
        case 'B': x=('B', 'F')
    #undo = dict(zip("UDLRFB", "UURLBF"))[face]
    b=cube.copy()    
    b = reorient(b, x[0])
    for i in range(1 if len(face) == 1 else 3):
        b = rotate_top(b)
    b = reorient(b, x[1]) 
    return b

p(a)
p(perm("B", a))