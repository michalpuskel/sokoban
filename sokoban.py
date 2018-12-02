import tkinter
from functools import reduce

class Sokoban:
    def __init__(self, square=64):
        self.map = []
        self.loadFile('mapa.txt')
        print(self)

        self.square = (square // 64) * 64
        self.scale = self.square // 64
        print(self.scale)
        self.sokoHeading = 'up'

        self.canvas = tkinter.Canvas(bg='pale green', width=self.square * len(self.map[0]), height=self.square * len(self.map))
        self.canvas.pack()

        self.garbage = []
        self.draw()

    def loadFile(self, file):
        with open(file) as f:
            for line in f:
                self.map.append(list(line.strip()))

    def __repr__(self):
        return reduce(lambda acc, l: f'{acc}\n{l}', [f'{line}' for line in self.map])

    def draw(self):
        self.canvas.delete('all')

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                image = None
                if self.map[y][x] == '@':
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
                    img.zoom(self.scale, self.scale)
                    self.canvas.create_image(x * self.square, y * self.square, image=img, anchor='nw')

                    self.garbage.append(img)







trash = Sokoban(200)

tkinter.mainloop()