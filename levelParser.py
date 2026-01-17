import json
import re
from Blocks import block
from engine_math import Vector2 # type: ignore

def parse_vector(vector_string):
    """Parses a string of format Vector2(x,y) into a Vector2 object."""
    match = re.match(r"Vector2\(([^,]+),([^)]+)\)", vector_string)
    if match:
        return Vector2(int(match.group(1)), int(match.group(2)))
    else:
        raise ValueError(f"Invalid vector string: {vector_string}")

def parse_block(block_data):
    """Parses the block data into a Block object."""
    cords = parse_vector(block_data[0])
    pos = parse_vector(block_data[1])
    deadly = bool(block_data[2])
    tag = block_data[3]
    rot = block_data[4]
    
    return block(cords, pos, deadly, tag, rot)

def parse_json_file(filename: str):
    """Reads a JSON file and returns an array of Block objects."""
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Initialize the scene list
    scene = []
    
    # Iterate through each block in the JSON file and parse it
    for block_data in data:
        block = parse_block(block_data)
        scene.append(block)
    
    return scene

# print(parse_json_file("level.json")