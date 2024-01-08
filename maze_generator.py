from cell import Cell
from methods import remove_walls

def generate_maze(screen, tile, cols, rows):
  grid_cells = [Cell(col, row, screen, tile, cols, rows) for row in range(rows) for col in range(cols)]
  current_cell = grid_cells[0]
  stack = []
  break_count = 1
  while break_count != len(grid_cells):
    current_cell.visited = True
    next_cell = current_cell.check_neighbors(grid_cells)

    if next_cell:
      next_cell.visited = True
      break_count += 1
      stack.append(current_cell)
      remove_walls(current_cell, next_cell)
      current_cell = next_cell
    elif stack:
      current_cell = stack.pop()
  return grid_cells