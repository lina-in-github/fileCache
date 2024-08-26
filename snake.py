import random
import sys
import time
import threading
import os
import keyboard
import types

class KeyChecker:
    pressedkey='w'
    @classmethod
    def readkey(cls):
        class p(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.daemon = True
                self.setDaemon(True)
                self.start()
            def run(self):
                #global pressedkey
                while True:
                    if keyboard.is_pressed('w'):
                        cls.pressedkey='w'
                    if keyboard.is_pressed('a'):
                        cls.pressedkey='a'
                    if keyboard.is_pressed('s'):
                        cls.pressedkey='s'
                    if keyboard.is_pressed('d'):
                        cls.pressedkey='d'
                    time.sleep(0.1)
        p()
        while True:
            yield cls.pressedkey
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
        self.food=(random.randint(0,self.scale[1]-1),random.randint(0,self.scale[0]-1))
    def render(self, Head_Char='\033[36m@\033[0m', Body_Char='\033[36m#\033[0m',Food_Char='\033[31m*\033[0m'):
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
    def mainloop(self, faceEnumGenerator):
        for faceEnum in faceEnumGenerator:
            try:
                targ = False
                if self.snake.head == self.food:
                    targ = True
                    self.food = (random.randint(0, self.scale[1]-1), random.randint(0, self.scale[0]-1))
                if self.snake.head in self.snake.body:
                    break
                time.sleep(0.15)
                self.snake.move(faceEnum, targ)
                os.system('cls' if os.name == 'nt' else 'clear') 
                self.render()  
                for line in self.map:
                    for cell in line:
                        sys.stdout.write(cell+' ')
                    sys.stdout.write('\n')
            except IndexError:
                break  
        print(f'Game Over!,your length is:{len(self.snake.body)}')
class Snake:   
    def __init__(self,map):
        randomPos=lambda:(random.randint(0,map.scale[0]),random.randint(0,map.scale[1]-1))     
        self.head=randomPos()
        self.body=[]
    def move(self, direction, isEated=False):
        hcp=self.head[:]
        self.head=(self.head[0]+direction[0],self.head[1]+direction[1])
        self.body.insert(0,hcp)
        if not isEated:
            self.body.pop()
def faceEnumGenerator():
    rk=KeyChecker.readkey()
    while True:
        yield FaceEnum.get(rk.__next__())
print('\033[?25l')
if __name__=='__main__':
    map=Map(20,40)
    map.mainloop(faceEnumGenerator())