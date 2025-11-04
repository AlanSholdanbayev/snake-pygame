#!/usr/bin/env python3
"""Простая реализация Snake на pygame.

Запуск:
	python3 main.py

Управление:
	Стрелки или WASD — движение
	R — перезапуск после Game Over
	Q или ESC — выйти

"""
import random
import sys

try:
	import pygame
except Exception:
	print("Не удалось импортировать pygame. Установите зависимости из requirements.txt:")
	print("    pip install -r requirements.txt")
	raise


# Настройки
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT
FPS = 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
GREEN = (30, 200, 30)
GREY = (40, 40, 40)


def random_food_position(snake):
	"""Вернуть случайную позицию для еды, не совпадающую со змейкой."""
	while True:
		pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
		if pos not in snake:
			return pos


class SnakeGame:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Snake — pygame")
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont(None, 28)
		self.large_font = pygame.font.SysFont(None, 48)
		self.reset()

	def reset(self):
		mid = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
		self.snake = [mid, (mid[0] - 1, mid[1]), (mid[0] - 2, mid[1])]
		self.direction = (1, 0)  # вправо
		self.grow = False
		self.food = random_food_position(self.snake)
		self.score = 0
		self.game_over = False

	def draw_cell(self, pos, color):
		x, y = pos
		rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
		pygame.draw.rect(self.screen, color, rect)

	def handle_event(self, event):
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key in (pygame.K_q, pygame.K_ESCAPE):
				pygame.quit()
				sys.exit()
			if not self.game_over:
				# направление (dx, dy)
				if event.key in (pygame.K_UP, pygame.K_w):
					self.try_change_direction((0, -1))
				elif event.key in (pygame.K_DOWN, pygame.K_s):
					self.try_change_direction((0, 1))
				elif event.key in (pygame.K_LEFT, pygame.K_a):
					self.try_change_direction((-1, 0))
				elif event.key in (pygame.K_RIGHT, pygame.K_d):
					self.try_change_direction((1, 0))
			else:
				if event.key == pygame.K_r:
					self.reset()

	def try_change_direction(self, new_dir):
		# нельзя повернуть в точности в противоположную сторону
		if (new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]):
			return
		self.direction = new_dir

	def update(self):
		if self.game_over:
			return

		head = self.snake[0]
		new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

		# столкновение со стеной — конец
		if (
			new_head[0] < 0
			or new_head[0] >= GRID_WIDTH
			or new_head[1] < 0
			or new_head[1] >= GRID_HEIGHT
		):
			self.game_over = True
			return

		# столкновение с самим собой
		if new_head in self.snake:
			self.game_over = True
			return

		# передвигаем змейку
		self.snake.insert(0, new_head)
		if new_head == self.food:
			self.score += 1
			self.food = random_food_position(self.snake)
			# при поедании — не удаляем хвост (растём)
		else:
			self.snake.pop()

	def draw_grid(self):
		for x in range(0, SCREEN_WIDTH, GRID_SIZE):
			pygame.draw.line(self.screen, GREY, (x, 0), (x, SCREEN_HEIGHT))
		for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
			pygame.draw.line(self.screen, GREY, (0, y), (SCREEN_WIDTH, y))

	def render(self):
		self.screen.fill(BLACK)
		# сетка (опционально)
		self.draw_grid()

		# еда
		self.draw_cell(self.food, RED)

		# змейка
		for i, seg in enumerate(self.snake):
			color = GREEN if i == 0 else (0, 160, 0)
			self.draw_cell(seg, color)

		# счёт
		score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
		self.screen.blit(score_surf, (8, 8))

		if self.game_over:
			overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
			overlay.set_alpha(180)
			overlay.fill((10, 10, 10))
			self.screen.blit(overlay, (0, 0))

			go_text = self.large_font.render("Game Over", True, WHITE)
			go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
			self.screen.blit(go_text, go_rect)

			info = self.font.render("Press R to restart or Q/ESC to quit", True, WHITE)
			info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
			self.screen.blit(info, info_rect)

		pygame.display.flip()

	def run(self):
		while True:
			for event in pygame.event.get():
				self.handle_event(event)

			self.update()
			self.render()
			self.clock.tick(FPS)


def main():
	game = SnakeGame()
	game.run()


if __name__ == "__main__":
	main()

