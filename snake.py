import random
import sys
import time
import keyboard
def readkey():
    ...
class FaceEnum:
    UP=(-1,0)
    DOWN=(1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)
    def __init__(self, char):
        if char == 'w':
            self.vector=FaceEnum.UP
        if char =='a':
            self.vector=FaceEnum.LEFT
        if char =='s':
            self.vector=FaceEnum.DOWN
        if char =='d':
            self.vector=FaceEnum.RIGHT
class Map:
    def __init__(self,height,width):
        self.scale=(height,width)
        self.map=[[' ' for _ in range(width)] for _ in range(height)]
        self.snake=Snake(self)
        self.food=(random.randint(0,height-1),random.randint(0,width-1))
    def render(self,Head_Char='@',Body_Char='#'):
        sys.stdout.clear()
        for y,row in enumerate(self.map):
            for x,cell in enumerate(row):
                if (x,y)==self.snake.head:
                    sys.stdout.write(Head_Char)
                elif (x,y) in self.snake.body:
                    sys.stdout.write(Body_Char)
                else:
                    sys.stdout.write(cell)
            sys.stdout.write('\n')
    def mainloop(self, faceEnumGenerator):
        while True:
            faceEnum=faceEnumGenerator.next()
            try:
                targ = False
                time.sleep(0.5)
                if self.snake.head == self.food:
                    targ = True
                    self.food = (random.randint(0, self.scale.height-1), random.randint(0, self.scale.width-1))
                if self.snake.head in self.snake.body:
                    break
                self.snake.move(faceEnum, targ)
                self.render()  
            except:
                break  
        sys.stdout.clear()
        print(f'Game Over!,your length is:{len(self.snake.body)}')    

class Snake:   
    def __init__(self,map):
        randomPos=lambda:(random.randint(0,map.scale.height-1),random.randint(0,map.scale.width-1))     
        self.head=randomPos()
        self.body=[]
    def move(self, direction, isEated=False):
        self.head[0] += direction[0]
        self.head[1] += direction[1]
        tmp=self.body[-1][:]
        self.body = [(i[0] + direction[0], i[1] + direction[1]) for i in self.body]  # Fixed: Use 'self.body' instead of 'body'
        if isEated:
            self.body.append(tmp)
def faceEnumGenerator():
    directions=[FaceEnum.UP,FaceEnum.DOWN,FaceEnum.LEFT,FaceEnum.RIGHT]
    while True:
        yield FaceEnum(readkey()).vector

if __name__=='__main__':
    map=Map(20,30)
    map.mainloop(faceEnumGenerator())

