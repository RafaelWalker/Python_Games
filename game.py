from turtle import Screen
import pgzrun
from math import sin, cos, pi
import random
from pygame import Rect 

# Tela e recursos do jogo
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Game"

# Configurações globais
game_running = False
sound_on = True

# Animações e sprites
hero_sprites = ['hero_walk1', 'hero_walk2', 'hero_idle']
enemy_sprites = ['enemy_walk1', 'enemy_walk2', 'enemy_idle']
music_track = 'background_music'

# Classe do herói
class Hero:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.speed = 5
        self.jump_power = 10
        self.is_jumping = False
        self.gravity = 1
        self.rect = Rect(x, y, 64, 64)
        self.sprite = hero_sprites[0]
        self.sprite_index = 0
        self.animation_speed = 0.2
    
    def move(self, direction):
        if direction == 'left':
            self.pos[0] -= self.speed
        elif direction == 'right':
            self.pos[0] += self.speed
    
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_power = -15
    
    def update(self):
        # Atualiza o movimento do pulo e aplica gravidade
        if self.is_jumping:
            self.pos[1] += self.jump_power
            self.jump_power += self.gravity
        
        # Limitar o jogador ao chão
        if self.pos[1] >= HEIGHT - 64:
            self.pos[1] = HEIGHT - 64
            self.is_jumping = False
        
        # Atualizar sprite de animação
        self.sprite_index += self.animation_speed
        if self.sprite_index >= len(hero_sprites):
            self.sprite_index = 0
        self.sprite = hero_sprites[int(self.sprite_index)]
    
    def draw(self):
        Screen.blit(self.sprite, (self.pos[0], self.pos[1]))

# Classe de inimigo
class Enemy:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.speed = random.choice([-3, 3])
        self.rect = Rect(x, y, 64, 64)
        self.sprite = enemy_sprites[0]
        self.sprite_index = 0
        self.animation_speed = 0.2
    
    def update(self):
        # Movimento horizontal do inimigo
        self.pos[0] += self.speed
        if self.pos[0] <= 0 or self.pos[0] >= WIDTH - 64:
            self.speed *= -1  # Muda de direção quando atinge a borda
        
        # Atualizar sprite de animação
        self.sprite_index += self.animation_speed
        if self.sprite_index >= len(enemy_sprites):
            self.sprite_index = 0
        self.sprite = enemy_sprites[int(self.sprite_index)]
    
    def draw(self):
        Screen.blit(self.sprite, (self.pos[0], self.pos[1]))

# Inicialização do herói e inimigos
hero = Hero(100, HEIGHT - 64)
enemies = [Enemy(random.randint(200, WIDTH - 64), HEIGHT - 64) for _ in range(5)]

def draw():
    if game_running:
        Screen.clear()
        hero.draw()
        for enemy in enemies:
            enemy.draw()
    else:
        draw_menu()

def draw_menu():
    Screen.clear()
    Screen.draw.text("Platformer Game", center=(WIDTH // 2, HEIGHT // 3), fontsize=50)
    Screen.draw.text("Press SPACE to Start", center=(WIDTH // 2, HEIGHT // 2), fontsize=30)
    Screen.draw.text("Press M to Toggle Sound", center=(WIDTH // 2, HEIGHT // 1.7), fontsize=30)
    Screen.draw.text("Press ESC to Quit", center=(WIDTH // 2, HEIGHT // 1.5), fontsize=30)

def update():
    global game_running
    if game_running:
        hero.update()
        for enemy in enemies:
            enemy.update()

def on_key_down(key):
    global game_running, sound_on
    if not game_running:
        if key == keys.SPACE:
            game_running = True
            if sound_on:
                music.play(music_track)
        elif key == keys.ESCAPE:
            exit()
        elif key == keys.M:
            sound_on = not sound_on
            if sound_on:
                music.play(music_track)
            else:
                music.stop()
    else:
        # Controles do herói
        if key == keys.LEFT:
            hero.move('left')
        elif key == keys.RIGHT:
            hero.move('right')
        elif key == keys.UP:
            hero.jump()

pgzrun.go()
