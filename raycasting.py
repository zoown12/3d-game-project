import pygame
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        
    def ray_cast(self) :
        ox, oy = self.game.player.pos #맵에서 플레이어 위치
        x_map, y_map = self.game.player.map_pos #멥에서 플레이어가 있는 타일의 위치
        
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001 # 0을 나누기 오류 회피
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            #가로
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth
                 
            #세로
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1) #방향 벡터
            depth_vert = (x_vert - ox) / cos_a #벡터 크기
            y_vert = oy + depth_vert * sin_a
            
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            
            for i in range(MAX_DEPTH): #광선 발사
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map: #광선이 벽에 부딪히면 종료
                    break
                #아니면 광선을 더 멀리 발사
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            #거리
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor
                
            #remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)
                
            #projection
            proj_height= SCREEN_DIST/ (depth+0.0001)


            #draw wall
            color=[255/(1+depth ** 5 * 0.00002)] *3
            pygame.draw.rect(self.game.screen,color,
                        (ray*SCALE,HALF_HEIGHT-proj_height //2,SCALE,proj_height))
                
            #디버깅
           # pygame.draw.line(self.game.screen, 'yellow', (100*ox,100*oy),(100*ox+100*depth*cos_a, 100*oy+100*depth*sin_a),2)
            
            ray_angle += DELTA_ANGLE
    
    def update(self):
        self.ray_cast()
