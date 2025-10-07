import pygame
import random
import os

# ИНИЦИАЛИЗАЦИЯ
pygame.init()  # Инициализация pygame

# КОНСТАНТЫ
# Настройки окна
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем основное окно
pygame.display.set_caption("Nyan Cat")  # Заголовок окна

# Цвета (RGB)
DARK_BLUE = (10, 10 ,40)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)


# ЗАГРУЗКА РЕСУРСОВ
# Кадры анимации Нян Кэта
nyan_frames = []
for i in range(6):
    try:
        frame = pygame.image.load(f'images/cat/{i}.png')
        frame = pygame.transform.scale(frame, (frame.get_width() // 6, frame.get_height() // 6))
        nyan_frames.append(frame)
    except:
        print(f"Не удалось загрузить кадр {i}.png")

# Заглушка если кадры не загрузились
if not nyan_frames:
    dummy_frame = pygame.Surface((100, 64))
    dummy_frame.fill(PINK)
    nyan_frames = [dummy_frame] * 5

# Изображения еды
GOOD_IMAGES = []
BAD_IMAGES = []

try:
    for filename in os.listdir("images/good"):
        img = pygame.image.load(os.path.join("images/good", filename)).convert_alpha()
        img = pygame.transform.scale(img, (48, 48))
        GOOD_IMAGES.append(img)

    for filename in os.listdir("images/bad"):
        img = pygame.image.load(os.path.join("images/bad", filename)).convert_alpha()
        img = pygame.transform.scale(img, (48, 48))
        BAD_IMAGES.append(img)
except:
    print("Не удалось загрузить изображения еды")


# КЛАССЫ
class Cat:
    """Класс игрового персонажа - кота"""
    def __init__(self):
        self.width = 100  # Ширина
        self.height = 64  # Высота
        self.x = 0  # Позиция по х
        self.y = HEIGHT // 2 - self.height // 2  # Позиция по у (центр)
        self.speed = 5  # Скорость движения
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
        surface.blit(self.animate(), (self.rect.x, self.rect.y))

    def update(self, keys):
        """Обновление позиции кота"""
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 50:
            self.y -= self.speed

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < HEIGHT - self.height:
            self.y +=self.speed

        self.rect.topleft = (self.x, self.y)  # Обновляем положение прямоугольника


class Food:
    """Класс еды (хорошей и плохой)"""
    def __init__(self):
        self.kind = random.choice(["good", "bad"])  # Тип еды

        # Выбор изображения в зависимости от типа
        if self.kind == "good" and GOOD_IMAGES:
            self.image = random.choice(GOOD_IMAGES)
        elif self.kind == "bad" and BAD_IMAGES:
            self.image = random.choice(BAD_IMAGES)
        else:
            self.image = pygame.Surface((48, 48))
            self.image.fill(GREEN if self.kind == "good" else RED)

        self.x = WIDTH + 50  # За пределами правого края экрана
        self.y = random.randint(50, HEIGHT - 50)  #  С отступом в 50 пикселей от верха и низа
        self.speed = 4 + score * 0.1  # Скорость изменяется в зависимости от счёта
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        """Движение еды"""
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, surface):
        """Отрисовка еды"""
        surface.blit(self.image, (self.x, self.y))


# ИНИЦИАЛИЗАЦИЯ ИГРЫ
clock = pygame.time.Clock()  # Для контроля FPS
running = True  # Флаг работы игры
cat = Cat()  # Создаем кота
food_timer = 0  # Таймер появления еды
foods = []  # Список еды на экране
score = 10  # Счет игрока
eaten_good = 0  # Количество подряд съеденной хорошей еды
happiness = 3  # Настроение» кота
omnomnometr = []  # Список изображений хорошей еды

# ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ
while running:
    current_time = pygame.time.get_ticks()  # Получаем текущее время с момента запуска игры
    dt = clock.tick(60) / 1000  # Задаём частоту кадров: 60 FPS

    WIN.fill(DARK_BLUE)  # Заливаем фон тёмно-синим цветом (перерисовываем экран каждый кадр).

    # Обработка событий
    for event in pygame.event.get():  # Получаем все события (например, нажатие клавиш, закрытие окна)
        if event.type == pygame.QUIT:  # Если закрыли окно
            running = False

    keys = pygame.key.get_pressed()  # Получаем текущее состояние всех клавиш клавиатуры

    # Обновление кота
    cat.update(keys)
    cat.draw(WIN)  # Рисуем кота

    # Обновление еды
    food_timer -= dt
    if food_timer <= 0:
        foods.append(Food())
        min_delay = max(0.2, 2 - score * 0.05)
        food_timer = random.uniform(min_delay, min_delay + 0.5)

    for food in foods[:]:  #  Проходим по каждому объекту в КОПИИ списка еды.
        food.move()
        food.draw(WIN)

        # Обработка столкновений кота с едой
        if food.rect.colliderect(cat.rect):
            if food.kind == "good":
                score += 1
                omnomnometr.append(food.image)
                eaten_good += 1
                # Бонус за каждые 10 хороших продуктов
                if eaten_good % 10 == 0:
                    score += 10
            else:
                score -= 1
                happiness -= 1
                eaten_good = 0
                omnomnometr = []

            foods.remove(food)
        elif food.x < -50:  # Удаление еды за экраном
            foods.remove(food)

    pygame.display.update()  # Обновляем экран (отображаем все изменения).

pygame.quit()  # Закрываем Pygame, освобождаем ресурсы
