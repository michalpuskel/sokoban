import tkinter
from functools import reduce

class Sokoban:
    def __init__(self):
        self.map = []
        self.loadFile('mapa.txt')
        self.playerX, self.playerY = self.scanPlayerPosition()
        print(self)

        self.square = 64
        self.sokoHeading = 'up'

        self.canvas = tkinter.Canvas(bg='pale green', width=self.square * len(self.map[0]), height=self.square * len(self.map))
        self.canvas.pack()

        self.garbage = []
        self.draw()

    def loadFile(self, file):
        with open(file) as f:
            for line in f:
                self.map.append(list(line.strip()))

    def scanPlayerPosition(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == '@':
                    self.map[y][x] = '_'
                    return x, y

    def __repr__(self):
        return reduce(lambda acc, l: f'{acc}\n{l}', [f'{line}' for line in self.map])

    def draw(self):
        self.canvas.delete('all')

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                image = None
                if y == self.playerY and x == self.playerX:
                    image = 'character_' + self.sokoHeading
                elif self.map[y][x] == '$':
                    image = 'crate'
                elif self.map[y][x] == '.':
                    image = 'target_point'
                elif self.map[y][x] == '#':
                    image = 'wall'
                elif self.map[y][x] == '_':
                    pass
                elif self.map[y][x] == '!':
                    image = 'crate_gold'

                if image is not None:
                    img = tkinter.PhotoImage(file=f'obrazky/{image}.png')
                    self.canvas.create_image(x * self.square, y * self.square, image=img, anchor='nw')

                    self.garbage.append(img)

    #todo refactor
    def canMove(self, direction):
        newX, newY = self.playerX, self.playerY

        if direction == 'up':
            newY -= 1
        elif direction == 'down':
            newY += 1
        elif direction == 'left':
            newX -= 1
        elif direction == 'right':
            newX += 1

        if not (0 <= newX < len(self.map[0])):
           return False
        if not (0 <= newY < len(self.map)):
           return False

        if self.map[newY][newX] == '#':
            return False
        elif self.map[newY][newX] in '$!':
            return self.crateCanMove(newX, newY, direction)

        return True

    def crateCanMove(self, x, y, direction):
        ...

    def move(self):
        ...

    def crateMove(self):
        ...







trash = Sokoban()

tkinter.mainloop()