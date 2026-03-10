import json
import re
from blocks import block
from engine_math import Vector2 # type: ignore

def parse_vector(vector_string):
    """Parses a string of format Vector2(x,y) into a Vector2 object."""
    match = re.match(r"Vector2\(([^,]+),([^)]+)\)", vector_string)
    if match:
        return Vector2(int(match.group(1)), int(match.group(2)))
    else:
        raise ValueError(f"Invalid vector string: {vector_string}")

def parse_block(block_data):
    """Parses a single block data entry into a Block object."""
    cords = parse_vector(block_data[0])
    pos = parse_vector(block_data[1])
    deadly = bool(block_data[2])
    tag = block_data[4]
    rot = block_data[5]
    portal = bool(block_data[3])
    return block(cords, pos, deadly, portal, tag, rot)

def load_raw(filename: str):
    """Reads a JSON file and returns the raw list without constructing blocks."""
    with open(filename, 'r') as file:
        return json.load(file)

def parse_json_file(filename: str):
    """Reads a JSON file and returns an array of Block objects."""
    data = load_raw(filename)
    return [parse_block(b) for b in data]