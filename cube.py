import numpy as np
import random

top    = 0, slice(0,3), slice(0,3), 0 # == cube[0,:,:,0]
bottom = 2, slice(0,3), slice(0,3), 0 
left   = slice(0,3), 0, slice(0,3), 1
right  = slice(0,3), 2, slice(0,3), 1
front  = slice(0,3), slice(0,3), 0, 2
back   = slice(0,3), slice(0,3), 2, 2
faces = [top, bottom, left, right, front, back]

def new_cube():
    a = np.zeros(3*3*3*3, dtype='str').reshape([3,3,3,3])
    a[:,:,:,:] = '-'
    for (face, color) in zip(faces, "WYORGB"):
         a[face] = color
    return a

def new_test_cube():
    a = new_cube()
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    faces = [top, bottom, left, front, right, back]  # Faces are in a different order from the global "faces" variable
    for i in range(len(faces)):
        a[faces[i]] = np.array(letters[9*i:9*(i+1)]).reshape([3,3])
    return a

a = new_cube()
a = new_test_cube()

def flatten_cube(a):
    return ''.join(a.flatten()) # flatten the cube to a single string

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
    ax = dict(zip("UDLRFB", [1,1,1,1,2,2]))[newTop]
    k = dict(zip("UDLRFB", [0,2,1,3,1,3]))[newTop]
    cube = np.rot90(cube, k=k, axes=[ax, 0])  # Creates a copy
    old = cube.copy()
    match newTop:  # Reorient the fourth/faces dimension
        case 'L' | 'R' | 'F' | 'B': 
            cube[:,:,:,0] = old[:,:,:,ax]
            cube[:,:,:,ax] = old[:,:,:,0]
    return cube

#L = Clockwise, L' = counterclockwise
def do_move(face, cube):
    undo = dict(zip("UDLRFB", "UDRLBF"))[face[0]]
    b = reorient(cube, face[0])
    for i in range(1 if len(face) == 1 else 3):
        b = rotate_top(b)
    b = reorient(b, undo) 
    return b

def mix(cube):
    all_moves = "U D L R F B U' D' L' R' F' B'".split(" ")
    for _ in range(20):
        cube = do_move(random.choice(all_moves), cube)
    return cube
