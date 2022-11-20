import pygame as pg
from settings1 import *
from collections import deque
import os

class SpriteObject:
    def __init__(self, game, path = 'resources/sprites/static_sprites/candlebra.png', 
                 pos = (10.5, 3.5), scale = 1.0, shift = 0.0):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_height() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        #에러 회피
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        #구조물 크기, 높이
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift 
        
    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        
        image = pg.transform.scale(self.image, (proj_width, proj_height))
        
        self.sprite_half_width = proj_width // 2 #구조물 중간 위치
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift #화면 밖으로 나가지 않는 위치
        
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))
    
    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
         
        #플레이어가 구조물을 바라보는 각 계산
        self.theta = math.atan2(dy, dx) # atan2 : 인수가 2개인 역탄젠트   ***
        
        #플레이어 앵글
        #세타와 플레이어 방향각의 차이  
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or ( dx < 0 and dy < 0):
            delta += math.tau #tau = 2pi
            
        #광선이 몇개 필요한지
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        
        #구조물 크기 결정을 위한 거리계산
        self.dist = math.hypot(dx, dy) #직각삼각형 빗면 계산
        self.norm_dist = self.dist * math.cos(delta)
        
        #게임 성능 향상
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()
    
    def update(self):   
        self.get_sprite()
        
class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger: #트리거가 트루이면 큐가 돌면서 애니매이션 출력
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque() #양뱡향 큐
        for file_name in os.listdir(path): #파일에 있는 이미지 큐에 다운로드
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
