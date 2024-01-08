from cell import Cell
import pygame

def remove_walls(current: Cell, next: Cell):
  dx = current.x - next.x
  if dx == 1:
    current.walls['left'] = False
    next.walls['right'] = False
  elif dx == -1:
    current.walls['right'] = False
    next.walls['left'] = False
  dy = current.y - next.y
  if dy == 1:
    current.walls['top'] = False
    next.walls['bottom'] = False
  elif dy == -1:
    current.walls['bottom'] = False
    next.walls['top'] = False

def already_exists(current: Cell, cells: list):
  if next(cell for cell in cells if cell.x == current.x and cell.y == current.y):
    return True
  return False

def get_font(size):
    return pygame.font.Font("font.ttf", size)
