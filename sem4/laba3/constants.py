import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
BROWN = (101, 67, 33)
DARK_GREEN = (34, 139, 34)

BACKGROUND_IMAGE = os.path.join(IMAGES_DIR, 'background.png')
CROSSHAIR_IMAGE = os.path.join(IMAGES_DIR, 'crosshair.png')
TREE_IMAGE = os.path.join(IMAGES_DIR, 'tree.png')
POLE_IMAGE = os.path.join(IMAGES_DIR, 'pole.png')

CHICKEN_NEAR_FLY1_IMAGE = os.path.join(IMAGES_DIR, 'chicken_near_fly1.png')
CHICKEN_NEAR_FLY2_IMAGE = os.path.join(IMAGES_DIR, 'chicken_near_fly2.png')
CHICKEN_MID_FLY1_IMAGE = os.path.join(IMAGES_DIR, 'chicken_mid_fly1.png')
CHICKEN_MID_FLY2_IMAGE = os.path.join(IMAGES_DIR, 'chicken_mid_fly2.png')
CHICKEN_FAR_FLY1_IMAGE = os.path.join(IMAGES_DIR, 'chicken_far_fly1.png')
CHICKEN_FAR_FLY2_IMAGE = os.path.join(IMAGES_DIR, 'chicken_far_fly2.png')

CHICKEN_NEAR_DEAD_IMAGE = os.path.join(IMAGES_DIR, 'chicken_near_dead.png') 
CHICKEN_MID_DEAD_IMAGE = os.path.join(IMAGES_DIR, 'chicken_mid_dead.png')
CHICKEN_FAR_DEAD_IMAGE = os.path.join(IMAGES_DIR, 'chicken_far_dead.png')

BULLET_ICON = os.path.join(IMAGES_DIR, 'bullet.png')
BULLET_EMPTY_ICON = os.path.join(IMAGES_DIR, 'bullet_empty.png')

GUNSHOT_SOUND = os.path.join(SOUNDS_DIR, 'gunshot.wav')
HIT_SOUND = os.path.join(SOUNDS_DIR, 'hit.wav')
BACKGROUND_MUSIC = os.path.join(SOUNDS_DIR, 'background_music.mp3')
RELOAD_SOUND = os.path.join(SOUNDS_DIR, 'reload.wav')
EMPTY_GUN_SOUND = os.path.join(SOUNDS_DIR, 'empty_gun.wav')
TIME_UP_SOUND = os.path.join(SOUNDS_DIR, 'time_up.wav')

FONT_PATH = os.path.join(FONTS_DIR, 'arial.ttf')
if not os.path.exists(FONT_PATH):
    FONT_PATH = None

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
RECORDS_FILE = os.path.join(BASE_DIR, 'records.json')

MENU_BACKGROUND = os.path.join(IMAGES_DIR, 'menu_background.png')
RECORDS_BACKGROUND = os.path.join(IMAGES_DIR, 'menu_background.png')
HELP_BACKGROUND = os.path.join(IMAGES_DIR, 'menu_background.png')

MENU_MUSIC = os.path.join(SOUNDS_DIR, 'menu_music.mp3')

SKY_IMAGE = os.path.join(IMAGES_DIR, 'sky.png')
CLOUDS_IMAGE = os.path.join(IMAGES_DIR, 'clouds.png')
FIELD_IMAGE = os.path.join(IMAGES_DIR, 'field.png')
TREES_BG_IMAGE = os.path.join(IMAGES_DIR, 'trees_bg.png')
