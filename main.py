import pygame,pygame_menu
import sys
from settings1 import *
from map1 import *
from raycasting import *
from player1 import *
from object_renderer import *
from sprite_object1 import *
from object_handler import *
from weapon import *
from sound import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False) #마우스 포인트 숨기기
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event,40) #타이머 40밀리초 설정
        self.new_game()
        
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        # self.static_sprite = SpriteObject(self)
        # self.animated_sprite = AnimatedSprite(self)
        self.object_handler = ObjectHandler(self)
        self.weapon=Weapon(self)
        self.sound=Sound(self)
    
    def update(self):
        self.player.update()
        self.raycasting.update()
        
        #object_renderer 완성 후 실행
        # self.static_sprite.update()
        # self.animated_sprite.update()
    
        self.object_handler.update()
        self.weapon.update() 
        
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        #self.clock.tick(0)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        #self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()
        
    def check_events(self):
        self.global_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)
                
                
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


class Menu:
    pygame.init()
    surface = pygame.display.set_mode((600, 400))
    select_map = 0

    def level(self, value):  # 난이도 선택시 호출되는 함수
        global select_map
        print("난이도 선택값:", value)
        if value == 1:
            select_map = 1
        elif value == 2:
            select_map = 2

    def start():  # 게임시작 선택시 호출되는 함수
        print("게임시작")
        game = Game()
        game.run()

    def quit():
        pygame.quit()
        sys.exit()

    t = pygame_menu.themes.THEME_DARK
    t.widget_font = pygame.font.SysFont("gothic", 30)

    menu = pygame_menu.Menu("DOOM", 400, 300, theme=t)
    menu.add.selector("Level ", [("Hard", 1), ("Easy", 2)], onchange=level)
    menu.add.button("Start", start)
    menu.add.button("Quit", quit)
    menu.mainloop(surface)

if __name__ == '__main__':
    game = Game()
    game.run()