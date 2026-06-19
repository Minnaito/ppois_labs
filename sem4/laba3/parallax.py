import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class ParallaxBackground:
    """Класс для создания эффекта параллакса с деревьями как препятствиями."""

    def __init__(self):
        # Загрузка изображений
        self.sky_img = pygame.image.load('assets/images/sky.png').convert_alpha()
        self.clouds_img = pygame.image.load('assets/images/clouds.png').convert_alpha()
        self.field_img = pygame.image.load('assets/images/field.png').convert_alpha()
        self.trees_img = pygame.image.load('assets/images/trees_bg.png').convert_alpha()

        # Масштабируем под экран
        self.sky_img = pygame.transform.scale(self.sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clouds_img = pygame.transform.scale(self.clouds_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.field_img = pygame.transform.scale(self.field_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.trees_img = pygame.transform.scale(self.trees_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Позиции для бесконечной прокрутки
        self.clouds_x = 0
        self.field_x = 0
        self.trees_x = 0

        # Скорости движения слоев
        self.clouds_speed = 0.3
        self.field_speed = 0.8
        self.trees_speed = 1.4

        # Изображение следа от пули
        self.hole_img = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.hole_img, (30, 30, 30), (6, 6), 5)

        self.bullet_holes = []

        # Маска для деревьев
        self.trees_mask = pygame.mask.from_surface(self.trees_img)

    def update(self, dx):
        """Обновление позиций слоев."""
        old_trees_x = self.trees_x

        # Обновляем позиции
        self.clouds_x -= dx * self.clouds_speed
        self.field_x -= dx * self.field_speed
        self.trees_x -= dx * self.trees_speed

        # Зацикливание
        if self.clouds_x <= -SCREEN_WIDTH:
            self.clouds_x += SCREEN_WIDTH
        if self.clouds_x >= SCREEN_WIDTH:
            self.clouds_x -= SCREEN_WIDTH

        if self.field_x <= -SCREEN_WIDTH:
            self.field_x += SCREEN_WIDTH
        if self.field_x >= SCREEN_WIDTH:
            self.field_x -= SCREEN_WIDTH

        if self.trees_x <= -SCREEN_WIDTH:
            self.trees_x += SCREEN_WIDTH

            for hole in self.bullet_holes:
                hole['x'] += SCREEN_WIDTH
        if self.trees_x >= SCREEN_WIDTH:
            self.trees_x -= SCREEN_WIDTH
            for hole in self.bullet_holes:
                hole['x'] -= SCREEN_WIDTH

        # Обновляем позиции следов
        delta_x = self.trees_x - old_trees_x
        for hole in self.bullet_holes:
            hole['x'] += delta_x

        # Обновляем время жизни следов и удаляем старые
        for i in range(len(self.bullet_holes) - 1, -1, -1):
            self.bullet_holes[i]['lifetime'] -= 0.2
            if self.bullet_holes[i]['lifetime'] <= 0:
                del self.bullet_holes[i]

    def add_bullet_hole(self, pos):
        """Добавить след от пули на дереве."""
        # Находим, в какую копию деревьев попала пуля
        positions = [self.trees_x, self.trees_x - SCREEN_WIDTH, self.trees_x + SCREEN_WIDTH]

        for x_offset in positions:
            local_x = pos[0] - x_offset
            local_y = pos[1]

            if 0 <= local_x < SCREEN_WIDTH and 0 <= local_y < SCREEN_HEIGHT:
                try:
                    if self.trees_mask.get_at((int(local_x), int(local_y))):
                        self.bullet_holes.append({
                            'x': x_offset + local_x,
                            'y': local_y,
                            'lifetime': FPS * 0.2
                        })
                        break
                except:
                    pass

    def draw_background(self, screen):
        """Отрисовка фона."""
        screen.blit(self.sky_img, (0, 0))

        screen.blit(self.clouds_img, (self.clouds_x, 0))
        screen.blit(self.clouds_img, (self.clouds_x - SCREEN_WIDTH, 0))
        screen.blit(self.clouds_img, (self.clouds_x + SCREEN_WIDTH, 0))

        screen.blit(self.field_img, (self.field_x, 0))
        screen.blit(self.field_img, (self.field_x - SCREEN_WIDTH, 0))
        screen.blit(self.field_img, (self.field_x + SCREEN_WIDTH, 0))

    def draw_trees(self, screen):
        """Отрисовка деревьев и следов от пуль."""
        screen.blit(self.trees_img, (self.trees_x, 0))
        screen.blit(self.trees_img, (self.trees_x - SCREEN_WIDTH, 0))
        screen.blit(self.trees_img, (self.trees_x + SCREEN_WIDTH, 0))

        # Рисуем следы от пуль на деревьях
        for hole in self.bullet_holes:
            alpha = min(255, int(255 * hole['lifetime'] / (FPS * 0.2)))
            if alpha > 0:
                hole_img_alpha = self.hole_img.copy()
                hole_img_alpha.set_alpha(alpha)
                screen.blit(hole_img_alpha, (hole['x'], hole['y']))
            else:
                screen.blit(self.hole_img, (hole['x'], hole['y']))

    def check_shot(self, pos):
        """Проверка, попала ли пуля в дерево."""
        # Проверяем все три копии деревьев
        positions = [self.trees_x, self.trees_x - SCREEN_WIDTH, self.trees_x + SCREEN_WIDTH]

        for x_offset in positions:
            local_x = pos[0] - x_offset
            local_y = pos[1]

            if 0 <= local_x < SCREEN_WIDTH and 0 <= local_y < SCREEN_HEIGHT:
                try:
                    # Проверяем маску
                    if self.trees_mask.get_at((int(local_x), int(local_y))):
                        return True
                except:
                    # Если маска не работает, проверяем по цвету пикселя
                    pixel_color = self.trees_img.get_at((int(local_x), int(local_y)))
                    if pixel_color[3] > 0:
                        return True
        return False

    def reset(self):
        """Сброс позиций всех слоев и следов."""
        self.clouds_x = 0
        self.field_x = 0
        self.trees_x = 0
        self.bullet_holes = []