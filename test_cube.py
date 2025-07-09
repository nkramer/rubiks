import pytest
import numpy as np
import sys
import os

# Add the current directory to the path so we can import cube
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cube import *

@pytest.fixture
def test_cube():
    return new_test_cube()

def assert_equal_modulo_whitespace(str1, str2):
    def multi_strip(s): return '\n'.join([line.strip() for line in s.splitlines()])
    assert multi_strip(str1) == multi_strip(str2)

def test_new_cube():
    assert flatten_cube(new_cube()) == 'WOGWO-WOBW-GW--W-BWRGWR-WRB-OG-O--OB--G-----B-RG-R--RBYOGYO-YOBY-GY--Y-BYRGYR-YRB'
    assert flatten_cube(new_test_cube()) == 'asBbt-cuTd-Ce--f-UgKDhL-iMV-vE-w--xW--F-----X-NG-O--PYjyHkz-lAZm-In--o-0pQJqR-rS1'

def test_print():    
    assert_equal_modulo_whitespace(cube_to_string(new_test_cube()), 
"""        c f i
        b e h
        a d g
u t s   B C D   K L M   V U T
x w v   E F G   N O P   Y X W
A z y   H I J   Q R S   1 0 Z
        j m p
        k n q
        l o r""")
    assert_equal_modulo_whitespace(cube_to_4d_string(new_test_cube()), 
"""a s B   d - C   g K D
b t -   e - -   h L -
c u T   f - U   i M V

- v E   - - F   - N G
- w -   - - -   - O -
- x W   - - X   - P Y

j y H   m - I   p Q J
k z -   n - -   q R -
l A Z   o - 0   r S 1
""")

def test_perm():
    # Test all possible permutations with a test cube
    results = [flatten_cube(perm(p, new_test_cube())) 
        for p in ['U', 'D', 'L', 'R', 'F', 'B'] + ["U'", "D'", "L'", "R'", "F'", "B'"]]
    str = '\n'.join(results)
    assert_equal_modulo_whitespace(str, """gDKdC-aBsh-Le--b-tiVMfU-cTu-vE-w--xW--F-----X-NG-O--PYjyHkz-lAZm-In--o-0pQJqR-rS1
asBbt-cuTd-Ce--f-UgKDhL-iMV-vE-w--xW--F-----X-NG-O--PYlZAo0-r1Sk-zn--q-RjHymI-pJQ
TucWx-ZAld-Ce--f-UgKDhL-iMV-tb-w--zk--F-----X-NG-O--PYBsaEv-Hyjm-In--o-0pQJqR-rS1
asBbt-cuTd-Ce--f-UJQpGN-DKg-vE-w--xW--F-----X-Rq-O--LhjyHkz-lAZm-In--o-01SrYP-VMi
yjHbt-cuTv-Ee--f-UsaBhL-iMV-mI-w--xW--F-----X-dC-O--PYQpJkz-lAZN-Gn--o-0KgDqR-rS1
asBbt-MiVd-Ce--P-YgKDhL-Sr1-vE-w--fU--F-----X-NG-O--o0jyHkz-ucTm-In--x-WpQJqR-AlZ
cTufU-iVMb-te--h-LaBsdC-gDK-vE-w--xW--F-----X-NG-O--PYjyHkz-lAZm-In--o-0pQJqR-rS1
asBbt-cuTd-Ce--f-UgKDhL-iMV-vE-w--xW--F-----X-NG-O--PYpJQmI-jHyq-Rn--k-zr1So0-lZA
HyjEv-Bsad-Ce--f-UgKDhL-iMV-zk-w--tb--F-----X-NG-O--PYZAlWx-Tucm-In--o-0pQJqR-rS1
asBbt-cuTd-Ce--f-UVMiYP-1Sr-vE-w--xW--F-----X-Lh-O--RqjyHkz-lAZm-In--o-0DKgGN-JQp
KgDbt-cuTN-Ge--f-UQpJhL-iMV-dC-w--xW--F-----X-mI-O--PYsaBkz-lAZv-En--o-0yjHqR-rS1
asBbt-AlZd-Ce--x-WgKDhL-ucT-vE-w--o0--F-----X-NG-O--fUjyHkz-Sr1m-In--P-YpQJqR-MiV""")

# def test_cube_initialization(test_cube):
#     """Test that the cube is properly initialized with correct shape and faces"""
#     assert test_cube.shape == (3, 3, 3, 3)
#     assert test_cube.dtype == 'str'
    
