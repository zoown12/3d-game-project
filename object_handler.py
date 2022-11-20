from sprite_object1 import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'resources/sprites/static_sprites'
        self.anim_sprite_path = 'resources/sprites/animated_sprites'
        add_sprite = self.add_sprite
        
        # 맵에 구조물 생성
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        
    def update(self):
        [sprite.update() for sprite in self.sprite_list]
            
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
