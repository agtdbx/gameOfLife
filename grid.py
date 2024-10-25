import pygame as pg

from pygame.math import Vector2 as vec2
from define import  NB_W_TILE, NB_H_TILE,\
                    MIN_TILE_SIZE, START_TILE_SIZE, MAX_TILE_SIZE,\
                    TILE_FILL_COLOR, TILE_EMPTY_COLOR, \
                    WIN_W, WIN_H

class    Grid:
    def __init__(self) -> None:
        self.clear()

        self.drawTileBorder = True
        self.tileSize = START_TILE_SIZE

        self.offsetX = 0
        self.offsetY = 0


    def clear(self):
        self.tiles = []
        for _ in range(NB_H_TILE):
            self.tiles.append([0] * NB_W_TILE)


    def moveOffset(self, dir: str):
        if dir == 'u':
            self.offsetY -= 1
        elif dir == 'd':
            self.offsetY += 1
        elif dir == 'l':
            self.offsetX -= 1
        elif dir == 'r':
            self.offsetX += 1

        self.offsetX %= NB_W_TILE
        self.offsetY %= NB_H_TILE


    def zoomIn(self):
        self.tileSize = max(MIN_TILE_SIZE, self.tileSize - 5)


    def zoomOut(self):
        self.tileSize = min(MAX_TILE_SIZE, self.tileSize + 5)


    def switchDrawTileBorder(self):
        self.drawTileBorder = not self.drawTileBorder


    def handleMouseClick(self, mousePos: tuple[int], value: int):
        tileX = (mousePos[0] // self.tileSize) + self.offsetX
        tileY = (mousePos[1] // self.tileSize) + self.offsetY
        self.set(tileX, tileY, value)


    def set(self, x: int, y: int, value: int):
        x %= NB_W_TILE
        y %= NB_H_TILE

        self.tiles[y][x] = value


    def get(self, x: int, y: int) -> int:
        x %= NB_W_TILE
        y %= NB_H_TILE

        return self.tiles[y][x]


    def draw(self, win: pg.Surface):
        colors = [TILE_EMPTY_COLOR, TILE_FILL_COLOR]

        for y in range(NB_H_TILE):
            drawY = y * self.tileSize
            drawRY = (y + 1) * self.tileSize
            for x in range(NB_W_TILE):
                drawX = x * self.tileSize
                if drawX > WIN_W:
                    break

                drawRX = (x + 1) * self.tileSize
                drawRect = (drawX, drawY, self.tileSize, self.tileSize)

                tileStatus = self.get(x + self.offsetX, y + self.offsetY)

                pg.draw.rect(win, colors[tileStatus], drawRect)
                if self.drawTileBorder:
                    tileStatus = not tileStatus
                    pg.draw.line(win, colors[tileStatus], (drawX, drawY), (drawRX, drawY))
                    pg.draw.line(win, colors[tileStatus], (drawX, drawY), (drawX, drawRY))

            if drawY > WIN_H:
                break
