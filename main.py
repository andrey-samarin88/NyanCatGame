import pygame
import random
import os

# ИНИЦИАЛИЗАЦИЯ
pygame.init()  # Инициализация pygame
pygame.font.init()  # Инициализация шрифтов
pygame.mixer.init()  # Инициализация звуков

# КОНСТАНТЫ
# Настройки окна
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nyan Cat")
FONT = "Arial"

# Цвета (RGB)
DARK_BLUE = (10, 10, 40)  # Фон
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
        frame = pygame.image.load(f"images/cat/{i}.png")
        frame = pygame.transform.scale(frame, (frame.get_width() // 6, frame.get_height() // 6))
        nyan_frames.append(frame)
    except:
        print(f"Не удалось загрузить кадр {i}.png")

# Заглушка если кадры не загрузились
if not nyan_frames:
    dummy_frame = pygame.Surface((100, 64))
    dummy_frame.fill(PINK)
    nyan_frames = [dummy_frame] * 5

# Загрузка изображений еды
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

# Загрузка звуков
try:
    SOUND_EAT_GOOD = pygame.mixer.Sound('sounds/eat_good.wav')
    SOUND_EAT_BAD = pygame.mixer.Sound('sounds/eat_bad.wav')
    SOUND_HAPPINESS_STAR = pygame.mixer.Sound('sounds/happiness_star.wav')
    SOUND_GAME_OVER = pygame.mixer.Sound('sounds/game_over.mp3')
    SOUND_BG_MUSIC = pygame.mixer.Sound('sounds/background_music.mp3')

    # Настройка громкости
    SOUND_BG_MUSIC.set_volume(0.1)
    SOUND_EAT_GOOD.set_volume(0.2)
except:
    print("Не удалось загрузить некоторые звуки")


# КЛАССЫ
class Cat:
    """Класс игрового персонажа - кота"""

    def __init__(self):
        self.width = 100  # Ширина
        self.height = 64  # Высота
        self.x = 0  # Позиция по X
        self.y = HEIGHT // 2 - self.height // 2  # Позиция по Y (центр)
        self.speed = 5  # Скорость движения
        self.animation_speed = 0.2  # Скорость анимации
        self.frames = nyan_frames  # Кадры анимации
        self.current_frame = 0  # Текущий кадр
        self.image = self.frames[0]  # Текущее изображение
        self.rect = self.image.get_rect(topleft=(self.x, self.y))  # Хитбокс

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
        # Движение вверх
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 50:
            self.y -= self.speed
        # Движение вниз
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < HEIGHT - self.height:
            self.y += self.speed

        self.rect.topleft = (self.x, self.y)


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

        self.x = WIDTH + 50  # Начальная позиция за экраном
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 4 + score * 0.1  # Скорость зависит от счета
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        """Движение еды"""
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, surface):
        """Отрисовка еды"""
        surface.blit(self.image, (self.x, self.y))


class Star:
    """Класс фоновых звезд"""

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 5)
        self.size = random.randint(1, 2)

    def move(self):
        """Движение звезд"""
        self.x -= self.speed
        if self.x < 0:  # Если звезда ушла за экран
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)

    def draw(self, surface):
        """Отрисовка звезд"""
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)


