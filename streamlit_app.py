import streamlit as st
import numpy as np
import random
from cube import new_cube, new_test_cube, perm, faces, top, bottom, left, right, front, back

# Page configuration
st.set_page_config(
    page_title="Rubik's Cube Visualizer",
    page_icon="🧊",
    layout="wide"
)

# Title
st.title("🧊 Rubik's Cube Visualizer")

# Initialize session state for cube
if 'cube' not in st.session_state:
    st.session_state.cube = new_cube()

if st.sidebar.button("🔀 Shuffle Cube"):
    # Define all possible moves
    all_moves = ['U', 'D', 'L', 'R', 'F', 'B', "U'", "D'", "L'", "R'", "F'", "B'"]
    
    # Apply 20 random moves
    for _ in range(20):
        random_move = random.choice(all_moves)
        st.session_state.cube = perm(random_move, st.session_state.cube)

c = st.sidebar.container() # Display the reset queue button after the selector
# Cube type selection
cube_type = st.sidebar.selectbox(
    "Cube Type",
    ["Standard Cube (Colors)", "Test Cube (Letters)"],
    index=0
)

# Reset button
if c.button("Reset cube"):
    if cube_type == "Standard Cube (Colors)":
        st.session_state.cube = new_cube()
    else:
        st.session_state.cube = new_test_cube()

# Move controls
st.sidebar.header("Moves")

# Create 2 columns for moves - each face and its prime on the same row
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("U", use_container_width=True):
        st.session_state.cube = perm("U", st.session_state.cube)
    if st.button("D", use_container_width=True):
        st.session_state.cube = perm("D", st.session_state.cube)
    if st.button("L", use_container_width=True):
        st.session_state.cube = perm("L", st.session_state.cube)
    if st.button("R", use_container_width=True):
        st.session_state.cube = perm("R", st.session_state.cube)
    if st.button("F", use_container_width=True):
        st.session_state.cube = perm("F", st.session_state.cube)
    if st.button("B", use_container_width=True):
        st.session_state.cube = perm("B", st.session_state.cube)

with col2:
    if st.button("U'", use_container_width=True):
        st.session_state.cube = perm("U'", st.session_state.cube)
    if st.button("D'", use_container_width=True):
        st.session_state.cube = perm("D'", st.session_state.cube)
    if st.button("L'", use_container_width=True):
        st.session_state.cube = perm("L'", st.session_state.cube)
    if st.button("R'", use_container_width=True):
        st.session_state.cube = perm("R'", st.session_state.cube)
    if st.button("F'", use_container_width=True):
        st.session_state.cube = perm("F'", st.session_state.cube)
    if st.button("B'", use_container_width=True):
        st.session_state.cube = perm("B'", st.session_state.cube)

# Function to create the cube layout like p() function
def create_cube_layout(cube):
    """Create the cube layout similar to the p() function"""
    
    # Create blank grids and strips like in p() function
    blank = np.zeros(3*3, dtype='str').reshape([3,3])
    blank[:,:] = ' '
    strip = np.zeros(3*1, dtype='str').reshape([3,1])
    strip[:,:] = ' '
    
    # Create blank rows for spacing
    blank_row = np.zeros(15, dtype='str')
    blank_row[:] = ' '
    
    # Build the layout with blank rows for spacing
    c = np.concatenate((
        np.concatenate((blank, strip, np.flip(np.transpose(cube[top]), axis=0), strip, blank, strip, blank), axis=1),
        [blank_row],  # Blank row after top face
        np.concatenate((np.flip(cube[left], axis=1), strip, cube[front], strip, cube[right], strip, np.flip(cube[back], axis=1)), axis=1),
        [blank_row],  # Blank row before bottom face
        np.concatenate((blank, strip, np.transpose(cube[bottom]), strip, blank, strip, blank), axis=1)
    ))
    
    return c

# Function to get color for each cell
def get_cell_color(value):
    """Get background color for a cell based on its value"""
    color_map = {
        'W': '#FFFFFF',  # White
        'Y': '#FFFF00',  # Yellow
        'O': '#FFA500',  # Orange
        'R': '#FF0000',  # Red
        'G': '#00FF00',  # Green
        'B': '#0000FF',  # Blue
        ' ': '#F0F0F0',  # Light gray for blank spaces
        '-': '#E0E0E0'   # Slightly darker gray for dashes
    }
    return color_map.get(value, '#FFFFFF')  # Default to white

# Function to create HTML grid display
def create_html_cube_display(data, use_colors=True):
    """Create HTML grid display for the cube"""
    html_parts = []
    
    # CSS styles
    css = """
    <style>
    .cube-grid {
        display: grid;
        grid-template-columns: repeat(15, 30px);
        grid-template-rows: repeat(11, 30px);
        gap: 1px;
        font-family: monospace;
        font-size: 15px;
        font-weight: bold;
        text-align: center;
        line-height: 30px;
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
        background-color: transparent;
        border: none;
    }
    </style>
    """
    
    html_parts.append(css)
    html_parts.append('<div class="cube-grid">')
    
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == ' ':
                # Blank space
                html_parts.append(f'<div class="cube-cell blank-cell"></div>')
            else:
                # Regular cell
                if use_colors:
                    bg_color = get_cell_color(cell)
                    # Use white text for blue and red backgrounds, black for others
                    text_color = 'white' if cell in ['B', 'R'] else 'black'
                    html_parts.append(f'<div class="cube-cell" style="background-color: {bg_color}; color: {text_color};">{cell}</div>')
                else:
                    html_parts.append(f'<div class="cube-cell" style="background-color: #f0f0f0; color: black;">{cell}</div>')
    
    html_parts.append('</div>')
    return ''.join(html_parts)

# Create the cube layout
cube_layout = create_cube_layout(st.session_state.cube)

# Display the cube layout with HTML grid
if cube_type == "Standard Cube (Colors)":
    # Use colored display for standard cube
    html_display = create_html_cube_display(cube_layout, use_colors=True)
else:
    # Use regular display for test cube
    html_display = create_html_cube_display(cube_layout, use_colors=False)

st.markdown(html_display, unsafe_allow_html=True)

# Move history (optional feature)
if 'move_history' not in st.session_state:
    st.session_state.move_history = []

# Add move to history when a move is made
# (This would need to be implemented with callbacks or state management)

st.sidebar.header("Move History")
if st.session_state.move_history:
    for i, move in enumerate(st.session_state.move_history):
        st.sidebar.write(f"{i+1}. {move}")
else:
    st.sidebar.write("No moves made yet")
