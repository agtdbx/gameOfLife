import pygame as pg
import random

from define import  NB_W_TILE, NB_H_TILE,\
                    MIN_TILE_SIZE, START_TILE_SIZE, MAX_TILE_SIZE, ZOOM_SPEED,\
                    TILE_FILL_COLOR, TILE_EMPTY_COLOR, CAMERA_SPEED,\
                    WIN_W, WIN_H

class    Grid:
    def __init__(self) -> None:

        self.drawTileBorder = True
        self.tileSize = MIN_TILE_SIZE
        # self.tileSize = START_TILE_SIZE

        self.surfaceW = NB_W_TILE * MIN_TILE_SIZE
        self.surfaceH = NB_H_TILE * MIN_TILE_SIZE
        self.surfaceTL = pg.Surface((self.surfaceW,self.surfaceH))
        self.surfaceBL = pg.Surface((self.surfaceW,self.surfaceH))
        self.surfaceTR = pg.Surface((self.surfaceW,self.surfaceH))
        self.surfaceBR = pg.Surface((self.surfaceW,self.surfaceH))

        self.drawGridW = self.tileSize * NB_W_TILE
        self.drawGridH = self.tileSize * NB_H_TILE

        self.cameraX = 0
        self.cameraY = 0
        self.colors = [TILE_EMPTY_COLOR, TILE_FILL_COLOR]

        self.clear()


    def clear(self):
        self.tiles = []
        for _ in range(NB_H_TILE):
            self.tiles.append([0] * NB_W_TILE)
        self.computeSurface()


    def addRandomTile(self):
        tileX = random.randint(0, NB_W_TILE - 1)
        tileY = random.randint(0, NB_H_TILE - 1)
        self.tiles[tileY][tileX] = 1
        self.computeTileChange(tileX, tileY, 1)


    def moveCamera(self, dir: str, delta: float):
        if dir == 'u':
            self.cameraY += CAMERA_SPEED * delta
        elif dir == 'd':
            self.cameraY -= CAMERA_SPEED * delta
        elif dir == 'l':
            self.cameraX += CAMERA_SPEED * delta
        elif dir == 'r':
            self.cameraX -= CAMERA_SPEED * delta

        self.cameraX %= self.surfaceW
        self.cameraY %= self.surfaceH


    def zoomIn(self):
        self.tileSize = max(MIN_TILE_SIZE, self.tileSize - ZOOM_SPEED)
        self.drawGridW = self.tileSize * NB_W_TILE
        self.drawGridH = self.tileSize * NB_H_TILE
        self.computeSurface()


    def zoomOut(self):
        self.tileSize = min(MAX_TILE_SIZE, self.tileSize + ZOOM_SPEED)
        self.drawGridW = self.tileSize * NB_W_TILE
        self.drawGridH = self.tileSize * NB_H_TILE
        self.computeSurface()


    def switchDrawTileBorder(self):
        self.drawTileBorder = not self.drawTileBorder
        self.computeSurface()


    def handleMouseClick(self, mousePos: tuple[int], value: int):
        tileX = (mousePos[0] - int(self.cameraX)) // self.tileSize
        tileY = (mousePos[1] - int(self.cameraY)) // self.tileSize
        self.set(tileX, tileY, value)


    def set(self, x: int, y: int, value: int):
        x %= NB_W_TILE
        y %= NB_H_TILE

        self.tiles[y][x] = value
        self.computeTileChange(x, y, value)


    def get(self, x: int, y: int) -> int:
        x %= NB_W_TILE
        y %= NB_H_TILE

        return self.tiles[y][x]


    def draw(self, win: pg.Surface):
        # Draw top left
        drawX = self.cameraX - self.surfaceW - 1
        drawY = self.cameraY - self.surfaceH - 1
        win.blit(self.surfaceTL, (drawX, drawY))

        # Draw bottom left
        drawX = self.cameraX - self.surfaceW - 1
        drawY = self.cameraY
        win.blit(self.surfaceBL, (drawX, drawY))

        # Draw top right
        drawX = self.cameraX
        drawY = self.cameraY - self.surfaceH - 1
        win.blit(self.surfaceTR, (drawX, drawY))

        # Draw bottom right
        drawX = self.cameraX
        drawY = self.cameraY
        win.blit(self.surfaceBR, (drawX, drawY))


    def computeSurface(self):
        offsetX = self.drawGridW - self.surfaceW
        offsetY = self.drawGridH - self.surfaceH
        for y in range(NB_H_TILE):
            # For BR surface
            BRdrawY = y * self.tileSize
            BRdrawRY = (y + 1) * self.tileSize

            # For TR surface
            TRdrawY = BRdrawY - offsetY
            TRdrawRY = BRdrawRY - offsetY

            # For BL surface
            BLdrawY = BRdrawY
            BLdrawRY = BRdrawRY

            # For TL surface
            TLdrawY = BRdrawY - offsetY
            TLdrawRY = BRdrawRY - offsetY

            for x in range(NB_W_TILE):
                tileStatus = self.get(x, y)

                # For BR surface
                BRdrawX = x * self.tileSize
                BRdrawRX = (x + 1) * self.tileSize

                # For TR surface
                TRdrawX = BRdrawX
                TRdrawRX = BRdrawRX

                # For TL surface
                TLdrawX = BRdrawX - offsetX
                TLdrawRX = BRdrawRX - offsetX

                # For BL surface
                BLdrawX = BRdrawX - offsetX
                BLdrawRX = BRdrawRX - offsetX

                if TLdrawX < WIN_W or TLdrawY < WIN_H or TLdrawRX >= 0 or TLdrawRY >= 0:
                    self.computeTile(self.surfaceTL, TLdrawX, TLdrawY, TLdrawRX, TLdrawRY, tileStatus)
                if BLdrawX < WIN_W or BLdrawY < WIN_H or BLdrawRX >= 0 or BLdrawRY >= 0:
                    self.computeTile(self.surfaceBL, BLdrawX, BLdrawY, BLdrawRX, BLdrawRY, tileStatus)
                if TRdrawX < WIN_W or TRdrawY < WIN_H or TRdrawRX >= 0 or TRdrawRY >= 0:
                    self.computeTile(self.surfaceTR, TRdrawX, TRdrawY, TRdrawRX, TRdrawRY, tileStatus)
                if BRdrawX < WIN_W or BRdrawY < WIN_H or BRdrawRX >= 0 or BRdrawRY >= 0:
                    self.computeTile(self.surfaceBR, BRdrawX, BRdrawY, BRdrawRX, BRdrawRY, tileStatus)


    def computeTile(self, surface: pg.Surface, drawX: int, drawY: int, drawRX: int, drawRY: int, tileStatus: int):
        drawRect = (drawX, drawY, self.tileSize, self.tileSize)
        pg.draw.rect(surface, self.colors[tileStatus], drawRect)
        if self.drawTileBorder:
            tileStatus = not tileStatus
            pg.draw.line(surface, self.colors[tileStatus], (drawX, drawY), (drawRX, drawY))
            pg.draw.line(surface, self.colors[tileStatus], (drawX, drawY), (drawX, drawRY))


    def computeTileChange(self, x: int, y: int, value: int):
        offsetX = self.drawGridW - self.surfaceW
        offsetY = self.drawGridH - self.surfaceH

        # BR surface
        BRdrawX = x * self.tileSize
        BRdrawRX = (x + 1) * self.tileSize
        BRdrawY = y * self.tileSize
        BRdrawRY = (y + 1) * self.tileSize

        # TR surface
        TRdrawX = BRdrawX
        TRdrawRX = BRdrawRX
        TRdrawY = BRdrawY - offsetY
        TRdrawRY = BRdrawRY - offsetY

        # BL surface
        BLdrawX = BRdrawX - offsetX
        BLdrawRX = BRdrawRX - offsetX
        BLdrawY = BRdrawY
        BLdrawRY = BRdrawRY

        # TL surface
        TLdrawX = BRdrawX - offsetX
        TLdrawRX = BRdrawRX - offsetX
        TLdrawY = BRdrawY - offsetY
        TLdrawRY = BRdrawRY - offsetY

        if TLdrawX < WIN_W or TLdrawY < WIN_H or TLdrawRX >= 0 or TLdrawRY >= 0:
            self.computeTile(self.surfaceTL, TLdrawX, TLdrawY, TLdrawRX, TLdrawRY, value)
        if BLdrawX < WIN_W or BLdrawY < WIN_H or BLdrawRX >= 0 or BLdrawRY >= 0:
            self.computeTile(self.surfaceBL, BLdrawX, BLdrawY, BLdrawRX, BLdrawRY, value)
        if TRdrawX < WIN_W or TRdrawY < WIN_H or TRdrawRX >= 0 or TRdrawRY >= 0:
            self.computeTile(self.surfaceTR, TRdrawX, TRdrawY, TRdrawRX, TRdrawRY, value)
        if BRdrawX < WIN_W or BRdrawY < WIN_H or BRdrawRX >= 0 or BRdrawRY >= 0:
            self.computeTile(self.surfaceBR, BRdrawX, BRdrawY, BRdrawRX, BRdrawRY, value)


    def simulateStep(self):
        changes = []

        # Detect changes
        for y in range(NB_H_TILE):
            pY = (y - 1) % NB_H_TILE # previous y
            nY = (y + 1) % NB_H_TILE # next y

            for x in range(NB_W_TILE):
                pX = (x - 1) % NB_W_TILE # previous x
                nX = (x + 1) % NB_W_TILE # next x

                # Get number of tile fill in neighborhood
                neighborsValue = 0
                neighborsValue += self.tiles[pY][pX]
                neighborsValue += self.tiles[pY][x]
                neighborsValue += self.tiles[pY][nX]
                neighborsValue += self.tiles[y][pX]
                neighborsValue += self.tiles[y][nX]
                neighborsValue += self.tiles[nY][pX]
                neighborsValue += self.tiles[nY][x]
                neighborsValue += self.tiles[nY][nX]

                tileStatus = self.tiles[y][x]

                # If an empty tile is have 3 fill tile around, make it fill
                if tileStatus == 0 and neighborsValue == 3:
                    changes.append((x, y, 1)) # add the change

                # If an fill tile is haven't 2 or 3 fill tile around, make it empty
                if tileStatus == 1 and neighborsValue != 2 and neighborsValue != 3:
                    changes.append((x, y, 0)) # add the change

        # Apply changes
        for x, y, value in changes:
            self.tiles[y][x] = value
            self.computeTileChange(x, y, value)
