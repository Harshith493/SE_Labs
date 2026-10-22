import json
import math
import os
import pygame
import random
from game.player import Player, LANE_H
from game.traffic import Raft, make_car

# Eight hops from the starting bank to the goal bank requires nine lane rows:
# the two banks plus the seven intervening road/raft rows.
LANES = 9
WIDTH = 800
HEIGHT = LANES * LANE_H
FPS = 60
ROAD = (55, 58, 62)
RAFT_LANE = 3
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "high_scores.json")


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Escape - Frogger")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 17, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.high_scores = self.load_high_scores()
        self.reset()

    def load_high_scores(self):
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as file:
                scores = json.load(file)
            return sorted((int(score) for score in scores), reverse=True)[:5]
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return []

    def save_high_score(self):
        value = self.score // FPS
        self.high_scores = sorted(self.high_scores + [value], reverse=True)[:5]
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as file:
            json.dump(self.high_scores, file, indent=2)

    def reset(self):
        self.player = Player(WIDTH // 2, HEIGHT - LANE_H // 2)
        self.cars = []
        self.raft = Raft(RAFT_LANE * LANE_H + LANE_H // 2, WIDTH)
        self.timer = 0
        self.spawn_interval = 48
        self.speed = 3
        self.score = 0
        self.score_started = False
        self.lives = 3
        self.day_frames = 0
        self.is_night = False
        self.game_over = False
        self.won = False
        self.result_saved = False
        self.hit_effect = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
        return True

    def lose_life(self, effect_kind):
        impact_position = self.player.rect.center
        had_lives_remaining = self.lives > 1
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            self.hit_effect = None
            return
        if had_lives_remaining:
            self.hit_effect = {"kind": effect_kind, "position": impact_position, "frame": 0}
        self.player.rect.center = (WIDTH // 2, HEIGHT - LANE_H // 2)
        self.player.move_cooldown = 20

    def update(self):
        if self.game_over or self.won:
            if not self.result_saved:
                self.save_high_score()
                self.result_saved = True
            return
        if self.hit_effect:
            self.hit_effect["frame"] += 1
            if self.hit_effect["frame"] >= 20:
                self.hit_effect = None
        keys = pygame.key.get_pressed()
        old_center = self.player.rect.center
        old_lane = min(LANES - 1, max(0, old_center[1] // LANE_H))
        self.player.move(keys, 0, WIDTH, HEIGHT)
        new_lane = min(LANES - 1, max(0, self.player.rect.centery // LANE_H))
        if old_lane == LANES - 1 and new_lane < LANES - 1:
            self.score_started = True
        if self.player.rect.centery <= LANE_H // 2:
            # Reaching the far safe bank completes the crossing immediately.
            self.won = True
            return

        # Lane 3 is water: the player must land on the moving raft and is carried by it.
        self.raft.update()
        if new_lane == RAFT_LANE:
            if self.player.rect.colliderect(self.raft.rect):
                if old_lane == RAFT_LANE:
                    self.player.rect.x += round(self.raft.speed * self.raft.direction)
                if self.player.rect.left < 0 or self.player.rect.right > WIDTH:
                    self.lose_life("splash")
            elif old_lane != RAFT_LANE or self.player.move_cooldown == 10:
                self.lose_life("splash")

        self.timer += 1
        self.day_frames += 1
        if self.day_frames >= 30 * FPS:
            self.day_frames = 0
            self.is_night = not self.is_night
        if self.timer >= self.spawn_interval:
            lane = random.choice([i for i in range(1, LANES - 1) if i != RAFT_LANE])
            self.cars.append(make_car(lane, WIDTH, self.speed))
            self.timer = 0
            self.spawn_interval = max(25, self.spawn_interval - 0.15)
        for car in self.cars:
            car.night = self.is_night
            car.update()
            if car.rect.colliderect(self.player.rect):
                self.lose_life("explosion")
                break
        self.cars = [car for car in self.cars if not car.off_screen(WIDTH)]
        if self.score_started:
            self.score += 1
            if self.score % (5 * FPS) == 0:
                self.speed = min(9, self.speed + 0.4)

    def draw(self):
        grass = (28, 55, 80) if self.is_night else (77, 135, 78)
        road = (32, 37, 48) if self.is_night else ROAD
        self.screen.fill(grass)
        for lane in range(LANES):
            top = lane * LANE_H
            pygame.draw.rect(self.screen, road, pygame.Rect(0, top, WIDTH, LANE_H))
            if lane not in (0, LANES - 1):
                pygame.draw.line(self.screen, (205, 202, 175), (0, top), (WIDTH, top), 2)
            if lane != RAFT_LANE:
                for x in range(20, WIDTH, 90):
                    pygame.draw.rect(self.screen, (220, 195, 90), pygame.Rect(x, top + LANE_H // 2 - 2, 42, 4))
        pygame.draw.rect(self.screen, grass, pygame.Rect(0, HEIGHT - LANE_H, WIDTH, LANE_H))
        pygame.draw.rect(self.screen, grass, pygame.Rect(0, 0, WIDTH, LANE_H))
        for x in range(20, WIDTH, 90):
            pygame.draw.rect(self.screen, (220, 195, 90), pygame.Rect(x, LANE_H // 2 - 2, 42, 4))
        # Water lane and raft are drawn above road stripes.
        water_y = RAFT_LANE * LANE_H
        pygame.draw.rect(self.screen, (35, 105, 145) if not self.is_night else (20, 58, 95),
                         pygame.Rect(0, water_y, WIDTH, LANE_H))
        self.raft.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)
        self.player.draw(self.screen)
        self._draw_hit_effect()
        hud = pygame.Surface((WIDTH, 32), pygame.SRCALPHA)
        hud.fill((15, 18, 20, 220))
        self.screen.blit(hud, (0, 0))
        phase = "NIGHT" if self.is_night else "DAY"
        label = self.font.render(
            f"Score: {self.score // FPS}  Lives: {self.lives}  {phase}  W/S: hop  A/D: move  R: restart",
            True, (245, 245, 235))
        self.screen.blit(label, (8, 7))
        scores = "Top 5: " + (", ".join(map(str, self.high_scores)) if self.high_scores else "—")
        self.screen.blit(self.font.render(scores, True, (245, 245, 235)), (WIDTH - 230, 38))
        if self.game_over:
            self._msg("GAME OVER", (235, 75, 75))
        if self.won:
            self._msg("YOU MADE IT!", (100, 240, 120))
        pygame.display.flip()

    def _draw_hit_effect(self):
        if not self.hit_effect:
            return
        frame = self.hit_effect["frame"]
        x, y = self.hit_effect["position"]
        progress = frame / 20
        if self.hit_effect["kind"] == "explosion":
            radius = max(2, int(25 * progress))
            pygame.draw.circle(self.screen, (255, 105, 25), (x, y), radius)
            pygame.draw.circle(self.screen, (255, 220, 75), (x, y), max(2, radius // 2))
            for angle in range(0, 360, 60):
                radians = math.radians(angle)
                particle = (int(x + math.cos(radians) * radius * 1.4),
                            int(y + math.sin(radians) * radius * 1.4))
                pygame.draw.circle(self.screen, (255, 175, 45), particle, max(2, 5 - frame // 5))
        else:
            radius = max(2, int(24 * progress))
            pygame.draw.circle(self.screen, (115, 220, 255), (x, y), radius, width=3)
            pygame.draw.circle(self.screen, (65, 170, 230), (x, y), max(2, radius // 2))
            for offset in (-14, -7, 7, 14):
                drop_x = x + offset
                drop_y = y - int(12 * progress)
                pygame.draw.circle(self.screen, (160, 235, 255), (drop_x, drop_y), max(2, 5 - frame // 6))

    def _msg(self, text, color):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 155))
        self.screen.blit(overlay, (0, 0))
        message = self.big_font.render(text, True, color)
        sub = self.font.render("Press R to Restart", True, (230, 230, 230))
        self.screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 42))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 18))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
