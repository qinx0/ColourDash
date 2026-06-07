from engine_nodes import Text2DNode
from engine_math import Vector2

class OutlinedTextNode:
    def __init__(self, position=Vector2(0,0), font=None, text="",
                 scale=Vector2(1,1), color=(1,1,1),
                 outline_color=(0,0,0), layer=0, offset=1):
        self._text = text
        self._nodes = []
        for dx, dy in [(-1,-1), (1,-1), (-1,1), (1,1)]:
            n = Text2DNode(position=Vector2(position.x+dx*offset, position.y+dy*offset),
                font=font, text=text, scale=scale,
                color=outline_color, layer=layer)
            self._nodes.append(n)
        self._fill = Text2DNode(position=position, font=font, text=text,
            scale=scale, color=color, layer=layer)

    @property
    def text(self): return self._text
    @text.setter
    def text(self, v):
        self._text = v
        for n in self._nodes: n.text = v
        self._fill.text = v

    @property
    def opacity(self): return self._fill.opacity
    @opacity.setter
    def opacity(self, v):
        for n in self._nodes: n.opacity = v
        self._fill.opacity = v

    @property
    def position(self): return self._fill.position
    @position.setter
    def position(self, v):
        dx = v.x - self._fill.position.x
        dy = v.y - self._fill.position.y
        for n in self._nodes:
            n.position = Vector2(n.position.x+dx, n.position.y+dy)
        self._fill.position = v