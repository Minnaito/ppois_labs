import pygame
import sys
import json
import random
import os
from constants import *
from entities import Chicken, Crosshair
from record import RecordManager
from parallax import ParallaxBackground


class Game:
    def __init__(self, screen, record_manager):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.record_manager = record_manager
        self.load_config()
        self.init_sounds()
        self.init_parallax()
        self.init_bullet_icons()

        # Группы спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.chickens = pygame.sprite.Group()
        self.bullet_holes = pygame.sprite.Group()

        self.crosshair = Crosshair()
        self.all_sprites.add(self.crosshair)

        # Игровые параметры
        self.score = 0
        self.time_left = self.config['game_time']
        self.ammo = self.config['max_ammo']
        self.max_ammo = self.config['max_ammo']
        self.reload_time = self.config['reload_time']
        self.reload_timer = 0
        self.is_reloading = False
        self.game_over_triggered = False

        # Визуальные эффекты
        self.time_warning_alpha = 0
        self.time_warning_direction = 1

        # Для параллакса - отслеживаем движение мыши
        self.last_mouse_x = SCREEN_WIDTH // 2

        # Шрифты
        try:
            self.font = pygame.font.Font(FONT_PATH, 36)
            self.small_font = pygame.font.Font(FONT_PATH, 24)
            self.big_font = pygame.font.Font(FONT_PATH, 72)
        except:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            self.big_font = pygame.font.Font(None, 72)

        self.running = True
        self.paused = False

    def load_config(self):
        """Загрузка конфигурации."""
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def init_parallax(self):
        """Инициализация параллакс фона."""
        self.parallax_bg = ParallaxBackground()

    def init_sounds(self):
        """Инициализация звуков."""
        pygame.mixer.init()

        self.gunshot = None
        self.hit_sound = None
        self.reload_sound = None
        self.empty_gun_sound = None
        self.time_up_sound = None

        try:
            if os.path.exists(GUNSHOT_SOUND):
                self.gunshot = pygame.mixer.Sound(GUNSHOT_SOUND)
                self.gunshot.set_volume(0.5)
        except Exception as e:
            print(f"Не удалось загрузить звук выстрела: {e}")

        try:
            if os.path.exists(HIT_SOUND):
                self.hit_sound = pygame.mixer.Sound(HIT_SOUND)
                self.hit_sound.set_volume(0.3)
        except Exception as e:
            print(f"Не удалось загрузить звук попадания: {e}")

        try:
            if os.path.exists(RELOAD_SOUND):
                self.reload_sound = pygame.mixer.Sound(RELOAD_SOUND)
        except Exception as e:
            print(f"Не удалось загрузить звук перезарядки: {e}")

        try:
            if os.path.exists(EMPTY_GUN_SOUND):
                self.empty_gun_sound = pygame.mixer.Sound(EMPTY_GUN_SOUND)
        except Exception as e:
            print(f"Не удалось загрузить звук пустого оружия: {e}")

        try:
            if os.path.exists(TIME_UP_SOUND):
                self.time_up_sound = pygame.mixer.Sound(TIME_UP_SOUND)
        except Exception as e:
            print(f"Не удалось загрузить звук окончания времени: {e}")

        try:
            if os.path.exists(BACKGROUND_MUSIC):
                pygame.mixer.music.load(BACKGROUND_MUSIC)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Не удалось загрузить фоновую музыку: {e}")

    def init_bullet_icons(self):
        """Загрузка иконок патронов."""
        try:
            self.bullet_img = pygame.image.load(BULLET_ICON)
            self.bullet_img = pygame.transform.scale(self.bullet_img, (24, 36))
        except Exception as e:
            print(f"Не удалось загрузить иконку полного патрона: {e}")
            self.bullet_img = pygame.Surface((24, 36), pygame.SRCALPHA)

        try:
            self.bullet_empty_img = pygame.image.load(BULLET_EMPTY_ICON)
            self.bullet_empty_img = pygame.transform.scale(self.bullet_empty_img, (24, 36))
        except Exception as e:
            print(f"Не удалось загрузить иконку пустого патрона: {e}")
            self.bullet_empty_img = pygame.Surface((24, 36), pygame.SRCALPHA)

    def spawn_chicken(self):
        """Создание новой курицы с края экрана."""
        level = random.choice(self.config['levels'])
        chicken = Chicken(level)

        if chicken.rect.bottom > SCREEN_HEIGHT - 150:
            chicken.rect.y = random.randint(50, SCREEN_HEIGHT - 200)

        self.chickens.add(chicken)
        self.all_sprites.add(chicken)

    def handle_events(self):
        """Обработка событий."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shoot()
                elif event.button == 3:
                    self.start_reload()

    def update_parallax(self):
        """Обновление параллакс фона на основе движения мыши."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.last_mouse_x

        if abs(dx) > 0:
            speed_factor = 0.5
            self.parallax_bg.update(dx * speed_factor)

        self.last_mouse_x = mouse_x

    def shoot(self):
        """Обработка выстрела."""
        if self.is_reloading:
            if self.empty_gun_sound:
                self.empty_gun_sound.play()
            return

        if self.ammo <= 0:
            if self.empty_gun_sound:
                self.empty_gun_sound.play()
            return

        if self.gunshot:
            self.gunshot.play()

        self.ammo -= 1
        pos = pygame.mouse.get_pos()

        # Проверка попадания в деревья
        if self.parallax_bg.check_shot(pos):
            self.parallax_bg.add_bullet_hole(pos)
            return

        # Проверка попадания в кур
        hits = []
        for chicken in self.chickens:
            if chicken.rect.collidepoint(pos) and not chicken.falling:
                hits.append(chicken)

        for chicken in hits:
            if self.hit_sound:
                self.hit_sound.play()
            self.score += chicken.points
            chicken.hit()

    def start_reload(self):
        """Начало перезарядки."""
        if not self.is_reloading and self.ammo < self.max_ammo:
            self.is_reloading = True
            self.reload_timer = self.reload_time * FPS
            if self.reload_sound:
                self.reload_sound.play()

    def update_reload(self):
        """Обновление перезарядки."""
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.ammo = self.max_ammo
                self.is_reloading = False

    def update_time_warning(self):
        """Эффект предупреждения о времени."""
        if self.time_left <= 10:
            self.time_warning_alpha += self.time_warning_direction * 5
            if self.time_warning_alpha >= 255:
                self.time_warning_alpha = 255
                self.time_warning_direction = -1
            elif self.time_warning_alpha <= 100:
                self.time_warning_alpha = 100
                self.time_warning_direction = 1

    def update(self):
        """Обновление игровой логики."""
        if not self.paused:
            self.update_parallax()
            self.all_sprites.update()
            self.bullet_holes.update()
            self.update_reload()
            self.update_time_warning()

            if random.random() < self.config['chicken_spawn_rate']:
                self.spawn_chicken()

            self.time_left -= 1 / FPS
            if self.time_left <= 0 and not self.game_over_triggered:
                self.time_left = 0
                self.game_over_triggered = True
                self.time_up()

    def time_up(self):
        """Действия при окончании времени."""
        pygame.mixer.music.stop()

        if self.time_up_sound:
            self.time_up_sound.play()

        self.paused = True

        for _ in range(int(FPS * 1.5)):
            self.draw_time_up()
            pygame.display.flip()
            self.clock.tick(FPS)

        self.game_over()

    def draw_time_up(self):
        """Отрисовка экрана окончания времени."""
        self.parallax_bg.draw_background(self.screen)
        self.chickens.draw(self.screen)
        self.parallax_bg.draw_trees(self.screen)
        self.bullet_holes.draw(self.screen)

        text = self.big_font.render("ВРЕМЯ ВЫШЛО!", True, RED)
        shadow = self.big_font.render("ВРЕМЯ ВЫШЛО!", True, BLACK)

        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 + 4))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)

        self.draw_hud()

    def draw_hud(self):
        """Отрисовка интерфейса."""
        score_text = self.font.render(f"Очки: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

        time_color = WHITE
        if self.time_left <= 10:
            time_color = RED if int(self.time_left * 2) % 2 == 0 else ORANGE
        elif self.time_left <= 30:
            time_color = YELLOW

        time_text = self.font.render(f"Время: {int(self.time_left)}", True, time_color)
        self.screen.blit(time_text, (SCREEN_WIDTH - 200, 20))

        ammo_text = self.small_font.render("Патроны:", True, WHITE)
        self.screen.blit(ammo_text, (20, 70))

        spacing = 28
        start_x = 140
        start_y = 50

        for i in range(self.max_ammo):
            if i < self.ammo:
                self.screen.blit(self.bullet_img, (start_x + i * spacing, start_y))
            else:
                if self.is_reloading and int(self.reload_timer / 10) % 2 == 0:
                    self.screen.blit(self.bullet_img, (start_x + i * spacing, start_y))
                else:
                    self.screen.blit(self.bullet_empty_img, (start_x + i * spacing, start_y))

        if self.is_reloading:
            reload_text = self.small_font.render("ПЕРЕЗАРЯДКА...", True, RED)
            self.screen.blit(reload_text, (20, 110))

        hint_text = self.small_font.render("ЛКМ - выстрел | ПКМ - перезарядка", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(hint_text, hint_rect)

        if self.time_left <= 10 and self.time_left > 0:
            warning = self.small_font.render("БЫСТРЕЕ!", True, RED)
            warn_rect = warning.get_rect(center=(SCREEN_WIDTH // 2, 70))
            self.screen.blit(warning, warn_rect)

    def draw(self):
        """Отрисовка игры."""
        self.parallax_bg.draw_background(self.screen)
        self.chickens.draw(self.screen)
        self.parallax_bg.draw_trees(self.screen)
        self.screen.blit(self.crosshair.image, self.crosshair.rect)
        self.draw_hud()

        pygame.display.flip()

    def game_over(self):
        """Завершение игры."""
        if self.record_manager.is_highscore(self.score):
            self.enter_name()
        self.running = False

    def enter_name(self):
        """Ввод имени для рекорда."""
        name = ""
        try:
            font = pygame.font.Font(FONT_PATH, 48)
            small_font = pygame.font.Font(FONT_PATH, 24)
        except:
            font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 24)

        while True:
            self.screen.fill(BLACK)

            title = font.render("НОВЫЙ РЕКОРД!", True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

            prompt = font.render("Введите ваше имя:", True, WHITE)
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))

            name_text = font.render(name, True, GREEN)
            self.screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 400))

            hint = small_font.render("Enter - сохранить", True, GRAY)
            self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 500))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        self.record_manager.add_record(name, self.score)
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return
                    else:
                        if len(name) < 15 and event.unicode.isprintable():
                            name += event.unicode

    def run(self):
        """Главный игровой цикл."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()