import pygame
import sys
import random 

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("IRONMAN GO!")
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/fontscore.ttf',45)

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

tower_surface = pygame.transform.scale2x(pygame.image.load('assets/towert1.png'))
tower_list = []
SPAWNTOWER = pygame.USEREVENT
pygame.time.set_timer(SPAWNTOWER,1200)
tower_height = [400,500,600,650]


def create_tower():
      random_tower_pos = random.choice(tower_height)
      random_tower = random.choice(tower_height)
      bottom_tower = tower_surface.get_rect(midtop = (1000,random_tower_pos))
      top_tower = tower_surface.get_rect(midbottom = (1000,random_tower_pos - 350))
      return bottom_tower,top_tower

def move_towers(towers):
      for tower in towers:
            tower.centerx -= 6
      return towers

def draw_towers(towers):
      for tower in towers:
            if tower.bottom >= 600:
                  screen.blit(tower_surface,tower)
            else:
                  flip_tower = pygame.transform.flip(tower_surface,False,True)
                  screen.blit(flip_tower,tower)

def check_collision(towers):
      for tower in towers:
            if iron_rect.colliderect(tower):
                  death_sound.play()
                  return False

      if iron_rect.top <= -100 or iron_rect.bottom >= 600:
            return False

      return True


def score_display(game_state):
      if game_state == 'main_game':
            score_surface = game_font.render(str(int(score)),True,(black))
            score_rect = score_surface.get_rect(center = (100,80))
            screen.blit(score_surface,score_rect)
      if game_state == 'game_over':
            score_surface = game_font.render(f'SCORE: {int(score)}' ,True,(black))
            score_rect = score_surface.get_rect(center = (150,50))
            screen.blit(score_surface,score_rect)

            high_score_surface = game_font.render(f'HIGH SCORE: {int(high_score)}',True,(black))
            high_score_rect = high_score_surface.get_rect(center = (800,50))
            screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
      if score > high_score:
            high_score = score
      return high_score


# Game Variables
gravity = 0.25
iron_movement = 0
game_active = True
score = -1
high_score = 0


bg_surface1 = pygame.image.load('assets/bgg3.jpg').convert()


iron_surface = pygame.image.load('assets/ronny1.png')
iron_rect = iron_surface.get_rect(center = (270,300))

message = pygame.image.load('assets/message2.png').convert()



game_over_surface = pygame.image.load('assets/message2.png')
game_over_rect = game_over_surface.get_rect(center = (500,320))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

stone = pygame.image.load('assets/stone.png')
thing_starty = random.randrange(50,550)
thing_startx = 250

def thing(x,y):
    screen.blit(stone,(thing_startx,thing_starty))


while True:
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()

            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_SPACE and game_active:
                        iron_movement = 0
                        iron_movement -= 5
                        flap_sound.play()

                  if event.key == pygame.K_SPACE and game_active == False:
                        game_active = True
                        tower_list.clear()
                        iron_rect.center = (270,300)
                        iron_movement = 0
                        score = -1

            if event.type == SPAWNTOWER:
                  tower_list.extend(create_tower())

      screen.blit(bg_surface1,(0,0))
      
      
        


      if game_active:
            # ironman
            iron_movement += gravity
            iron_rect.centery += iron_movement
            screen.blit(iron_surface,iron_rect)
            thing(thing_startx,thing_starty)
            game_active = check_collision(tower_list)

            # tower
            tower_list = move_towers(tower_list)
            draw_towers(tower_list)


            score_display('main_game')
            score_sound_countdown -= 1
            if score_sound_countdown <= 1:
                  score_sound.play()
                  score_sound_countdown = 100
                  score += 1
                  
            if iron_rect.centery >= (thing_starty-25) and iron_rect.centery <= (thing_starty+25):
                  score += 10
                  thing_starty = random.randrange(50,550)
                
      else:
            screen.blit(game_over_surface,game_over_rect)
            high_score = update_score(score,high_score)
            score_display('game_over')

      pygame.display.update()
      clock.tick(80)
      
