import pygame
import sys
import os
from constants import *
from game import Game
from record import RecordManager


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.record_manager = RecordManager()

        try:
            self.background = pygame.image.load(os.path.join(IMAGES_DIR, 'menu_background.png'))
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None

        try:
            pygame.mixer.music.load(os.path.join(SOUNDS_DIR, 'menu_music.mp3'))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass

        try:
            self.font = pygame.font.Font(FONT_PATH, 48)
            self.small_font = pygame.font.Font(FONT_PATH, 32)
        except:
            self.font = pygame.font.Font(None, 48)
            self.small_font = pygame.font.Font(None, 32)

        self.options = ["Начать игру", "Таблица рекордов", "Справка", "Стереть рекорды", "Выход"]
        self.selected = 0

        self.option_rects = []
        self.update_option_rects()

    def update_option_rects(self):
        self.option_rects = []
        for i, option in enumerate(self.options):
            text = self.small_font.render(option, True, WHITE)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
            self.option_rects.append(rect)

    def run(self):
        while True:
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.select_option()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected = i
                            self.select_option()
                            break

            self.clock.tick(FPS)

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("MOORHUHN", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        self.update_option_rects()

        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else WHITE
            text = self.small_font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
            self.screen.blit(text, rect)

    def select_option(self):
        if self.selected == 0:
            pygame.mixer.music.stop()
            game = Game(self.screen, self.record_manager)
            game.run()
            try:
                pygame.mixer.music.load(os.path.join(SOUNDS_DIR, 'menu_music.mp3'))
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            except:
                pass
        elif self.selected == 1:
            self.show_records()
        elif self.selected == 2:
            self.show_help()
        elif self.selected == 3:
            self.clear_records()
        elif self.selected == 4:
            pygame.quit()
            sys.exit()

    def show_records(self):
        records = self.record_manager.get_top()

        try:
            bg = pygame.image.load(os.path.join(IMAGES_DIR, 'menu_background.png'))
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            bg = None

        waiting = True
        while waiting:
            if bg:
                self.screen.blit(bg, (0, 0))
            else:
                self.screen.fill(BLACK)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            title = self.font.render("ТАБЛИЦА РЕКОРДОВ", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)

            if records:
                y = 200
                for i, rec in enumerate(records):
                    color = GREEN if i == 0 else WHITE
                    text = self.small_font.render(f"{i + 1}. {rec['name']} - {rec['score']}", True, color)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                    self.screen.blit(text, text_rect)
                    y += 50
            else:
                text = self.small_font.render("Пока нет рекордов", True, GRAY)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
                self.screen.blit(text, text_rect)

            hint = self.small_font.render("ESC - назад", True, GRAY)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 600))
            self.screen.blit(hint, hint_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting = False

    def show_help(self):
        try:
            bg = pygame.image.load(os.path.join(IMAGES_DIR, 'menu_background.png'))
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            bg = None

        try:
            title_font = pygame.font.Font(FONT_PATH, 48)
            section_font = pygame.font.Font(FONT_PATH, 32)
            text_font = pygame.font.Font(FONT_PATH, 24)
        except:
            title_font = pygame.font.Font(None, 48)
            section_font = pygame.font.Font(None, 32)
            text_font = pygame.font.Font(None, 24)

        help_lines = [
            "ПРАВИЛА ИГРЫ MOORHUHN", "",
            "Цель игры:", "Настрелять как можно больше кур за 60 секунд.", "",
            "Курицы на разном расстоянии дают разные очки:",
            "• Близкие - 10 очков",
            "• Средние - 20 очков",
            "• Далёкие - 30 очков", "",
            "Патроны:", "• У вас 8 патронов",
            "• Перезарядка вручную правой кнопкой мыши", "",
            "Препятствия:", "Деревья мешают стрельбе -",
            "пули застревают в них!", "",
            "Управление:", "• Мышь - прицел",
            "• Левый клик - выстрел",
            "• Правый клик - перезарядка",
            "• ESC - выход в меню", "", "", "Для выхода нажмите ESC"
        ]

        waiting = True
        while waiting:
            if bg:
                self.screen.blit(bg, (0, 0))
            else:
                self.screen.fill(BLACK)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            title = title_font.render("СПРАВКА", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(title, title_rect)

            y = 150
            for line in help_lines:
                if line.startswith('ПРАВИЛА'):
                    text = section_font.render(line, True, RED)
                elif line.startswith('•'):
                    text = text_font.render(line, True, YELLOW)
                elif line == "":
                    y += 10
                    continue
                elif line == "Для выхода нажмите ESC":
                    text = text_font.render(line, True, RED)
                else:
                    text = text_font.render(line, True, WHITE)

                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(text, text_rect)
                y += 30

            hint = self.small_font.render("ESC - назад", True, GRAY)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(hint, hint_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting = False

    def clear_records(self):
        waiting = True
        choice = 0

        try:
            bg = pygame.image.load(os.path.join(IMAGES_DIR, 'menu_background.png'))
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            bg = None

        while waiting:
            if bg:
                self.screen.blit(bg, (0, 0))
            else:
                self.screen.fill(BLACK)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            title = self.font.render("Удалить все рекорды?", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(title, title_rect)

            warning = self.small_font.render("Это действие нельзя отменить!", True, RED)
            warning_rect = warning.get_rect(center=(SCREEN_WIDTH // 2, 280))
            self.screen.blit(warning, warning_rect)

            colors = [GRAY, GRAY]
            colors[choice] = YELLOW

            no_text = self.small_font.render("НЕТ", True, colors[0])
            no_rect = no_text.get_rect(center=(SCREEN_WIDTH // 2 - 100, 400))
            self.screen.blit(no_text, no_rect)

            yes_text = self.small_font.render("ДА", True, colors[1])
            yes_rect = yes_text.get_rect(center=(SCREEN_WIDTH // 2 + 100, 400))
            self.screen.blit(yes_text, yes_rect)

            hint = self.small_font.render("Enter/ЛКМ - подтвердить | ESC - отмена", True, GRAY)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(hint, hint_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                    elif event.key == pygame.K_LEFT:
                        choice = 0
                    elif event.key == pygame.K_RIGHT:
                        choice = 1
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if choice == 1:
                            self.record_manager.clear_records()
                            self.show_message("Рекорды удалены!")
                        waiting = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if no_rect.collidepoint(mouse_pos):
                        waiting = False
                    elif yes_rect.collidepoint(mouse_pos):
                        self.record_manager.clear_records()
                        self.show_message("Рекорды удалены!")
                        waiting = False

    def show_message(self, text):
        try:
            bg = pygame.image.load(os.path.join(IMAGES_DIR, 'menu_background.png'))
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            bg = None

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1500:
            if bg:
                self.screen.blit(bg, (0, 0))
            else:
                self.screen.fill(BLACK)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            msg = self.font.render(text, True, GREEN)
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(msg, msg_rect)

            pygame.display.flip()
            pygame.time.wait(16)
