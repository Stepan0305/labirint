import pygame
from random import choice

class Cell:
  def __init__(self, x, y, screen=None, tile=None, cols=0, rows=0):
    self.x, self.y, self.screen, self.tile, self.cols, self.rows = x, y, screen, tile, cols, rows
    self.walls = { 'top': True, 'right': True, 'bottom': True, 'left': True }
    self.visited = False

  def draw(self):
    screen, tile = self.screen, self.tile
    x, y = self.x * tile, self.y * tile

    if self.walls['top']:
      pygame.draw.line(screen, pygame.Color('blue'), (x, y), (x + tile, y), 2)
    if self.walls['right']:
      pygame.draw.line(screen, pygame.Color('blue'), (x + tile, y), (x + tile, y + tile), 2)
    if self.walls['bottom']:
      pygame.draw.line(screen, pygame.Color('blue'), (x, y + tile), (x + tile, y + tile), 2)
    if self.walls['left']:
      pygame.draw.line(screen, pygame.Color('blue'), (x, y), (x, y + tile), 2)

  def get_rects(self):
      rects = []
      x, y = self.x * self.tile, self.y * self.tile
      if self.walls['top']:
          rects.append(pygame.Rect( (x, y), (self.tile, 3) ))
      if self.walls['right']:
          rects.append(pygame.Rect( (x + self.tile, y), (3, self.tile) ))
      if self.walls['bottom']:
          rects.append(pygame.Rect( (x, y + self.tile), (self.tile , 3) ))
      if self.walls['left']:
          rects.append(pygame.Rect( (x, y), (3, self.tile) ))
      return rects
    
  def check_cell(self, cells):
    cols, rows = self.cols, self.rows
    find_index = lambda x, y: x + y * cols
    if self.x < 0 or self.x > cols - 1 or self.y < 0 or self.y > rows - 1:
      return False
    return cells[find_index(self.x, self.y)]
  
  def check_neighbors(self, cells):
    neighbors = []
    top = Cell(self.x, self.y - 1, cols=self.cols, rows=self.rows).check_cell(cells)
    right = Cell(self.x + 1, self.y, cols=self.cols, rows=self.rows).check_cell(cells)
    bottom = Cell(self.x, self.y + 1, cols=self.cols, rows=self.rows).check_cell(cells)
    left = Cell(self.x - 1, self.y, cols=self.cols, rows=self.rows).check_cell(cells)
    if top and not top.visited:
      neighbors.append(top)
    if right and not right.visited:
      neighbors.append(right)
    if bottom and not bottom.visited:
      neighbors.append(bottom)
    if left and not left.visited:
      neighbors.append(left)
    return choice(neighbors) if neighbors else False