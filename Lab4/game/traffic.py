import pygame
import random

LANE_H = 70
CAR_W = 82
CAR_H = 42
COLORS = [(220, 65, 65), (235, 145, 45), (155, 75, 190), (60, 175, 95), (205, 185, 50), (65, 105, 215)]


class Car:
    def __init__(self, y, direction, speed, width):
        self.rect = pygame.Rect(0, 0, CAR_W, CAR_H)
        self.rect.center = (0 if direction > 0 else width, y)
        self.direction = direction  # 1=right, -1=left
        self.speed = speed
        self.color = random.choice(COLORS)

    def update(self):
        self.rect.x += self.direction * self.speed

    def off_screen(self, width):
        return self.rect.left > width + 40 or self.rect.right < -40

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=9)
        pygame.draw.rect(screen, (180, 220, 240),
                         pygame.Rect(self.rect.x + 28, self.rect.y + 7, 30, 28), border_radius=5)
        for wx in (self.rect.x + 9, self.rect.right - 16):
            pygame.draw.rect(screen, (25, 25, 28), pygame.Rect(wx, self.rect.y - 3, 10, 7), border_radius=3)
            pygame.draw.rect(screen, (25, 25, 28), pygame.Rect(wx, self.rect.bottom - 4, 10, 7), border_radius=3)
        if getattr(self, "night", False):
            # Headlights point in the direction of travel and reach well beyond the car.
            if self.direction > 0:
                points = [(self.rect.right - 2, self.rect.y + 8),
                          (self.rect.right + 155, self.rect.y - 14),
                          (self.rect.right + 155, self.rect.bottom + 14),
                          (self.rect.right - 2, self.rect.bottom - 8)]
            else:
                points = [(self.rect.left + 2, self.rect.y + 8),
                          (self.rect.left - 155, self.rect.y - 14),
                          (self.rect.left - 155, self.rect.bottom + 14),
                          (self.rect.left + 2, self.rect.bottom - 8)]
            beam = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(beam, (255, 238, 155, 35), points)
            screen.blit(beam, (0, 0))


class Raft:
    def __init__(self, y, width):
        self.rect = pygame.Rect(0, y - 19, 230, 38)
        self.direction = 1
        self.speed = 2.3
        self.width = width

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left > self.width:
            self.rect.right = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 78, 38), self.rect, border_radius=9)
        for x in range(self.rect.x + 18, self.rect.right - 8, 38):
            pygame.draw.line(screen, (185, 130, 72), (x, self.rect.y + 4), (x, self.rect.bottom - 4), 4)


def make_car(lane_idx, width, speed):
    direction = 1 if lane_idx % 2 == 0 else -1
    y = lane_idx * LANE_H + LANE_H // 2
    return Car(y, direction, speed, width)
