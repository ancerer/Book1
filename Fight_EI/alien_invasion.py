import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from  game_stats import GameStats
from button import Button


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一个play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一艘飞船
    ship = Ship(screen, ai_settings)
    # 创建一个用于存放子弹的组
    bullets = Group()
    # 创建一个外星人
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建统计信息
    stats = GameStats(ai_settings)

    # 开始游戏的主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_event(ai_settings, screen, stats, play_button, ship, bullets, aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens)
            gf.update_aliens(ai_settings, stats, screen, ship, bullets, aliens)
            
        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button)


run_game()


