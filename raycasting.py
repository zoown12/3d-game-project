import pygame
import math
from settings1 import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result=[]
        self.objects_to_render=[]
        self.textures=self.game.object_renderer.wall_textures
        
        
    def get_objects_to_render(self):
        self.objects_to_render=[]
        for ray,values in enumerate(self.ray_casting_result):
            depth,proj_height,texture,offset=values

            #벽의 프로젝션 높이가 화면의 해상도를 초과하는 특수한 경우
            if proj_height<HEIGHT: 
                wall_column=self.textures[texture].subsurface(
                    offset*(TEXTURE_SIZE - SCALE),0,SCALE,TEXTURE_SIZE
                    )
                wall_column=pygame.transform.scale(wall_column,(SCALE,proj_height))
                wall_pos =(ray*SCALE,HALF_HEIGHT-proj_height//2)
            else:
                texture_height=TEXTURE_SIZE * HEIGHT / proj_height
                wall_column=self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE-SCALE),HALF_TEXTURE_SIZE-texture_height//2,
                    SCALE,texture_height
                )
                wall_column =pygame.transform.scale(wall_column,(SCALE,HEIGHT))
                wall_pos=(ray *SCALE,0)
            #frame 드랍 방지 
            #벽에 접근할 때 광선의 깊이가 0이 되는 경향
            #텍스처가 이 성능 저하를 제거하기 위해 매우 큰 값으로 높이를 확장하기 시작한다.
            #벽의 프로젝션 높이를 화면의 해상도랑 맞쳐줘야댐

            self.objects_to_render.append((depth,wall_column,wall_pos))
        
        
    def ray_cast(self) :
        self.ray_casting_result = []
        ox, oy = self.game.player.pos #맵에서 플레이어 위치
        x_map, y_map = self.game.player.map_pos #멥에서 플레이어가 있는 타일의 위치
        texture_vert, texture_hor = 1, 1
        
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
                    texture_hor = self.game.map.world_map[tile_hor]
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
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                #아니면 광선을 더 멀리 발사
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            #거리
            #depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1-y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if  sin_a > 0 else x_hor
                
                
            #렌즈 효과 제거
            depth *= math.cos(self.game.player.angle - ray_angle)
                
            #projection
            proj_height= SCREEN_DIST/ (depth+0.0001)
            
            # 레이 캐스팅 결과목록
            self.ray_casting_result.append((depth,proj_height,texture,offset))

            # #draw wall 
            # color=[255/(1+depth ** 5 * 0.00002)] *3
            # pygame.draw.rect(self.game.screen,color, (ray*SCALE,HALF_HEIGHT-proj_height //2,SCALE,proj_height))
                
            #디버깅
            #pygame.draw.line(self.game.screen, 'yellow', (100*ox,100*oy),(100*ox+100*depth*cos_a, 100*oy+100*depth*sin_a),2)
            
            ray_angle += DELTA_ANGLE
    
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()