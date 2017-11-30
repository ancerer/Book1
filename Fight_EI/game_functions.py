import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

# 将事件管理和其它分开
from pygame.examples import aliens


def check_keydown_events(event,ai_settings, screen, ship, bullets):
    # 响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 创建新子弹并将其加入到编组中
        fire_bullets(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, play_button, ship, aliens, bullets, mouse_x, mouse_y, stats):
    """在玩家点击play按钮时，启动游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_event(ai_settings, screen, stats, play_button, ship, bullets, aliens):
    # 响应按键和鼠标事件，每次按键都被注册为一个KEYDOWN事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, play_button, ship, aliens, bullets, mouse_x, mouse_y, stats)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采用措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
                change_fleet_direction(ai_settings, aliens)
                break


def change_fleet_direction(ai_settings, aliens):
    """将外星人向下移动，并改变运动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_screen(ai_settings, screen, stats,  ship, bullets, aliens, play_button):
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, bullets, aliens):
    """更新子弹位置"""
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中外星人，若有，删除子弹和外星人
    check_bullets_aliens_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullets_aliens_collisions(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def check_aliens_bottom(ai_settings, stats, screen, ship, bullets, aliens):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, bullets, aliens)
            break


def update_aliens(ai_settings, stats, screen, ship, bullets, aliens):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测飞船和外星人之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # noinspection PyArgumentList
        ship_hit(ai_settings, stats, screen, ship, bullets, aliens)

    check_aliens_bottom(ai_settings, stats, screen, ship, bullets, aliens)


def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳外星人的个数"""
    available_space_x = ai_settings.screen_width - 1 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放入当前行"""
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(screen, ai_settings)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def ship_hit(ai_settings, stats, screen, ship, bullets, aliens):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 清空外星人和子弹列表
        bullets.empty()
        aliens.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False



