import random
import sys
import time
import threading
import os
import keyboard
from typing import List, Tuple, Generator
scaleSingleton:'Scale'=None
class Scale:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
    @classmethod
    def getInstance(cls):
        global scaleSingleton
        if scaleSingleton is None:
            scaleSingleton = cls(20, 40)
        return scaleSingleton

class Position:
    def __init__(self, x: int, y: int):
        if x < 0 or y < 0:
            raise IndexError('Position out of range')
        self.x = x
        self.y = y
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Position) and self.x == value.x and self.y == value.y

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
    def __init__(self, scale: Scale):
        self.scale = scale
        self.map = [[' ' for _ in range(scale.width)] for _ in range(scale.height)]
        self.snake = Snake(self)
        self.generate_food()

    def generate_food(self):
        self.food = Position(random.randint(0, self.scale.width - 1), random.randint(0, self.scale.height - 1))

    def render(self, Head_Char: str = '\033[36m@\033[0m', Body_Char: str = '\033[36m#\033[0m', Food_Char: str = '\033[31m*\033[0m') -> None:
        self.map = [[' ' for _ in range(self.scale.width)] for _ in range(self.scale.height)]
        self.snake.render(self, Head_Char, Body_Char)
        self.map[self.food.y][self.food.x] = Food_Char

    def mainloop(self, faceEnumGenerator: Generator[Tuple[int, int], None, None]) -> None:
        for faceEnum in faceEnumGenerator:
            try:
                targ: bool = False
                if self.snake.head == self.food:
                    targ = True
                    self.generate_food()
                if self.snake.head in self.snake.body:
                    break
                time.sleep(0.15)  
                self.snake.move(faceEnum, targ)  
                os.system('cls' if os.name == 'nt' else 'clear')  
                self.render()  
                print(' '+'-'*self.scale.width*2,end='\n|')
                for line in self.map:
                    for cell in line:
                        sys.stdout.write(cell +' ')
                    sys.stdout.write('|\n|')
                    sys.stdout.flush()
                print('\b '+'-'*self.scale.width*2)
            except IndexError:
                break  
        print(f'Game Over!,your length is:{len(self.snake.body)}')

class Snake:
    def __init__(self, map: Map):
        self.map = map
        self.head = self.generate_random_pos()
        self.body = []

    def generate_random_pos(self):
        return Position(random.randint(0, self.map.scale.width), random.randint(0, self.map.scale.height))

    def move(self, direction: Tuple[int, int], isEated: bool = False) -> None:
        hcp = Position(self.head.x, self.head.y)
        self.head.x += direction[0]
        self.head.y += direction[1]
        self.body.insert(0, hcp)
        if not isEated:
            self.body.pop()

    def render(self, map: Map, Head_Char: str, Body_Char: str) -> None:
        map.map[self.head.y][self.head.x] = Head_Char
        for body in self.body:
            map.map[body.y][body.x] = Body_Char


def faceEnumGenerator() -> Generator[Tuple[int, int], None, None]:
    rk = KeyChecker.readkey()
    while True:
        yield FaceEnum.get(rk.__next__())

print('\033[?25l')  
if __name__ == '__main__':
    map = Map(Scale.getInstance())  
    map.mainloop(faceEnumGenerator())