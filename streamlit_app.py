import streamlit as st
import numpy as np
from cube import new_cube, new_test_cube, perm, faces, top, bottom, left, right, front, back, mix, cube_to_string
import streamlit_shortcuts as ss

st.set_page_config(page_title="Rubik's Cube Visualizer", page_icon="🧊", layout="wide")
st.title("🧊 Rubik's Cube Visualizer")

if 'cube' not in st.session_state:
    st.session_state.cube = new_cube()

if st.sidebar.button("🔀 Shuffle Cube"):
    st.session_state.cube = mix(st.session_state.cube)

c = st.sidebar.container() # Display the reset queue button after the selector
cube_type = st.sidebar.selectbox("Cube Type",
    ["Standard Cube", "Test Cube"], index=0)
def is_colored(): return cube_type == "Standard Cube"

if c.button("Reset cube"):
    st.session_state.cube = new_cube() if is_colored() else new_test_cube()

st.sidebar.header("Moves")
col1, col2 = st.sidebar.columns(2)
moves = ["U", "D", "L", "R", "F", "B"]
for move in moves:
    with col1:
        if st.button(move, use_container_width=True, key=move+'_button'):
            st.session_state.cube = perm(move, st.session_state.cube)  
    with col2:
        if st.button(move+"'", use_container_width=True, key=move+'_prime_button'):
            st.session_state.cube = perm(move+"'", st.session_state.cube)

def get_cell_color(value):
    if not is_colored(): return '#FFFFFF' # White
    color_map = {
        'W': '#FFFFFF',  # White
        'Y': '#FFFF00',  # Yellow
        'O': '#FFA500',  # Orange
        'R': '#FF0000',  # Red
        'G': '#00FF00',  # Green
        'B': '#0000FF',  # Blue
    }
    return color_map.get(value, '#FFFFFF')  # Default to white

# Function to create HTML grid display
def cube_to_html(data):  
    css = """<style>
                .cube-grid {
                    display: grid;
                    grid-template-columns: repeat(15, auto);
                    grid-template-rows: repeat(11, auto);
                    font-family: monospace;
                    font-size: 15px;
                    width: fit-content;
                    margin: 0 auto;
                }
                .cube-cell {
                    width: 30px;
                    height: 30px;
                    border: 1px solid #ccc;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .blank-cell {
                    width: 15px;
                    height: 15px;
                }
            </style>"""
    
    html_parts = [css, '<div class="cube-grid">']
    for row in data:
        for cell in row:
            if cell == ' ':
                html_parts.append(f'<div class="blank-cell"> </div>')
            else:
                # Use white text for blue and red backgrounds, black for others
                text_color = 'white' if is_colored() and cell in ['B', 'R'] else 'black'
                style = f'style="background-color: {get_cell_color(cell)}; color: {text_color};"'
                html_parts.append(f'<div class="cube-cell" {style}>{cell}</div>')
    
    html_parts.append('</div>')
    return ''.join(html_parts)

cube_layout = cube_to_string(st.session_state.cube).split("\n")
cube_layout = [row[::2] for row in cube_layout] # Remove whitespace between squares
cube_layout.insert(3, " " * 15) # insert a blank row between cube faces
cube_layout.insert(7, " " * 15)
st.markdown(cube_to_html(cube_layout), unsafe_allow_html=True)

# Add keyboard shortcuts. To do: call add_shortcuts() only once, with one big argument list.
# Right now, each shortcut is taking up a little bit of space.
for move in moves:
    ss.add_shortcuts(**{move+'_button': move.lower()})
    ss.add_shortcuts(**{move+'_prime_button': 'shift+' + move.lower()})

st.markdown("""Press **U/D/L/R/F/B** to rotate clockwise, and **shift+U/D/L/R/F/B** for counterclockwise.""")
