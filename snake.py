import random
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)
class FaceEnum:
    UP=(-1,0)
    DOWN=(1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)
class Map:
    def __init__(self,height,width):
        self.scale=(height,width)
        self.map=[[' ' for _ in range(width)] for _ in range(height)]
        self.snake=Snake(self)
class Snake:   
    def __init__(self,map):
        randomPos=lambda:(random.randint(0,map.scale.height-1),random.randint(0,map.scale.width-1))     
        self.head=randomPos()
        self.body=[]
def move(self, direction, isEated=False):
    if isEated:
        self.body.append(self.head[:])  # Fixed: Append a copy of the head
    self.head[0] += direction[0]
    self.head[1] += direction[1]
    self.body = [(i[0] + direction[0], i[1] + direction[1]) for i in self.body]  # Fixed: Use 'self.body' instead of 'body'