class HappinessStar:
    """Класс звезд счастья"""

    def __init__(self):
        self.x = WIDTH + 50
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 10
        self.size = 15
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.spawn_time = pygame.time.get_ticks()

    def move(self):
        """Движение звезды"""
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, surface):
        """Отрисовка звезды"""
        pygame.draw.circle(surface, YELLOW, (int(self.x + self.size / 2), int(self.y + self.size / 2)), self.size)
        pygame.draw.circle(surface, WHITE, (int(self.x + self.size / 2), int(self.y + self.size / 2)), self.size // 2)


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def reset_game():
    """Сброс состояния игры"""
    global score, omnomnometr, happiness, eaten_good, food_timer, paused, high_score
    global game_over, foods, stars, happiness_stars, last_happiness_star, cat

    food_timer = 0  # Таймер появления еды
    foods = []  # Список еды на экране
    score = 10  # Счет игрока
    eaten_good = 0  # Счетчик съеденной хорошей еды
    happiness = 3  # Уровень счастья
    omnomnometr = []  # История съеденной еды
    stars = [Star() for _ in range(50)]  # Фоновые звезды
    happiness_stars = []  # Звезды счастья
    last_happiness_star = pygame.time.get_ticks()  # Время последней звезды
    paused = False  # Пауза
    game_over = False  # Конец игры
    cat = Cat()  # Создаем кота

    high_score = load_high_score()  # Загрузка рекорда

    # Запуск фоновой музыки
    try:
        SOUND_BG_MUSIC.stop()
        SOUND_BG_MUSIC.play(-1)  # -1 = бесконечный цикл
    except:
        pass


def draw_main_menu():
    """Отрисовка главного меню"""
    WIN.fill(DARK_BLUE)

    # Отрисовка фоновых звезд
    for star in stars:
        star.move()
        star.draw(WIN)

    # Шрифты для текста
    title_font = pygame.font.SysFont(FONT, 64)
    button_font = pygame.font.SysFont(FONT, 36)

    # Заголовок игры
    title = title_font.render("Nyan Cat", True, WHITE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    # Кнопка "Начать игру"
    start_text = button_font.render("НАЧАТЬ ИГРУ", True, DARK_BLUE)
    button_rect = pygame.Rect(WIDTH // 2 - 120, 300, 240, 60)
    pygame.draw.rect(WIN, YELLOW, button_rect, border_radius=12)
    WIN.blit(start_text, (button_rect.centerx - start_text.get_width() // 2,
                          button_rect.centery - start_text.get_height() // 2))

    pygame.display.update()
    return button_rect


def save_high_score(score):
    """Сохранение рекорда в файл"""
    with open("high_score.txt", "w") as f:
        f.write(str(score))


def load_high_score():
    """Загрузка рекорда из файла"""
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            return int(f.read())
    return 0


def play_sound(sound):
    """Воспроизведение звука с обработкой ошибок"""
    try:
        sound.play()
    except:
        pass


# ИНИЦИАЛИЗАЦИЯ ИГРЫ
clock = pygame.time.Clock()  # Для контроля FPS
running = True  # Флаг работы игры
menu = True  # Флаг меню

reset_game()  # Первоначальная настройка игры

# ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ
while running:
    current_time = pygame.time.get_ticks()  # Текущее время
    dt = clock.tick(60) / 1000  # Дельта времени (60 FPS)
    WIN.fill(DARK_BLUE)  # Очистка экрана

    # Обработка меню
    if menu:
        button_rect = draw_main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    menu = False
                    reset_game()
        continue

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Пауза по ESC
                paused = not paused
            elif event.key == pygame.K_SPACE and game_over:  # Рестарт по пробелу
                reset_game()

    # Режим паузы
    if paused and not game_over:
        font = pygame.font.SysFont(FONT, 60)
        pause_text = font.render("Пауза", True, YELLOW)
        instruction_text = font.render("Нажмите ESC, чтобы продолжить", True, WHITE)

        WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 40))
        WIN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.update()
        continue

    # Экран окончания игры
    if game_over:
        font1 = pygame.font.SysFont(FONT, 72)
        font2 = pygame.font.SysFont(FONT, 30)

        text = font1.render("Игра окончена!", True, RED)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 72))

        high_score_text = font2.render(f"Ваш счёт: {score} | Рекорд: {high_score}", True, YELLOW)
        WIN.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 72))

        restart_text = font2.render("Нажмите ПРОБЕЛ для перезапуска", True, WHITE)
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 50))

        pygame.display.update()
        continue

    # ОБНОВЛЕНИЕ СОСТОЯНИЯ
    keys = pygame.key.get_pressed()  # Получаем состояние клавиш

    # Обновление фоновых звезд
    for star in stars:
        star.move()
        star.draw(WIN)

    # Обновление кота
    cat.update(keys)
    cat.draw(WIN)

    # Генерация новой еды
    food_timer -= dt
    if food_timer <= 0:
        foods.append(Food())
        min_delay = max(0.2, 2 - score * 0.05)  # Уменьшаем задержку с ростом счета
        food_timer = random.uniform(min_delay, min_delay + 0.5)

    # Обработка еды
    for food in foods[:]:
        food.move()
        food.draw(WIN)

        # Проверка столкновения с котом
        if food.rect.colliderect(cat.rect):
            if food.kind == "good":
                score += 1
                omnomnometr.append(food.image)
                eaten_good += 1

                play_sound(SOUND_EAT_GOOD)

                # Бонус за каждые 10 хороших продуктов
                if eaten_good % 10 == 0:
                    score += 10
                    play_sound(SOUND_HAPPINESS_STAR)
            else:
                score -= 1
                happiness -= 1
                eaten_good = 0
                omnomnometr = []

                play_sound(SOUND_EAT_BAD)

            foods.remove(food)
        elif food.x < -50:  # Удаление еды за экраном
            foods.remove(food)

    # Удаление еды за экраном (альтернативный способ)
    foods = [food for food in foods if food.x + food.image.get_width() > 0]

    # Генерация звезд счастья
    if current_time - last_happiness_star > random.randint(20000, 30000):
        happiness_stars.append(HappinessStar())
        last_happiness_star = current_time

    # Обработка звезд счастья
    for star in happiness_stars[:]:
        star.move()
        star.draw(WIN)

        if star.rect.colliderect(cat.rect):
            happiness = min(3, happiness + 1)
            play_sound(SOUND_HAPPINESS_STAR)
            happiness_stars.remove(star)
        elif star.x < -50:
            happiness_stars.remove(star)

    # ОТРИСОВКА ИНТЕРФЕЙСА
    ui_font = pygame.font.SysFont(FONT, 28)

    # История съеденной еды
    for i, img in enumerate(omnomnometr[-10:]):
        WIN.blit(pygame.transform.scale(img, (32, 32)), (10 + i * 30, 10))

    # Счет и уровень счастья
    WIN.blit(ui_font.render(f"Счёт: {score}", True, WHITE), (WIDTH // 2 - 50, 10))
    WIN.blit(ui_font.render(f"Счастье: {happiness}", True, WHITE), (WIDTH - 150, 10))

    # Проверка условий поражения
    if (score < 1 or happiness <= 0) and not game_over:
        game_over = True

        try:
            SOUND_BG_MUSIC.stop()
        except:
            pass
        play_sound(SOUND_GAME_OVER)

        # Обновление рекорда
        if score > high_score:
            high_score = score
            save_high_score(high_score)

    pygame.display.update()  # Обновление экрана

pygame.quit()  # Корректный выход
