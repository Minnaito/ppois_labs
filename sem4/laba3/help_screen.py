import pygame
import sys
from constants import *


def show_help(screen):
    """Отображение экрана справки."""
    font = pygame.font.Font(FONT_PATH, 36)
    small_font = pygame.font.Font(FONT_PATH, 24)

    lines = [
        "ПРАВИЛА ИГРЫ MOORHUHN",
        "",
        "Цель игры:",
        "Настрелять как можно больше кур за 60 секунд.",
        "",
        "Курицы на разном расстоянии дают разные очки:",
        "• Близкие (красные) - 10 очков",
        "• Средние (зеленые) - 20 очков",
        "• Далёкие (синие) - 30 очков",
        "",
        "Патроны:",
        "• У вас 8 патронов",
        "• Перезарядка автоматическая (2 секунды)",
        "• Можно перезарядиться вручную клавишей R",
        "",
        "Препятствия:",
        "Деревья и столб мешают стрельбе -",
        "пули застревают в них!",
        "",
        "Управление:",
        "• Мышь - прицел",
        "• Левый клик - выстрел",
        "• R - ручная перезарядка",
        "• ESC - выход в меню",
        "",
        "Нажмите любую клавишу для возврата"
    ]

    waiting = True
    while waiting:
        screen.fill(BLACK)

        y = 50
        for line in lines:
            if line.startswith('•'):
                text = small_font.render(line, True, YELLOW)
            elif line.startswith('ПРАВИЛА'):
                text = font.render(line, True, RED)
            elif line == "":
                y += 10
                continue
            else:
                text = small_font.render(line, True, WHITE)

            screen.blit(text, (100, y))
            y += 30

        pygame.display.flip()
