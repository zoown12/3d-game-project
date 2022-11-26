from sprite_object1 import *
from random import randint,random,choice


class NPC(AnimatedSprite):
    def __init__(self,game,path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift =0.38, animation_time=180):
        super(). __init__(game,path,pos,scale,shift,animation_time)
        self.attack_images=self.get_images(self.path+'/attack')
        self.death_images=self.get_images(self.path+'/death')
        self.idle_images=self.get_images(self.path+'/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist=randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy=0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter=0 #한 번만 재생되게 사망 애니메이션 필요
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic() #npc 움직이기
       # self.draw_ray_cast()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)): #적 자체 크기만 고려 size
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos #플레이어가 있는 타일로 이동.

        #pg.draw.rect(self.game.screen,'blue',(100*next_x, 100*next_y,100,100)) # 디버깅
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x) #NPC의 각도와 타일의 중심
            dx = math.cos(angle) * self.speed #x방향 -> cos 계산
            dy = math.sin(angle) * self.speed#y방향 -> sin 계산ddddddddd
            self.check_wall_collision(dx, dy) #NPC 이동

    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)
    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1: #전역 변수의 40밀리초를 통해 npc 죽는 반응속도가 더 빨라짐
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot: #벽 뒤에서 총격을 확인하면 npc적중 방법 시선 검사(벽 뒤에서 쏘면 적 안맞게)
            if HALF_WIDTH - self.sprite_half_width <self.screen_x < HALF_WIDTH + self.sprite_half_width: #프레젝션 값을 고려하여 NPC위치 중앙
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -=self.game.weapon.damage #데미지입으면 NPC 체력 감소
                self.check_health() #NPC 체력 update

    def check_health(self):
        if self.health<1: #체력이 떨어지면 사운드,생동성 KILL
            self.alive = False
            self.game.sound.npc_death.play()

    def run_logic(self):
        if self.alive:
            self.ray_cast_value=self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist: #플레이어 거리가 공격 거리 보다 적을 떄
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger: #벽뒤에 있어도 플레이어를 찾 을수 있게 도와줌.
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos: #플레이어가 적과 같은 타일에 있는지 확인
            return True
        wall_dist_v, wall_dist_h = 0,0 #수직,수평을 위해 플레이어와 벽까지의 거리
        player_dist_v, player_dist_h = 0,0

        self.ray_casting_result = []
        ox, oy = self.game.player.pos  # 맵에서 플레이어 위치
        x_map, y_map = self.game.player.map_pos  # 멥에서 플레이어가 있는 타일의 위치
        texture_vert, texture_hor = 1, 1

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # 가로
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor #하나의 광선에 대해 raycast하는 세타 각도 이 광선이 벽이나 NPC에 부딪히면 기록
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # 세로
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)  # 방향 벡터

        depth_vert = (x_vert - ox) / cos_a  # 벡터 크기
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):  # 광선 발사
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:  # 광선이 벽에 부딪히면 종료
                wall_dist_v = depth_vert
                break
            # 아니면 광선을 더 멀리 발사
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v,player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h) #벽과 플레이어의 거리의 최대값


        if 0<player_dist<wall_dist or not wall_dist: #플레이어와 npc 사이에 직접적인 시선있는지 확인
            return True
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen,'red',(100*self.x,100*self.y),15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100*self.game.player.x,100*self.game.player.y),
                         (100*self.x,100*self.y),2)

class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

class CacoDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35

class CyberDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25