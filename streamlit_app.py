import streamlit as st
import numpy as np
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

# Sidebar controls
st.sidebar.header("Controls")

# Cube type selection
cube_type = st.sidebar.selectbox(
    "Cube Type",
    ["Standard Cube (Colors)", "Test Cube (Letters)"],
    index=0
)

if cube_type == "Standard Cube (Colors)":
    if st.sidebar.button("Reset to Standard Cube"):
        st.session_state.cube = new_cube()
else:
    if st.sidebar.button("Reset to Test Cube"):
        st.session_state.cube = new_test_cube()

# Move controls
st.sidebar.header("Moves")
moves = ['U', 'D', 'L', 'R', 'F', 'B', "U'", "D'", "L'", "R'", "F'", "B'"]

# Create 3 columns for moves
col1, col2, col3 = st.sidebar.columns(3)

with col1:
    if st.button("U"):
        st.session_state.cube = perm("U", st.session_state.cube)
    if st.button("D"):
        st.session_state.cube = perm("D", st.session_state.cube)
    if st.button("L"):
        st.session_state.cube = perm("L", st.session_state.cube)

with col2:
    if st.button("R"):
        st.session_state.cube = perm("R", st.session_state.cube)
    if st.button("F"):
        st.session_state.cube = perm("F", st.session_state.cube)
    if st.button("B"):
        st.session_state.cube = perm("B", st.session_state.cube)

with col3:
    if st.button("U'"):
        st.session_state.cube = perm("U'", st.session_state.cube)
    if st.button("D'"):
        st.session_state.cube = perm("D'", st.session_state.cube)
    if st.button("L'"):
        st.session_state.cube = perm("L'", st.session_state.cube)

# Additional moves
col4, col5, col6 = st.sidebar.columns(3)
with col4:
    if st.button("R'"):
        st.session_state.cube = perm("R'", st.session_state.cube)
with col5:
    if st.button("F'"):
        st.session_state.cube = perm("F'", st.session_state.cube)
with col6:
    if st.button("B'"):
        st.session_state.cube = perm("B'", st.session_state.cube)

# Function to create the cube layout like p() function
def create_cube_layout(cube):
    """Create the cube layout similar to the p() function"""
    import numpy as np
    
    # Create blank grids and strips like in p() function
    blank = np.zeros(3*3, dtype='str').reshape([3,3])
    blank[:,:] = ' '
    strip = np.zeros(3*1, dtype='str').reshape([3,1])
    strip[:,:] = ' '
    
    # Build the layout exactly like p() function
    c = np.concatenate((
        np.concatenate((blank, strip, np.flip(np.transpose(cube[top]), axis=0), strip, blank, strip, blank), axis=1),
        np.concatenate((np.flip(cube[left], axis=1), strip, cube[front], strip, cube[right], strip, np.flip(cube[back], axis=1)), axis=1),
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

# Function to create styled dataframe with colors
def create_colored_dataframe(data):
    """Create a dataframe with colored backgrounds"""
    import pandas as pd
    
    # Convert numpy array to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Apply styling with background colors and compact sizing
    def style_cell(val):
        color = get_cell_color(val)
        return f'background-color: {color}; color: black; text-align: center; font-weight: bold; padding: 2px; font-size: 12px;'
    
    styled_df = df.style.applymap(style_cell)
    return styled_df

# Main display area
st.header("Cube Display")

# Create the cube layout
cube_layout = create_cube_layout(st.session_state.cube)

# Display the cube layout with colors
if cube_type == "Standard Cube (Colors)":
    # Use colored display for standard cube
    styled_layout = create_colored_dataframe(cube_layout)
    st.dataframe(
        styled_layout,
        hide_index=True,
        use_container_width=False,
        width=400  # Much narrower to fit all faces
    )
else:
    # Use regular display for test cube
    st.dataframe(
        cube_layout,
        hide_index=True,
        column_config={
            str(i): st.column_config.TextColumn("", width="tiny") for i in range(cube_layout.shape[1])
        },
        use_container_width=False,
        width=400  # Much narrower to fit all faces
    )

# Add face labels for reference
st.markdown("""
**Face Layout:**
- Top face is in the center-top
- Left face is on the left (flipped horizontally)
- Front face is in the center
- Right face is on the right
- Back face is on the far right (flipped horizontally)
- Bottom face is in the center-bottom
""")

# Additional information
st.sidebar.header("Information")
st.sidebar.write(f"**Cube Shape:** {st.session_state.cube.shape}")
st.sidebar.write(f"**Data Type:** {st.session_state.cube.dtype}")

# Flattened cube string
st.sidebar.header("Flattened Cube")
flattened = ''.join(st.session_state.cube.flatten())
st.sidebar.text_area("Flattened Cube String", flattened, height=100)

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

# Footer
st.markdown("---")
st.markdown("**Rubik's Cube Visualizer** - Built with Streamlit and NumPy") 