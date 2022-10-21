"""
ПЗ 2
Выполнили студенты группы М3О-421Б-19
Димухаметов Данил
Нуштаева Юлия
Петина Екатерина
"""

# ---------------------Импорт необходимых модулей---------------------
import pygame
import os
import random
from random import uniform
from enum import Enum, auto


pygame.init()

# Global Constants
# ---------------------Определение размера экрана---------------------
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ------------------------ Определение текстур------------------------
# RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
#            pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
# JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
# DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
#            pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
#
# SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
#                 pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
#                 pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
# LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
#                 pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
#                 pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

RUNNING = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
           pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png"))]

DUCKING = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
           pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class DinoState(Enum):
    duck = auto()
    run = auto()
    jump = auto()


# ------------------------Класс динозаврика------------------------
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    # Конструктор класса
    # Определяем начальное состояние динозавра и передаём полям класса глобальные переменные
    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_state: DinoState
        self.dino_state = DinoState.run

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput) -> None:
        """
        Функция обновления состояния динозавра
        :param userInput: Вход с клавиатуры
        :return:
        """
        if self.dino_state == DinoState.duck:
            self.duck()
        if self.dino_state == DinoState.run:
            self.run()
        if self.dino_state == DinoState.jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        # Установка состояния динозавтра в зависимости от нажатой пользователем клавиши
        if userInput[pygame.K_UP] and not self.dino_state == DinoState.jump:
            self.dino_state = DinoState.jump
        elif userInput[pygame.K_DOWN] and not self.dino_state == DinoState.jump:
            self.dino_state = DinoState.duck
        elif not (self.dino_state == DinoState.jump or userInput[pygame.K_DOWN]):
            self.dino_state = DinoState.run

    # Функции отображения динозаврика в зависимости от нажатой кнопки
    # Ползанье
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    # Бег
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    # Прыжок
    def jump(self):
        self.image = self.jump_img
        if self.dino_state == DinoState.jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_state = DinoState.run
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# ------------Класс облака------------
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

# ------------Родительский класс препятствия------------
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self._type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

# Интерфейс для определения типа кактуса
class IRandomType():
    def get(self):
        return random.randint(0, 2)

# ------------Класс маленького кактуса------------
class SmallCactus(Obstacle, IRandomType):
    def __init__(self, image):
        #self.type = random.randint(0, 2)
        self.type = super().get()
        super().__init__(image, self.type)
        self.rect.y = 325

# ------------Класс большого кактуса------------
class LargeCactus(Obstacle, IRandomType):
    def __init__(self, image):
        self.type = super().get()
        super().__init__(image, self.type)
        self.rect.y = 300

# ------------Класс птицы------------
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        """
        Функция подсчёта общего счёта
        :return:
        """
        global points, game_speed
        points += 1
        if points % 100 == 0:
            if game_speed > 25:
                game_speed += random.randint(-5, 5)
            else:
                game_speed += random.randint(0, 5)

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        """
        Функция отрисовки фона
        :return:
        """
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_DOWN]:
            SCREEN.fill((uniform(0, 255), uniform(0, 255), uniform(0, 255)))
        else:
            SCREEN.fill((255, 255, 255))

        player.draw(SCREEN)
        player.update(userInput)

        # Создание препятствий
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
        # Отрисовка препятствий
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start or write proper TT", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
