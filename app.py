from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import numpy as np
from cube import new_cube, new_test_cube, do_move, mix, cube_to_string
import os
import base64
import pickle

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
    return "".join(html_cells)

def encode_cube_state(cube):
    """Encode cube state as base64 for URL parameter"""
    return base64.b64encode(pickle.dumps(cube)).decode('utf-8')

def decode_cube_state(encoded_state):
    """Decode cube state from base64 URL parameter"""
    try:
        return pickle.loads(base64.b64decode(encoded_state.encode('utf-8')))
    except:
        return None

@app.route('/')
def index():
    # Get cube state from query parameter or use default
    cube_state = request.args.get('state')
    cube_type = request.args.get('type', 'Standard Cube')
    
    if cube_state:
        cube = decode_cube_state(cube_state)
        if cube is None:
            # Invalid state parameter, use default
            cube = new_cube() if cube_type == "Standard Cube" else new_test_cube()
    else:
        cube = new_cube() if cube_type == "Standard Cube" else new_test_cube()
    
    is_colored = cube_type == "Standard Cube"
    
    # Convert cube to string and format for display
    cube_layout = cube_to_string(cube).split("\n")
    cube_layout = [row[::2] for row in cube_layout]  # Remove whitespace between squares
    cube_layout.insert(3, " " * 15)  # insert a blank row between cube faces
    cube_layout.insert(7, " " * 15)
    
    cube_html = cube_to_html(cube_layout, is_colored)
    current_state = encode_cube_state(cube)
    
    return render_template('index.html', 
                         cube_html=cube_html, 
                         cube_type=cube_type,
                         is_colored=is_colored,
                         current_state=current_state)

@app.route('/move/<move>')
def make_move(move):
    # Get current state from query parameter
    cube_state = request.args.get('state')
    cube_type = request.args.get('type', 'Standard Cube')
    
    if cube_state:
        cube = decode_cube_state(cube_state)
        if cube is None:
            return redirect(url_for('index'))
    else:
        cube = new_cube() if cube_type == "Standard Cube" else new_test_cube()
    
    cube = do_move(move, cube)
    new_state = encode_cube_state(cube)
    return redirect(url_for('index', state=new_state, type=cube_type))

@app.route('/mix')
def mix_cube():
    cube_type = request.args.get('type', 'Standard Cube')
    cube_state = request.args.get('state')
    
    if cube_state:
        cube = decode_cube_state(cube_state)
        if cube is None:
            cube = new_cube() if cube_type == "Standard Cube" else new_test_cube()
    else:
        cube = new_cube() if cube_type == "Standard Cube" else new_test_cube()
    
    cube = mix(cube)
    new_state = encode_cube_state(cube)
    return redirect(url_for('index', state=new_state, type=cube_type))

@app.route('/reset')
def reset_cube():
    cube_type = request.args.get('type', 'Standard Cube')
    
    cube = new_cube() if cube_type == "Standard Cube" else new_test_cube()
    new_state = encode_cube_state(cube)
    return redirect(url_for('index', state=new_state, type=cube_type))

if __name__ == '__main__':
    app.run(debug=True) 