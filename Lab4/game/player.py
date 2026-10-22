import pygame

LANE_H = 70
PLAYER_W = 48
PLAYER_H = 36


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, PLAYER_W, PLAYER_H)
        self.rect.center = (x, y)
        self.color = (65, 170, 235)
        self.move_cooldown = 0

    def move(self, keys, min_x, max_x, max_y):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return

        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -40
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 40
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -LANE_H
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = LANE_H

        if dx or dy:
            self.rect.x = max(min_x, min(max_x - self.rect.width, self.rect.x + dx))
            # Vertical movement is snapped to lane centers; clamp the center rather
            # than the rectangle's top so the player can reach the goal bank.
            center_y = max(LANE_H // 2, min(max_y - LANE_H // 2, self.rect.centery + dy))
            self.rect.centery = center_y
            self.move_cooldown = 10

    def draw(self, screen):
        # A small horizontal car, centered in its current road lane.
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (185, 225, 245),
                         pygame.Rect(self.rect.x + 13, self.rect.y + 7, 22, 22), border_radius=5)
        for wy in (self.rect.y + 3, self.rect.bottom - 9):
            pygame.draw.rect(screen, (25, 25, 28), pygame.Rect(self.rect.x + 9, wy, 11, 7), border_radius=3)
            pygame.draw.rect(screen, (25, 25, 28), pygame.Rect(self.rect.right - 20, wy, 11, 7), border_radius=3)