#     # Test that faces are properly set
#     assert test_cube[top][0,0] == '1'
#     assert test_cube[bottom][0,0] == 'A'
#     assert test_cube[left][0,0] == 'a'
#     assert test_cube[right][0,0] == 'α'
#     assert test_cube[front][0,0] == 'x'
#     assert test_cube[back][0,0] == 'X'

# def test_face_definitions(test_cube):
#     """Test that face slice definitions are correct"""
#     # Test that faces have the correct shapes
#     assert test_cube[top].shape == (3, 3)
#     assert test_cube[bottom].shape == (3, 3)
#     assert test_cube[left].shape == (3, 3)
#     assert test_cube[right].shape == (3, 3)
#     assert test_cube[front].shape == (3, 3)
#     assert test_cube[back].shape == (3, 3)

# def test_rotate_top_clockwise(test_cube):
#     """Test that rotate_top rotates the top face clockwise"""
#     original_top = test_cube[top].copy()
#     rotated_cube = rotate_top(test_cube)
    
#     # Test that the top face is rotated clockwise
#     # Original: [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
#     # Expected after clockwise rotation: [['7', '4', '1'], ['8', '5', '2'], ['9', '6', '3']]
#     expected_top = np.array([['7', '4', '1'], ['8', '5', '2'], ['9', '6', '3']])
#     np.testing.assert_array_equal(rotated_cube[top], expected_top)
    
#     # Test that other faces are not changed
#     np.testing.assert_array_equal(rotated_cube[bottom], test_cube[bottom])
#     np.testing.assert_array_equal(rotated_cube[left], test_cube[left])
#     np.testing.assert_array_equal(rotated_cube[right], test_cube[right])
#     np.testing.assert_array_equal(rotated_cube[front], test_cube[front])
#     np.testing.assert_array_equal(rotated_cube[back], test_cube[back])

# def test_rotate_top_preserves_cube_structure(test_cube):
#     """Test that rotate_top preserves the overall cube structure"""
#     rotated_cube = rotate_top(test_cube)
    
#     # Test that the cube shape is preserved
#     assert rotated_cube.shape == test_cube.shape
#     assert rotated_cube.dtype == test_cube.dtype
    
#     # Test that no values are lost (all positions should still have values)
#     assert not np.any(rotated_cube == '')

# def test_reorient_u(test_cube):
#     """Test reorient with 'U' (no change)"""
#     reoriented = reorient(test_cube, 'U')
#     np.testing.assert_array_equal(reoriented, test_cube)

# def test_reorient_d(test_cube):
#     """Test reorient with 'D' (rotate 180 degrees around Y axis)"""
#     reoriented = reorient(test_cube, 'D')
    
#     # After rotating 180 degrees around Y axis, top and bottom should be swapped
#     np.testing.assert_array_equal(reoriented[top], test_cube[bottom])
#     np.testing.assert_array_equal(reoriented[bottom], test_cube[top])
    
#     # Left and right should be flipped
#     np.testing.assert_array_equal(reoriented[left], np.flip(test_cube[right], axis=1))
#     np.testing.assert_array_equal(reoriented[right], np.flip(test_cube[left], axis=1))

# def test_reorient_l(test_cube):
#     """Test reorient with 'L' (rotate 90 degrees around Y axis)"""
#     reoriented = reorient(test_cube, 'L')
    
#     # Test that the cube structure is preserved
#     assert reoriented.shape == test_cube.shape
#     assert reoriented.dtype == test_cube.dtype

# def test_reorient_r(test_cube):
#     """Test reorient with 'R' (rotate 270 degrees around Y axis)"""
#     reoriented = reorient(test_cube, 'R')
    
#     # Test that the cube structure is preserved
#     assert reoriented.shape == test_cube.shape
#     assert reoriented.dtype == test_cube.dtype

# def test_reorient_f(test_cube):
#     """Test reorient with 'F' (rotate 90 degrees around Z axis)"""
#     reoriented = reorient(test_cube, 'F')
    
#     # Test that the cube structure is preserved
#     assert reoriented.shape == test_cube.shape
#     assert reoriented.dtype == test_cube.dtype

# def test_reorient_b(test_cube):
#     """Test reorient with 'B' (rotate 270 degrees around Z axis)"""
#     reoriented = reorient(test_cube, 'B')
    
#     # Test that the cube structure is preserved
#     assert reoriented.shape == test_cube.shape
#     assert reoriented.dtype == test_cube.dtype

# def test_perm_u(test_cube):
#     """Test perm with 'U' (rotate top face clockwise)"""
#     permuted = perm('U', test_cube)
    
