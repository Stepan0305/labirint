import pygame
from button import Button
from methods import get_font
from random import randrange
from maze_generator import generate_maze

pygame.init()
RES = WIDTH, HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode(RES)
FPS = 30
TILES = [150, 90, 50]
CURRENT_TILE = 1


def main_menu():
   clock = pygame.time.Clock()
   while True:
      SCREEN.fill(pygame.Color(70, 50, 170))
      mouse_pos = pygame.mouse.get_pos()
      play_text = get_font(45).render("ДОБРО ПОЖАЛОВАТЬ!", True, "White")
      play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
      SCREEN.blit(play_text, play_rect)

      play_btn = Button(image=pygame.image.load("play_rect.png"), pos=(WIDTH // 2, HEIGHT // 2), 
                              text_input="ИГРАТЬ!", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
      play_btn.changeColor(mouse_pos)
      play_btn.update(SCREEN)

      options_btn = Button(image=pygame.image.load("play_rect.png"), pos=(WIDTH // 2, HEIGHT // 4 * 3), 
                              text_input="НАСТРОЙКИ!", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
      options_btn.changeColor(mouse_pos)
      options_btn.update(SCREEN)

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if play_btn.checkForInput(mouse_pos):
               play_game()
            if options_btn.checkForInput(mouse_pos):
               settings()
      
      pygame.display.flip()
      clock.tick(FPS)

def congrats():
   clock = pygame.time.Clock()
   while True:
      SCREEN.fill(pygame.Color(70, 50, 170))
      mouse_pos = pygame.mouse.get_pos()
      play_text = get_font(45).render("МОЛОДЧИНА! RESPECT!", True, "White")
      play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
      image = pygame.image.load("cup.png")
      image = pygame.transform.scale(image, (WIDTH // 8, WIDTH // 8))
      image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
      menu_btn = Button(image=pygame.image.load("play_rect.png"), pos=(WIDTH // 2, HEIGHT // 4 * 3), 
                           text_input="МЕНЮ", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
      menu_btn.changeColor(mouse_pos)
      menu_btn.update(SCREEN)

      SCREEN.blit(play_text, play_rect)
      SCREEN.blit(image, image_rect)
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_btn.checkForInput(mouse_pos):
               main_menu()

      pygame.display.flip()
      clock.tick(FPS)

def settings():
   global CURRENT_TILE
   clock = pygame.time.Clock()
   def get_level_text():
      text = ""
      if CURRENT_TILE == 0:
         text = "Простой"
      elif CURRENT_TILE == 1:
         text = "Средний" 
      elif CURRENT_TILE == 2:
         text = "Сложный"
      return get_font(45).render(text, True, "White")
   
   def get_arrow_buttons():
      left = Button(image=None, pos=(WIDTH // 3, HEIGHT // 2), 
                           text_input="<-", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
      right = Button(image=None, pos=(WIDTH // 3 * 2, HEIGHT // 2), 
                           text_input="->", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
      if CURRENT_TILE == 0:
         return None, right
      elif CURRENT_TILE == 1:
         return left, right
      elif CURRENT_TILE == 2:
         return left, None

   while True:
      SCREEN.fill(pygame.Color(70, 50, 170))
      mouse_pos = pygame.mouse.get_pos()
      level_text = get_font(45).render("Выберите уровень сложности", True, "White")
      level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
      current_level_text = get_level_text()
      current_level_rect = current_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

      left, right = get_arrow_buttons()
      if left:
         left.changeColor(mouse_pos)
         left.update(SCREEN)
      if right:
         right.changeColor(mouse_pos)
         right.update(SCREEN)
      ok_btn = Button(image=pygame.image.load("play_rect.png"), pos=(WIDTH // 2, HEIGHT // 4 * 3), 
                           text_input="OK", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
      ok_btn.changeColor(mouse_pos)
      ok_btn.update(SCREEN)
      SCREEN.blit(level_text, level_rect)
      SCREEN.blit(current_level_text, current_level_rect)

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if left and left.checkForInput(mouse_pos):
               if CURRENT_TILE > 0:
                  CURRENT_TILE -= 1
            if right and right.checkForInput(mouse_pos):
               if CURRENT_TILE < 2:
                  CURRENT_TILE += 1
            if ok_btn.checkForInput(mouse_pos):
               main_menu()

      pygame.display.flip()
      clock.tick(FPS)

def play_game():
   REC_SIZE = TILES[CURRENT_TILE] - 8
   cols, rows = WIDTH // TILES[CURRENT_TILE], HEIGHT // TILES[CURRENT_TILE]
   clock = pygame.time.Clock()
   rolls = pygame.image.load('rolls.png').convert_alpha()
   rolls = pygame.transform.scale(rolls, (REC_SIZE, REC_SIZE))
   rolls_rect = rolls.get_rect()
   rolls_rect.x = randrange(cols) * TILES[CURRENT_TILE] + (TILES[CURRENT_TILE] - REC_SIZE) / 2
   rolls_rect.y = randrange(rows) * TILES[CURRENT_TILE] + (TILES[CURRENT_TILE] - REC_SIZE) / 2
   player = pygame.Rect((TILES[CURRENT_TILE] - REC_SIZE) / 2, (TILES[CURRENT_TILE] - REC_SIZE) / 2, REC_SIZE, REC_SIZE)
   maze = generate_maze(SCREEN, TILES[CURRENT_TILE], cols, rows)
   walls_collide_list = sum([cell.get_rects() for cell in maze], [])

   def is_collide(x, y):
      tmp_rect = player.move(x // 2, y // 2)
      if tmp_rect.collidelist(walls_collide_list) == -1:
            return False
      return True

   def is_finish():
      return player.colliderect(rolls_rect)

   def move_player(key):
      direction = (0, 0)
      if key == pygame.K_LEFT or key == pygame.K_a:
         direction = (-TILES[CURRENT_TILE], 0)
      elif key == pygame.K_RIGHT or key == pygame.K_d:
         direction = (TILES[CURRENT_TILE], 0)
      elif key == pygame.K_UP or key == pygame.K_w:
         direction = (0, -TILES[CURRENT_TILE])
      elif key == pygame.K_DOWN or key == pygame.K_s:
         direction = (0, TILES[CURRENT_TILE])
      if not is_collide(*direction):
         player.move_ip(direction)

   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            exit()
         elif event.type == pygame.KEYDOWN:
            move_player(event.key)

      SCREEN.fill(pygame.Color(30, 20, 70))
      pygame.draw.rect(SCREEN, pygame.Color(0, 0, 255), player)
      SCREEN.blit(rolls, rolls_rect)

      [cell.draw() for cell in maze]
      move_player(pygame.key.get_pressed())

      if is_finish():
         congrats()

      pygame.display.flip()
      clock.tick(FPS)
main_menu()