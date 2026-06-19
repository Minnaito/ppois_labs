import random
import pygame
import os
from constants import *


class Chicken(pygame.sprite.Sprite):
    """Класс курицы с анимацией полёта и падения."""

    def __init__(self, level_config, x=None, y=None):
        super().__init__()

        self.level = level_config['name']
        self.points = level_config['points']
        self.speed = level_config['speed']
        self.scale = level_config['scale']

        # Размеры из конфига
        self.base_width = level_config.get('width', 80)
        self.base_height = level_config.get('height', 80)
        self.width = int(self.base_width * self.scale)
        self.height = int(self.base_height * self.scale)

        # Загрузка изображений для анимации полёта
        self.fly_frames = []
        for i in range(1, 3):
            img_path = os.path.join(IMAGES_DIR, f'chicken_{self.level}_fly{i}.png')
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (self.width, self.height))
            self.fly_frames.append(img)

        if self.level == 'near':
            dead_image_path = CHICKEN_NEAR_DEAD_IMAGE
        elif self.level == 'mid':
            dead_image_path = CHICKEN_MID_DEAD_IMAGE
        else:
            dead_image_path = CHICKEN_FAR_DEAD_IMAGE

        self.dead_image = pygame.image.load(dead_image_path)
        self.dead_image = pygame.transform.scale(self.dead_image, (self.width, self.height))

        # Анимация
        self.current_frame = 0
        self.animation_speed = 10
        self.animation_counter = 0
        self.image = self.fly_frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Спавн
        if x is None:
            side = random.choice(['left', 'right'])
            if side == 'left':
                x = -self.rect.width
                self.direction = 1
            else:
                x = SCREEN_WIDTH
                self.direction = -1
        else:
            self.direction = random.choice([-1, 1])

        if y is None:
            y = random.randint(20, SCREEN_HEIGHT // 2)

        self.rect.x = x
        self.rect.y = y

        # ОТРАЖЕНИЕ КАРТИНОК
        if self.direction == 1:
            pass
        else:
            for i in range(len(self.fly_frames)):
                self.fly_frames[i] = pygame.transform.flip(self.fly_frames[i], True, False)
            self.dead_image = pygame.transform.flip(self.dead_image, True, False)
            self.image = self.fly_frames[self.current_frame]

        self.alive = True
        self.falling = False
        self.fall_speed = 0

    def update(self):
        if self.falling:
            # Анимация падения
            self.rect.y += self.fall_speed
            self.fall_speed += 0.5
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
        else:
            # Движение
            self.rect.x += self.direction * self.speed
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()

            # Анимация взмахов крыльев
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.fly_frames)
                self.image = self.fly_frames[self.current_frame]

    def hit(self):
        """Попадание в курицу."""
        self.alive = False
        self.falling = True
        self.image = self.dead_image


class Crosshair(pygame.sprite.Sprite):
    """Прицел (следует за мышью)."""

    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(CROSSHAIR_IMAGE)
        self.image = pygame.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect()

    def update(self):
        """Прицел следует за мышью."""
        self.rect.center = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)