#     # Should be equivalent to rotate_top
#     expected = rotate_top(test_cube)
#     np.testing.assert_array_equal(permuted, expected)

# def test_perm_u_prime(test_cube):
#     """Test perm with 'U'' (rotate top face counterclockwise)"""
#     permuted = perm("U'", test_cube)
    
#     # Should be equivalent to 3 clockwise rotations
#     expected = test_cube.copy()
#     for _ in range(3):
#         expected = rotate_top(expected)
#     np.testing.assert_array_equal(permuted, expected)

# def test_perm_d(test_cube):
#     """Test perm with 'D' (rotate bottom face clockwise)"""
#     permuted = perm('D', test_cube)
    
#     # Test that the cube structure is preserved
#     assert permuted.shape == test_cube.shape
#     assert permuted.dtype == test_cube.dtype

# def test_perm_l(test_cube):
#     """Test perm with 'L' (rotate left face clockwise)"""
#     permuted = perm('L', test_cube)
    
#     # Test that the cube structure is preserved
#     assert permuted.shape == test_cube.shape
#     assert permuted.dtype == test_cube.dtype

# def test_perm_r(test_cube):
#     """Test perm with 'R' (rotate right face clockwise)"""
#     permuted = perm('R', test_cube)
    
#     # Test that the cube structure is preserved
#     assert permuted.shape == test_cube.shape
#     assert permuted.dtype == test_cube.dtype

# def test_perm_f(test_cube):
#     """Test perm with 'F' (rotate front face clockwise)"""
#     permuted = perm('F', test_cube)
    
#     # Test that the cube structure is preserved
#     assert permuted.shape == test_cube.shape
#     assert permuted.dtype == test_cube.dtype

# def test_perm_b(test_cube):
#     """Test perm with 'B' (rotate back face clockwise)"""
#     permuted = perm('B', test_cube)
    
#     # Test that the cube structure is preserved
#     assert permuted.shape == test_cube.shape
#     assert permuted.dtype == test_cube.dtype

# def test_perm_preserves_cube_structure(test_cube):
#     """Test that perm preserves the overall cube structure for all faces"""
#     faces = ['U', 'D', 'L', 'R', 'F', 'B']
    
#     for face in faces:
#         permuted = perm(face, test_cube)
#         assert permuted.shape == test_cube.shape
#         assert permuted.dtype == test_cube.dtype
#         assert not np.any(permuted == '')

# def test_multiple_rotations(test_cube):
#     """Test that multiple rotations work correctly"""
#     # Apply multiple rotations
#     rotated = test_cube.copy()
#     rotated = perm('U', rotated)
#     rotated = perm('R', rotated)
#     rotated = perm("F'", rotated)
    
#     # Test that the cube structure is preserved
#     assert rotated.shape == test_cube.shape
#     assert rotated.dtype == test_cube.dtype
#     assert not np.any(rotated == '')

# def test_identity_operations(test_cube):
#     """Test that certain combinations of operations return to the original state"""
#     # U U' should return to original state
#     rotated = perm('U', test_cube)
#     rotated = perm("U'", rotated)
#     np.testing.assert_array_equal(rotated, test_cube)
    
#     # U U U U should return to original state (4 rotations = full circle)
#     rotated = test_cube.copy()
#     for _ in range(4):
#         rotated = perm('U', rotated)
#     np.testing.assert_array_equal(rotated, test_cube)

# def test_invalid_face_handling(test_cube):
#     """Test that invalid face inputs are handled gracefully"""
#     # This test assumes the functions will raise an exception for invalid inputs
#     # If they don't, we should test that they handle invalid inputs gracefully
    
#     # Test with invalid face in reorient
#     with pytest.raises(Exception):
#         reorient(test_cube, 'X')
    
#     # Test with invalid face in perm
#     with pytest.raises(Exception):
#         perm('X', test_cube)

# def test_cube_copy_behavior(test_cube):
#     """Test that functions return copies and don't modify the original cube"""
#     original_cube = test_cube.copy()
    
#     # Test rotate_top
#     rotated = rotate_top(test_cube)
#     np.testing.assert_array_equal(test_cube, original_cube)
#     assert rotated is not test_cube
    
#     # Test reorient
#     reoriented = reorient(test_cube, 'D')
#     np.testing.assert_array_equal(test_cube, original_cube)
#     assert reoriented is not test_cube
    
#     # Test perm
#     permuted = perm('U', test_cube)
#     np.testing.assert_array_equal(test_cube, original_cube)
#     assert permuted is not test_cube 