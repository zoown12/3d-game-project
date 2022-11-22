import pygame

class Sound:
    def __init__(self,game):
        self.game = game
        pygame.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun =pygame.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_attack = pygame.mixer.Sound(self.path + 'npc_attack.wav')
        self.npc_death = pygame.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_pain = pygame.mixer.Sound(self.path + 'npc_pain.wav')
        self.player_pain = pygame.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = pygame.mixer.Sound(self.path + 'theme.wav')