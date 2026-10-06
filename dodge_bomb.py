import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DEKTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface) -> None:
    #screen = pg.Surface((WIDTH, HEIGHT))
    game = pg.Surface((WIDTH, HEIGHT))
    #game.set_colorkey((0, 0, 0))
    pg.draw.rect(game,(0, 0, 0),(0, 0, WIDTH, HEIGHT)) 
    fonto = pg.font.Font(None, 90)
    txt = fonto.render("Game Over",True,(255, 255, 255))
    game.blit(txt, [350, 300])
    k8_png = pg.image.load("fig/8.png")  # 1-4のこうかとん
    game.blit(k8_png, [300, 300])
    game.blit(k8_png, [700, 300])
    screen.blit(game, [0, 0])
    pg.display.update()
    time.sleep(5)
    return game


'''
def init_bb_imgs() -> tuple[list[pg.Surfane], list[int]]:
    
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0,0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs
'''
    

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん又は爆弾のRect
    戻り値：タプル（横方向判定、縦方向判定）
    画面内ならTrue　画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = (random.randint(0, WIDTH))
    bb_rct.centery = (random.randint(0, HEIGHT))
    vx, vy = +5, -5
    bb_img.set_colorkey((0, 0, 0))
    clock = pg.time.Clock()
    tmr = 0
    #bb_rct.eidth = bb_img.get_rect().width
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # 練習4；kkとbbが重なっていたら
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key,tpl in DEKTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向移動
                sum_mv[1] += tpl[1]  # 縦方向移動
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこかしらはみ出ている
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])# 先ほどの動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 練習2：爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習2：爆弾
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
