import os
import sys
import pygame
from sys import exit
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 350

TRACK_WIDTH = WINDOW_WIDTH
TRACK_HEIGHT = 15
TRACK_X = 0
TRACK_Y = WINDOW_HEIGHT - TRACK_HEIGHT

CLOUD_WIDTH = 84
CLOUD_HEIGHT = 101

BIRD1_WIDTH = 97
BIRD1_HEIGHT = 68

DINO_WIDHT = 88
DINO_HEIGHT = 94
DINO_X = 50
DINO_Y = WINDOW_HEIGHT - DINO_HEIGHT - TRACK_HEIGHT

BIG_CACTUS_WIDTH = 100
BIG_CACTUS_HEIGHT = 75
CACTUS_HEIGHT = 70
CACTUS1_WIDTH = 34
CACTUS2_WIDTH = 69
CACTUS3_WIDTH = 102

GAME_OVER_WIDTH = 386
GAME_OVER_HEIGHT = 40
RESTART_WIDTH = 76
RESTART_HEIGHT = 68

CACTUS_VELOCITY_X = -9
ELEMENT_VELOCITY_X = -5
DINO_VELOCITY_Y = -10
GRAVITY = 0.4

#IMPORTING IMAGES
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

def load_image(image_name,scale=None) :
    full_path = resource_path(image_name)
    image = pygame.image.load(full_path) 
    if scale is not None :
        image = pygame.transform.scale(image,scale) 
    return image

track_image = load_image("dino-assets/track.png",(TRACK_WIDTH,TRACK_HEIGHT))
cloud_image = load_image("dino-assets/cloud.png",(CLOUD_WIDTH,CLOUD_HEIGHT))
bird1_image = load_image("dino-assets/bird1.png",(BIRD1_WIDTH,BIRD1_HEIGHT))
bird2_image = load_image("dino-assets/bird2.png",(BIRD1_WIDTH,BIRD1_HEIGHT))
elements_images = [cloud_image,bird1_image]
bird_fly_images = [bird1_image,bird2_image]
dino_image = load_image("dino-assets/dino.png",(DINO_WIDHT,DINO_HEIGHT))
dino_jump_image = load_image("dino-assets/dino-run1.png",(DINO_WIDHT,DINO_HEIGHT))
dino_run1_image = load_image("dino-assets/dino-run1.png",(DINO_WIDHT,DINO_HEIGHT))
dino_run2_image = load_image("dino-assets/dino-run2.png",(DINO_WIDHT,DINO_HEIGHT))
dino_run_images = [dino_run1_image,dino_run2_image]
dino_dead_image = load_image("dino-assets/dino-dead.png",(DINO_WIDHT,DINO_HEIGHT))
big_cactus3_image = load_image("dino-assets/big-cactus3.png",(BIG_CACTUS_WIDTH,BIG_CACTUS_HEIGHT))
cactus1_image = load_image("dino-assets/cactus1.png",(CACTUS1_WIDTH,CACTUS_HEIGHT))
cactus2_image = load_image("dino-assets/cactus2.png",(CACTUS2_WIDTH,CACTUS_HEIGHT))
cactus3_image = load_image("dino-assets/cactus3.png",(CACTUS3_WIDTH,CACTUS_HEIGHT))
cactus_images = [cactus1_image,cactus2_image,cactus3_image,big_cactus3_image]
game_over_image = load_image("dino-assets/game-over.png",(GAME_OVER_WIDTH,GAME_OVER_HEIGHT))
restart_image = load_image("dino-assets/reset.png",(RESTART_WIDTH,RESTART_HEIGHT))

class Block(pygame.Rect) :
   def __init__(self,coordinates,size,img):
      pygame.Rect.__init__(self,coordinates,size)
      self.img = img
      self.current_walk_index = 0
      self.velocity_x = 0
      self.velocity_y = 0

   def dino_animation(self) :
      if self.velocity_x == 0 and self.y + self.height == WINDOW_HEIGHT - TRACK_HEIGHT :
         self.current_walk_index = (self.current_walk_index + 1) % len(dino_run_images)
         self.img = dino_run_images[self.current_walk_index]

   def bird_animation(self) :
      if len(elements_list) != 0 :
            if (self.img in bird_fly_images) and self.x < WINDOW_WIDTH and self.x + self.width > 0 :
               self.current_walk_index = (self.current_walk_index + 1) % len(bird_fly_images)
               self.img = bird_fly_images[self.current_walk_index]

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("DINOSAUR GAME")
pygame.display.set_icon(dino_image)
clock = pygame.time.Clock()

