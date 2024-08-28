import random
import sys
import time
import threading
import os
import keyboard
from typing import List, Tuple,Generator

class KeyChecker:
    pressedkey: str = 'w'  
    @classmethod
    def readkey(cls) -> Generator[str, None, None]:
        
        class p(threading.Thread):
            def __init__(self) -> None:
                threading.Thread.__init__(self)
                self.daemon = True  
                
                self.start()  

            def run(self) -> None:
                while True:
                    
                    if keyboard.is_pressed('w'):
                        cls.pressedkey = 'w'
                    if keyboard.is_pressed('a'):
                        cls.pressedkey = 'a'
                    if keyboard.is_pressed('s'):
                        cls.pressedkey ='s'
                    if keyboard.is_pressed('d'):
                        cls.pressedkey = 'd'
                    time.sleep(0.05)  
        p()  
        while True:
            yield cls.pressedkey  


class FaceEnum:
    LEFT: Tuple[int, int] = (-1, 0)
    RIGHT: Tuple[int, int] = (1, 0)
    UP: Tuple[int, int] = (0, -1)
    DOWN: Tuple[int, int] = (0, 1)

    @staticmethod
    def get(char: str) -> Tuple[int, int]:
        if char == 'w':
            return FaceEnum.UP
        if char == 'a':
            return FaceEnum.LEFT
        if char =='s':
            return FaceEnum.DOWN
        if char == 'd':
            return FaceEnum.RIGHT


class Map:
    def __init__(self, height: int, width: int) -> None:
        self.scale: Tuple[int, int] = (height, width)  
        self.map: List[List[str]] = [[' ' for _ in range(width)] for _ in range(height)]  
        self.snake: Snake = Snake(self)  
        self.food: Tuple[int, int] = (random.randint(0, self.scale[1] - 1), random.randint(0, self.scale[0] - 1))  

    def render(self, Head_Char: str = '\033[36m@\033[0m', Body_Char: str = '\033[36m#\033[0m', Food_Char: str = '\033[31m*\033[0m') -> None:
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                
                if (x, y) == self.snake.head:
                    self.map[y][x] = Head_Char
                elif (x, y) in self.snake.body:
                    self.map[y][x] = Body_Char
                elif (x, y) == self.food:
                    self.map[y][x] = Food_Char
                else:
                    self.map[y][x] =' '

    def mainloop(self, faceEnumGenerator: Generator[Tuple[int, int], None, None]) -> None:
        for faceEnum in faceEnumGenerator:
            try:
                targ: bool = False
                
                if self.snake.head == self.food:
                    targ = True
                    self.food = (random.randint(0, self.scale[1] - 1), random.randint(0, self.scale[0] - 1))
                if self.snake.head in self.snake.body:
                    break
                time.sleep(0.15)  
                self.snake.move(faceEnum, targ)  
                os.system('cls' if os.name == 'nt' else 'clear')  
                self.render()  
                print(' '+'-'*self.scale[1]*2,end='\n|')
                for line in self.map:
                    for cell in line:
                        sys.stdout.write(cell +' ')
                    sys.stdout.write('|\n|')
                    sys.stdout.flush()
                print('\b '+'-'*self.scale[1]*2)
            except IndexError:
                break  
        print(f'Game Over!,your length is:{len(self.snake.body)}')

class Snake:   
    def __init__(self, map: Map) -> None:
        randomPos = lambda: (random.randint(0, map.scale[0]), random.randint(0, map.scale[1] - 1))     
        self.head: Tuple[int, int] = randomPos()
        self.body: List[Tuple[int, int]] = []


    def move(self, direction: Tuple[int, int], isEated: bool = False) -> None:
        hcp: Tuple[int, int] = self.head[:]
        self.head = (self.head[0] + direction[0], self.head[1] + direction[1])
        self.body.insert(0, hcp)
        if not isEated:
            self.body.pop()


def faceEnumGenerator() -> Generator[Tuple[int, int], None, None]:
    rk = KeyChecker.readkey()
    while True:
        yield FaceEnum.get(rk.__next__())

print('\033[?25l')  
if __name__ == '__main__':
    map = Map(20, 40)  
    map.mainloop(faceEnumGenerator()) 