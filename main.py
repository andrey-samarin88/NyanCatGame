import pygame
import random
import os

# ИНИЦИАЛИЗАЦИЯ
pygame.init()  # Инициализация pygame

# КОНСТАНТЫ
WIDTH, HEIGHT = 800, 600  # Настройки окна
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем основное окно
pygame.display.set_caption("Nyan Cat")  # Заголовок окна

# Цвета (RGB)
DARK_BLUE = (10, 10 ,40)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)


nyan_frames = []
for i in range(6):
    try:
        frame = pygame.image.load(f'images/cat/{i}.png')
        frame = pygame.transform.scale(frame, (frame.get_width() // 6, frame.get_height() // 6))
        nyan_frames.append(frame)
    except:
        print(f"Не удалось загрузить кадр {i}.png")

if not nyan_frames:
    dummy_frame = pygame.Surface((100, 64))
    dummy_frame.fill(PINK)
    nyan_frames = [dummy_frame] * 5


GOOD_IMAGES = []
BAD_IMAGES = []


# КЛАССЫ
class Cat:
    """Класс игрового персонажа - кота"""
    def __init__(self):
        self.width = 100  # Ширина
        self.height = 64  # Высота
        self.x = 0  # Позиция по х
        self.y = HEIGHT // 2 - self.height // 2  # Позиция по у (центр)
        self.speed = 5  # Скорость движения
        # self.color = PINK  # Цвет
        # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Хитбокс
        self.animation_speed = 0.2  # Скорость анимации
        self.frames = nyan_frames  # Кадры анимации
        self.current_frame = 0  # Текущий кадр
        self.image = self.frames[0]  # Текущее изображение
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def animate(self):
        """Анимация кота"""
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect(topleft=(self.x, self.rect.y))
        return self.image


    def draw(self, surface):
        """Отрисовка кота"""
        #pygame.draw.rect(surface, self.color, self. rect)  #  Нарисовать прямоугольник на WIN
        surface.blit(self.animate(), (self.rect.x, self.rect.y))


    def update(self, keys):
        """Обновление позиции кота"""
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 50:
            self.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < HEIGHT - self.height:
            self.y +=self.speed
        self.rect.topleft = (self.x, self.y)  # Обновляем положение прямоугольника


# ИНИЦИАЛИЗАЦИЯ ИГРЫ
clock = pygame.time.Clock()  # # Для контроля FPS
running = True
cat = Cat()

# ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ
while running:
    current_time = pygame.time.get_ticks()  # Получаем текущее время с момента запуска игры
    dt = clock.tick(60) / 1000  # Задаём частоту кадров: 60 FPS

    WIN.fill(DARK_BLUE)  # Заливаем фон тёмно-синим цветом (перерисовываем экран каждый кадр).

    for event in pygame.event.get():  # Получаем все события (например, нажатие клавиш, закрытие окна)
        if event.type == pygame.QUIT:  # Если закрыли окно
            running = False

    keys = pygame.key.get_pressed()  # Получаем текущее состояние всех клавиш клавиатуры
    cat.update(keys)

    cat.draw(WIN)

    pygame.display.update()  # Обновляем экран (отображаем все изменения).

pygame.quit()  # Закрываем Pygame, освобождаем ресурсы