create_cactus_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_cactus_timer,1000) #FOR EVERY 1 SEC
create_elements_timer = pygame.USEREVENT + 1
pygame.time.set_timer(create_elements_timer,7000) #FOR EVERY 7 SEC
animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(animation_timer,250) #FOR EVERY 0.25 SEC

dino = Block((DINO_X,DINO_Y),(DINO_WIDHT,DINO_HEIGHT),dino_image)
cactus_list = []
elements_list = []
score = 0
game_over = False

def create_cactus() :
   random_cactus_image = random.choice(cactus_images)
   random_cactus = Block((WINDOW_WIDTH,WINDOW_HEIGHT - random_cactus_image.height - TRACK_HEIGHT),random_cactus_image.get_size(),random_cactus_image)
   random_cactus.velocity_x = CACTUS_VELOCITY_X
   cactus_list.append(random_cactus)

def create_element() :
   random_element_image = random.choice(elements_images)
   random_element = Block((WINDOW_WIDTH,25),random_element_image.get_size(),random_element_image)
   random_element.velocity_x = ELEMENT_VELOCITY_X
   elements_list.append(random_element)

def dino_image_update() :
   if dino.img == dino_jump_image and dino.y + dino.height == WINDOW_HEIGHT - TRACK_HEIGHT :
      dino.img = dino_image

def move() :
   global score,cactus_list,game_over,elements_list

   score += 1

   dino.velocity_y += GRAVITY
   dino.y += dino.velocity_y
   if dino.y + dino.height >= WINDOW_HEIGHT - TRACK_HEIGHT :
      dino.y = WINDOW_HEIGHT - TRACK_HEIGHT - DINO_HEIGHT

   for cactus in cactus_list :
        cactus.x += cactus.velocity_x
        if dino.colliderect(cactus) and not game_over :
           game_over = True
           dino.img = dino_dead_image
   cactus_list = [cactus for cactus in cactus_list if cactus.x + cactus.width > 0]

   for element in elements_list :
           element.x += element.velocity_x
   elements_list = [element for element in elements_list if element.x + element.width > 0]

def draw() :
    window.fill("grey")
    window.blit(track_image,(TRACK_X,TRACK_Y))
    window.blit(dino.img,dino)

    for cactus in cactus_list :
       window.blit(cactus.img,cactus)

    for element in elements_list :
       window.blit(element.img,element)

    text_font = pygame.font.SysFont("courier",20)
    text_render = text_font.render("00000" + str(score),True,"black")
    window.blit(text_render,(670,0))

    if game_over :
       window.blit(game_over_image,(WINDOW_WIDTH/4,WINDOW_HEIGHT/4))
       window.blit(restart_image,(WINDOW_WIDTH/2 - 50,WINDOW_HEIGHT/2 - 25))

while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN :
           if event.key == pygame.K_SPACE :
              if game_over :
                cactus_list.clear()
                elements_list.clear()
                dino.y = DINO_Y
                score = 0
                dino.img = dino_image
                game_over = False
                dino.velocity_y = 0
 
              if dino.y + dino.height >= WINDOW_HEIGHT - TRACK_HEIGHT :
                dino.velocity_y = DINO_VELOCITY_Y
                dino.img = dino_jump_image

        if event.type == create_cactus_timer and not game_over :
           create_cactus()

        if event.type == create_elements_timer and not game_over :
           create_element()

        if event.type == animation_timer and not game_over :
           dino.dino_animation()
           if len(elements_list) != 0 :
               elements_list[0].bird_animation()
           
    if not game_over :
        move()
        dino_image_update()
        draw()
        pygame.display.update()
        clock.tick(60) #60FPS