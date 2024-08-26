import random
import sys
import time
import threading
import os
import keyboard
import types
from typing import List, Tuple,Generator

# 定义一个类 KeyChecker 用于检测按键
class KeyChecker:
    pressedkey: str = 'w'  # 初始化默认按下的键为 'w'

    # 定义一个类方法 readkey
    @classmethod
    def readkey(cls) -> Generator[str, None, None]:
        # 定义一个内部类 p 继承自 threading.Thread
        class p(threading.Thread):
            def __init__(self) -> None:
                threading.Thread.__init__(self)
                self.daemon = True  # 将线程设置为守护线程
                # self.setDaemon(True)  # 重复设置守护线程，可删除此行
                self.start()  # 启动线程

            def run(self) -> None:
                # global pressedkey  # 此处不需要使用 global 关键字，因为使用的是类属性
                while True:
                    # 根据按下的不同键更新 pressedkey 的值
                    if keyboard.is_pressed('w'):
                        cls.pressedkey = 'w'
                    if keyboard.is_pressed('a'):
                        cls.pressedkey = 'a'
                    if keyboard.is_pressed('s'):
                        cls.pressedkey ='s'
                    if keyboard.is_pressed('d'):
                        cls.pressedkey = 'd'
                    time.sleep(0.05)  # 控制检测按键的频率
        p()  # 创建并启动线程
        while True:
            yield cls.pressedkey  # 生成器，不断产生按下的键

# 定义一个枚举类 FaceEnum 表示方向
class FaceEnum:
    LEFT: Tuple[int, int] = (-1, 0)
    RIGHT: Tuple[int, int] = (1, 0)
    UP: Tuple[int, int] = (0, -1)
    DOWN: Tuple[int, int] = (0, 1)

    # 静态方法根据输入的字符获取对应的方向
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

# 定义 Map 类表示游戏地图
class Map:
    def __init__(self, height: int, width: int) -> None:
        self.scale: Tuple[int, int] = (height, width)  # 地图的大小
        self.map: List[List[str]] = [[' ' for _ in range(width)] for _ in range(height)]  # 初始化地图
        self.snake: Snake = Snake(self)  # 创建蛇对象
        self.food: Tuple[int, int] = (random.randint(0, self.scale[1] - 1), random.randint(0, self.scale[0] - 1))  # 随机生成食物的位置

    # 渲染地图的方法
    def render(self, Head_Char: str = '\033[36m@\033[0m', Body_Char: str = '\033[36m#\033[0m', Food_Char: str = '\033[31m*\033[0m') -> None:
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                # 根据不同情况设置地图中的字符
                if (x, y) == self.snake.head:
                    self.map[y][x] = Head_Char
                elif (x, y) in self.snake.body:
                    self.map[y][x] = Body_Char
                elif (x, y) == self.food:
                    self.map[y][x] = Food_Char
                else:
                    self.map[y][x] =' '

    # 游戏主循环
    def mainloop(self, faceEnumGenerator: Generator[Tuple[int, int], None, None]) -> None:
        for faceEnum in faceEnumGenerator:
            try:
                targ: bool = False
                # 判断蛇是否吃到食物
                if self.snake.head == self.food:
                    targ = True
                    self.food = (random.randint(0, self.scale[1] - 1), random.randint(0, self.scale[0] - 1))
                # 判断蛇是否撞到自己
                if self.snake.head in self.snake.body:
                    break
                time.sleep(0.15)  # 控制游戏速度
                self.snake.move(faceEnum, targ)  # 让蛇移动
                os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
                self.render()  # 渲染地图
                for line in self.map:
                    for cell in line:
                        sys.stdout.write(cell +'')
                    sys.stdout.write('\n')
            except IndexError:
                break  
        print(f'Game Over!,your length is:{len(self.snake.body)}')

# 定义 Snake 类表示蛇
class Snake:   
    def __init__(self, map: Map) -> None:
        randomPos = lambda: (random.randint(0, map.scale[0]), random.randint(0, map.scale[1] - 1))     
        self.head: Tuple[int, int] = randomPos()
        self.body: List[Tuple[int, int]] = []

    # 蛇移动的方法
    def move(self, direction: Tuple[int, int], isEated: bool = False) -> None:
        hcp: Tuple[int, int] = self.head[:]
        self.head = (self.head[0] + direction[0], self.head[1] + direction[1])
        self.body.insert(0, hcp)
        if not isEated:
            self.body.pop()

# 生成方向枚举的生成器函数
def faceEnumGenerator() -> Generator[Tuple[int, int], None, None]:
    rk = KeyChecker.readkey()
    while True:
        yield FaceEnum.get(rk.__next__())

print('\033[?25l')  # 隐藏光标

if __name__ == '__main__':
    map = Map(20, 40)  # 创建地图对象
    map.mainloop(faceEnumGenerator())  # 启动游戏主循环