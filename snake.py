import random
import sys
import time
import threading
import os
import keyboard
pressedkey='w'
def readkey():
    class p(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
            self.setDaemon(True)
            self.start()
        def run(self):
            global pressedkey
            while True:
                if keyboard.is_pressed('w'):
                    pressedkey='w'
                if keyboard.is_pressed('a'):
                    pressedkey='a'
                if keyboard.is_pressed('s'):
                    pressedkey='s'
                if keyboard.is_pressed('d'):
                    pressedkey='d'
                time.sleep(0.01)
    p()
    while True:
        yield pressedkey
class FaceEnum:
    LEFT=(-1,0)
    RIGHT=(1,0)
    UP=(0,-1)
    DOWN=(0,1)
    @staticmethod
    def get(char):
        if char == 'w':
            return FaceEnum.UP
        if char =='a':
            return FaceEnum.LEFT
        if char =='s':
            return FaceEnum.DOWN
        if char =='d':
            return FaceEnum.RIGHT
class Map:
    def __init__(self,height,width):
        self.scale=(height,width)
        self.map=[[' ' for _ in range(width)] for _ in range(height)]
        self.snake=Snake(self)
        self.food=(random.randint(0,height-1),random.randint(0,width-1))
    def render(self, Head_Char='@', Body_Char='#',Food_Char='*'):
        #sdwadwsys.stdout.write('\033[H\033[2J')  # Clear the screen and move the cursor to the top-left corner
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if (x, y) == self.snake.head:
                    self.map[y][x] =Head_Char
                elif (x, y) in self.snake.body:
                    self.map[y][x] = Body_Char
                elif (x, y) == self.food:
                    self.map[y][x] = Food_Char
                else:
                    self.map[y][x] =' '
                #sys.stdout.write(cell)
    def mainloop(self, faceEnumGenerator):
        for faceEnum in faceEnumGenerator:
            try:
                targ = False
                time.sleep(0.5)
                os.system('cls' if os.name == 'nt' else 'clear')  # FIXME:Fail to clear screen
                if self.snake.head == self.food:
                    targ = True
                    self.food = (random.randint(0, self.scale[0]-1), random.randint(0, self.scale[1]-1))
                if self.snake.head in self.snake.body:
                    break
                self.snake.move(faceEnum, targ)
                self.render()  
                for line in self.map:
                    for cell in line:
                        sys.stdout.write(cell)
                    sys.stdout.write('\n')
                
            except IndexError as e:
                raise
                break  
            #print('\033[2J')
        print(f'Game Over!,your length is:{len(self.snake.body)}')

class Snake:   
    def __init__(self,map):
        randomPos=lambda:(random.randint(0,map.scale[0]),random.randint(0,map.scale[1]-1))     
        self.head=randomPos()
        self.body=[]
    def move(self, direction, isEated=False):
        self.head=(self.head[0]+direction[0],self.head[1]+direction[1])
        tmp=self.body[len(self.body)-1][:] if len(self.body)!=0 else self.head
        self.body = [(i[0] + direction[0], i[1] + direction[1]) for i in self.body]  # Fixed: Use 'self.body' instead of 'body'
        if isEated:
            self.body.append(tmp)
def faceEnumGenerator():
    directions=[FaceEnum.UP,FaceEnum.DOWN,FaceEnum.LEFT,FaceEnum.RIGHT]
    rk=readkey()
    while True:
        yield FaceEnum.get(rk.__next__())
print('\033[?25l')
if __name__=='__main__':
    map=Map(20,30)
    map.mainloop(faceEnumGenerator())

