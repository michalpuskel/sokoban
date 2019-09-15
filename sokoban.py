import tkinter
from functools import reduce


class Sokoban:
    def __init__(self, mapFile):
        self.map = []
        self.loadFile(mapFile)
        self.playerX, self.playerY = self.scanPlayerPosition()
        print(self)

        self.square = 64
        self.sokoHeading = 'up'

        self.canvas = tkinter.Canvas(
            bg='pale green', width=self.square * len(self.map[0]), height=self.square * len(self.map))
        self.canvas.pack()

        self.mouseControls = False
        self.bindControls()

        self.defineImages()
        self.animate()

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

    def checkWinner(self):
        return len(list(filter(lambda c: c == '.', reduce(lambda acc, row: acc + row, self.map)))) == 0

    def animate(self):
        while True:
            if self.checkWinner():
                print('Winner!')

            self.draw()
            self.canvas.update()
            self.canvas.after(50)

    def defineImages(self):
        self.img_character_up = tkinter.PhotoImage(
            file='obrazky/character_up.gif')
        self.img_character_down = tkinter.PhotoImage(
            file='obrazky/character_down.gif')
        self.img_character_left = tkinter.PhotoImage(
            file='obrazky/character_left.gif')
        self.img_character_right = tkinter.PhotoImage(
            file='obrazky/character_right.gif')
        self.img_crate = tkinter.PhotoImage(file='obrazky/crate.gif')
        self.img_crate_gold = tkinter.PhotoImage(file='obrazky/crate_gold.gif')
        self.img_target_point = tkinter.PhotoImage(
            file='obrazky/target_point.gif')
        self.img_wall = tkinter.PhotoImage(file='obrazky/wall.gif')

    def draw(self):
        self.canvas.delete('all')

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                image = None
                if y == self.playerY and x == self.playerX:
                    if self.sokoHeading == 'up':
                        image = self.img_character_up
                    elif self.sokoHeading == 'down':
                        image = self.img_character_down
                    elif self.sokoHeading == 'left':
                        image = self.img_character_left
                    elif self.sokoHeading == 'right':
                        image = self.img_character_right
                    else:
                        image = self.img_character_down
                elif self.map[y][x] == '$':
                    image = self.img_crate
                elif self.map[y][x] == '.':
                    image = self.img_target_point
                elif self.map[y][x] == '#':
                    image = self.img_wall
                elif self.map[y][x] == '_':
                    pass
                elif self.map[y][x] == '!':
                    image = self.img_crate_gold

                if image is not None:
                    self.canvas.create_image(
                        x * self.square, y * self.square, image=image, anchor='nw')

    def playerMove(self, direction):
        playerCanMove, newX, newY = self.objectCanMove(
            self.playerX, self.playerY, direction)

        if not playerCanMove:
            if self.canMove(newX, newY) and self.map[newY][newX] in '$!':
                crateCanMove, crateFinalX, crateFinalY = self.objectCanMove(
                    newX, newY, direction)
                if crateCanMove:
                    self.crateMove(newX, newY, crateFinalX, crateFinalY)
                    # self.playerX, self.playerY = newX, newY
                return crateCanMove

            return False

        self.playerX, self.playerY = newX, newY
        return True

    def objectCanMove(self, x, y, direction):
        newX, newY = self.tryMove(x, y, direction)

        if not self.canMove(newY, newY):
            return False

        return self.map[newY][newX] in '_.', newX, newY

    def tryMove(self, x, y, direction):
        newX, newY = x, y

        if direction == 'up':
            newY -= 1
        elif direction == 'down':
            newY += 1
        elif direction == 'left':
            newX -= 1
        elif direction == 'right':
            newX += 1

        return newX, newY

    def canMove(self, newX, newY):
        return (0 <= newX < len(self.map[0])) and \
               (0 <= newY < len(self.map))

    def crateMove(self, fromX, fromY, newX, newY):
        if not self.map[fromY][fromX] in '$!':
            raise Exception('moved something as crate error')

        if not self.map[newY][newX] in '_.':
            raise Exception('moved crate to non free square error')

        self.map[fromY][fromX] = '_' if self.map[fromY][fromX] == '$' else '.'
        self.map[newY][newX] = '$' if self.map[newY][newX] == '_' else '!'

    def moveUp(self, _):
        self.sokoHeading = 'up'
        self.doMove()

    def moveDown(self, _):
        self.sokoHeading = 'down'
        self.doMove()

    def moveLeft(self, _):
        self.sokoHeading = 'left'
        self.doMove()

    def moveRight(self, _):
        self.sokoHeading = 'right'
        self.doMove()

    def doMove(self):
        self.playerMove(self.sokoHeading)

    def toggleMouseControl(self, _):
        self.mouseControls = not self.mouseControls
        if self.mouseControls:
            print('Mouse Control ON')
        else:
            print('Mouse Control OFF')

    def mouseMoveControl(self, event):
        if not self.mouseControls:
            return

        self.sokoHeading = self.convertMouseCoordsToMoveDirection(
            event.x, event.y)
        self.doMove()

    def convertMouseCoordsToMoveDirection(self, mouseX, mouseY):
        x = mouseX // self.square
        y = mouseY // self.square

        dx = x - self.playerX
        dy = y - self.playerY

        if dx == 0 == dy:
            return None

        if abs(dx) >= abs(dy):
            if dx < 0:
                return 'left'
            else:
                return'right'
        else:
            if dy < 0:
                return 'up'
            else:
                return 'down'

    def bindControls(self):
        self.canvas.bind_all('<Up>', self.moveUp)
        self.canvas.bind_all('<Down>', self.moveDown)
        self.canvas.bind_all('<Left>', self.moveLeft)
        self.canvas.bind_all('<Right>', self.moveRight)

        self.canvas.bind_all('w', self.moveUp)
        self.canvas.bind_all('s', self.moveDown)
        self.canvas.bind_all('a', self.moveLeft)
        self.canvas.bind_all('d', self.moveRight)

        self.canvas.bind_all('<space>', self.toggleMouseControl)
        self.canvas.bind('<Motion>', self.mouseMoveControl)
        self.canvas.bind('<ButtonPress>', self.mouseMoveControl)


Sokoban('mapa_easy.txt')

tkinter.mainloop()
