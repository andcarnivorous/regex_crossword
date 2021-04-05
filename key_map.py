import pygame as pg
import string


class KeyMapper(object):

    movements = (pg.K_DOWN, pg.K_LEFT, pg.K_UP, pg.K_RIGHT)

    def __init__(self, event, limit, x, y):
        self.event = event
        self.x = x
        self.y = y
        self.limit = limit
        if self.event.key in self.movements:
            self.map_movement()
        self.uni = str(event.unicode)
        self.valid = self.sanitize_key()

    def map_movement(self):
        if self.event.key == pg.K_LEFT:
            self.x -= 1 if self.x > 10 else 0
        if self.event.key == pg.K_RIGHT:
            self.x += 1 if self.x < 9 + self.limit else 0
        if self.event.key == pg.K_UP:
            self.y -= 1 if self.y > 0 else 0
        if self.event.key == pg.K_DOWN:
            self.y += 1 if self.y < self.limit-1 else 0

    def sanitize_key(self):
        if self.uni and self.uni.upper() in string.ascii_uppercase:
            return True
        else:
            return False
