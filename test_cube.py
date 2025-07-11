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
    results = [flatten_cube(do_move(p, new_test_cube())) 
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
