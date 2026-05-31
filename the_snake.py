from random import choice, randint

import pygame


pygame.init()

# Размеры экрана.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Размер клетки.
GRID_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POSITION = (
    (GRID_WIDTH // 2) * GRID_SIZE,
    (GRID_HEIGHT // 2) * GRID_SIZE
)

# Цвета.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

# Направления.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Все клетки поля.
ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

# Экран.
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

clock = pygame.time.Clock()

# Изменение направления.
DIRECTION_MAP = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,

    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,

    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,

    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        """Инициализировать объект."""
        self.position = position
        self.body_color = body_color

    @staticmethod
    def draw_cell(position, color):
        """Нарисовать одну клетку."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовать объект."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_cells=None):
        """Создать яблоко."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_cells or [])

    def randomize_position(self, occupied_cells):
        """Выбрать свободную клетку."""
        free_cells = tuple(
            ALL_CELLS - set(occupied_cells)
        )
        self.position = choice(free_cells)

    def draw(self):
        """Отрисовать яблоко."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Создать змейку."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        self.position = CENTER_POSITION

        self.length = 1

        self.positions = [self.position]

        self.direction = RIGHT

        self.next_direction = None

        self.last = None

    def get_head_position(self):
        """Вернуть координаты головы."""
        return self.positions[0]

    def update_direction(self):
        """Применить новое направление."""
        if self.next_direction is not None:
            self.direction = self.next_direction

    def move(self):
        """Передвинуть змейку."""
        head_x, head_y = self.get_head_position()

        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def cut_tail(self):
        """Оставить только голову после самоукуса."""
        self.positions = [self.get_head_position()]
        self.length = 1

    def draw(self):
        """Отрисовать изменения змейки."""
        self.draw_cell(
            self.get_head_position(),
            self.body_color
        )

        if self.last is not None:
            self.draw_cell(
                self.last,
                BOARD_BACKGROUND_COLOR
            )


def handle_keys(game_object):
    """Обработать нажатия клавиш."""
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            game_object.next_direction = DIRECTION_MAP.get(
                (event.key, game_object.direction),
                game_object.next_direction
            )


def main():
    """Основной игровой цикл."""
    screen.fill(BOARD_BACKGROUND_COLOR)

    snake = Snake()

    apple = Apple(snake.positions)

    record = 1

    while True:

        clock.tick(20)

        handle_keys(snake)

        snake.update_direction()

        snake.move()

        head = snake.get_head_position()

        # Поедание яблока.
        if head == apple.position:

            snake.length += 1

            record = max(record, snake.length)

            apple.randomize_position(
                snake.positions
            )

        # Самоукус.
        if (
            snake.length > 4
            and head in snake.positions[1:]
        ):
            snake.cut_tail()

        apple.draw()

        snake.draw()

        pygame.display.set_caption(
            f'Изгиб Питона | Рекорд: {record}'
        )

        pygame.display.update()


if __name__ == "__main__":
    main()
