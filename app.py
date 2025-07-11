from flask import Flask, render_template, request, jsonify, session
import numpy as np
from cube import new_cube, new_test_cube, do_move, mix, cube_to_string
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_cell_color(value, is_colored):
    if not is_colored:
        return '#FFFFFF'  # White
    color_map = {
        'W': '#FFFFFF',  # White
        'Y': '#FFFF00',  # Yellow
        'O': '#ff8819',  # Orange
        'R': '#FF0000',  # Red
        'G': '#24c932',  # Green
        'B': '#055af7',  # Blue
    }
    return color_map.get(value, '#FFFFFF')  # Default to white

def cube_to_html(data, is_colored):
    def cell_to_html(cell):
        if cell == ' ':
            return f'<div class="blank-cell"> </div>'
        else:
            # Use white text for blue and red backgrounds, black for others
            text_color = 'white' if is_colored and cell in ['B', 'R'] else 'black'
            style = f'style="background-color: {get_cell_color(cell, is_colored)}; color: {text_color};"'
            return f'<div class="cube-cell" {style}>{cell}</div>'

    html_cells = [cell_to_html(cell) for row in data for cell in row]
    return f'<div class="cube-grid"> {"".join(html_cells)}</div>'

@app.route('/')
def index():
    if 'cube' not in session:
        session['cube'] = new_cube().tolist()
    
    cube = np.array(session['cube'])
    cube_type = session.get('cube_type', 'Standard Cube')
    is_colored = cube_type == "Standard Cube"
    
    # Convert cube to string and format for display
    cube_layout = cube_to_string(cube).split("\n")
    cube_layout = [row[::2] for row in cube_layout]  # Remove whitespace between squares
    cube_layout.insert(3, " " * 15)  # insert a blank row between cube faces
    cube_layout.insert(7, " " * 15)
    
    cube_html = cube_to_html(cube_layout, is_colored)
    
    return render_template('index.html', 
                         cube_html=cube_html, 
                         cube_type=cube_type,
                         is_colored=is_colored)

@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    move = data.get('move')
    
    if 'cube' not in session:
        session['cube'] = new_cube().tolist()
    
    cube = np.array(session['cube'])
    cube = do_move(move, cube)
    session['cube'] = cube.tolist()
    
    # Return updated cube HTML
    cube_type = session.get('cube_type', 'Standard Cube')
    is_colored = cube_type == "Standard Cube"
    
    cube_layout = cube_to_string(cube).split("\n")
    cube_layout = [row[::2] for row in cube_layout]
    cube_layout.insert(3, " " * 15)
    cube_layout.insert(7, " " * 15)
    
    cube_html = cube_to_html(cube_layout, is_colored)
    
    return jsonify({'cube_html': cube_html})

@app.route('/mix', methods=['POST'])
def mix_cube():
    if 'cube' not in session:
        session['cube'] = new_cube().tolist()
    
    cube = np.array(session['cube'])
    cube = mix(cube)
    session['cube'] = cube.tolist()
    
    cube_type = session.get('cube_type', 'Standard Cube')
    is_colored = cube_type == "Standard Cube"
    
    cube_layout = cube_to_string(cube).split("\n")
    cube_layout = [row[::2] for row in cube_layout]
    cube_layout.insert(3, " " * 15)
    cube_layout.insert(7, " " * 15)
    
    cube_html = cube_to_html(cube_layout, is_colored)
    
    return jsonify({'cube_html': cube_html})

@app.route('/reset', methods=['POST'])
def reset_cube():
    data = request.get_json()
    cube_type = data.get('cube_type', 'Standard Cube')
    
    if cube_type == "Standard Cube":
        cube = new_cube()
    else:
        cube = new_test_cube()
    
    session['cube'] = cube.tolist()
    session['cube_type'] = cube_type
    
    is_colored = cube_type == "Standard Cube"
    
    cube_layout = cube_to_string(cube).split("\n")
    cube_layout = [row[::2] for row in cube_layout]
    cube_layout.insert(3, " " * 15)
    cube_layout.insert(7, " " * 15)
    
    cube_html = cube_to_html(cube_layout, is_colored)
    
    return jsonify({'cube_html': cube_html})

if __name__ == '__main__':
    app.run(debug=True) 