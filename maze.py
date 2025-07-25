"""
Модуль для реализации класса Maze.
Генерация лабиринта с использованием алгоритма Прима.
Решение лабиринта с использованием алгоритма Best First Search.
"""
import random
from queue import PriorityQueue
from typing import List, Tuple
from PIL import Image, ImageDraw


class Maze:
    """
    Класс для генерации, решения и манипулирования лабиринтами.

    Args:
        rows (int): Количество строк в лабиринте.
        cols (int): Количество столбцов в лабиринте.

    Attributes:
        rows_fixed (int): Фиксированное количество строк в лабиринте (с учетом стен).
        cols_fixed (int): Фиксированное количество столбцов в лабиринте (с учетом стен).
        seed (int): Семя для генерации лабиринта.
        maze (List[List[int]]): Двумерный список, представляющий структуру лабиринта.
        path (List[List[int]]): Путь, найденный в процессе решения лабиринта.
    """

    def __init__(self, rows: int = 1, cols: int = 1, seed: int = 63) -> None:  #42
        """
        Инициализация объекта Maze.

        Args:
            rows (int): Количество строк в лабиринте.
            cols (int): Количество столбцов в лабиринте.

        Returns:
            None
        """
        self.rows_fixed = rows + 2
        self.cols_fixed = cols + 2
        self.random_seed = seed
        self.maze = None
        self.path = None

    def generate_maze(self) -> None:
        """
        Генерация лабиринта с использованием алгоритма Прима.

        Returns:
            None
        """

        def get_walls_around(maze: List[List[int]], x: int, y: int) -> List[Tuple[int, int]]:
            """
            Вспомогательная функция для получения всех съемных стен вокруг заданной ячейки.

            Args:
                maze (List[List[int]]): Текущий лабиринт.
                x (int): Координата x ячейки.
                y (int): Координата y ячейки.

            Returns:
                List[Tuple[int, int]]: Список координат съемных стен вокруг ячейки.
            """
            removable_wall = 2  # Съемная стена, которую можно удалить
            if not ((0 <= x < len(maze)) and (0 <= y < len(maze[0]))):
                # Если координаты вне допустимого диапазона, вызываем исключение
                raise IndexError
            around = []
            # Проверяем все соседние клетки вокруг текущей ячейки
            for i in range(max(x - 1, 0), min(x + 2, len(maze))):
                for j in range(max(y - 1, 0), min(y + 2, len(maze[i]))):
                    if maze[i][j] == removable_wall:
                        around.append((i, j))  # Добавляем координаты съемной стены
            return around

        # Устанавливаем фиксированное начальное значение для генератора случайных чисел
        random.seed(self.random_seed)

        # Определяем константы для статусов клеток
        non_visited_cell = 0  # Не посещенная клетка
        visited_cell = -1  # Посещенная клетка
        removable_wall = 2  # Съемная стена
        non_removable_wall = 1  # Несъемная стена

        # Инициализация пустого лабиринта
        # Каждая ячейка с четными координатами — несъемная стена,
        # каждая ячейка с нечетными координатами — потенциальный проход
        self.maze = [[int(not (((i % 2) * (j % 2)) == 1)) for i in range(self.cols_fixed)]
                     for j in range(self.rows_fixed)]

        # Проверяем, что размеры лабиринта больше минимальных значений
        if self.rows_fixed < 2 or self.cols_fixed < 2:
            # Если размеры слишком малы (меньше 2x2), прекращаем генерацию
            return

        # Размещаем съемные стены внутри лабиринта
        for x in range(1, self.rows_fixed - 1):
            for y in range(1, self.cols_fixed - 1):
                # Проверяем, что текущая ячейка - стена и не находится на краю
                if self.maze[x][y] and ((x % 2) == 1 or (y % 2) == 1) and not (((x % 2) * (y % 2)) == 1):
                    # Если условия выполнены, меняем значение ячейки на съемную стену
                    self.maze[x][y] = removable_wall

        # Стек для хранения возможных стен, которые можно удалить
        walls_stack = []

        # Начальная ячейка (в этой ячейке уже будет путь)
        self.maze[1][1] = visited_cell

        # Добавляем стены вокруг начальной ячейки в стек
        for w in get_walls_around(self.maze, 1, 1):
            walls_stack.append(w)

        # Основной цикл алгоритма Прима
        while walls_stack:
            # Выбираем случайную стену из стека
            i = random.randint(0, len(walls_stack) - 1)
            wall = walls_stack.pop(i)  # Удаляем выбранную стену из стека
            # ([(6,2),(5,3),(4,7)]    -   pop 2
            # ([(6,2),(5,3)]

            # Разбиваем координаты стены на x и y
            x, y = wall

            # Переменная для подсчета количества непосещенных ячеек вокруг стены
            unvisited_around_wall = 0

            # Проходим по клеткам вокруг стены (в пределах 3x3)
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    # Если ячейка непосещена
                    if self.maze[i][j] == non_visited_cell:
                        unvisited_around_wall += 1  # Увеличиваем счетчик непосещенных ячеек
                        self.maze[i][j] = visited_cell  # Помечаем ячейку как посещенную

                        # Добавляем новые стены вокруг только что посещенной ячейки в стек
                        for w in get_walls_around(self.maze, i, j):
                            walls_stack.append(w)

            # Если вокруг стены были непосещенные ячейки, то эта стена становится проходом
            if unvisited_around_wall:
                self.maze[x][y] = visited_cell

        # Очистка лабиринта от временных меток, установка несъемных стен и возврат
        for x in range(self.rows_fixed):
            for y in range(self.cols_fixed):
                if self.maze[x][y] == -1 or self.maze[x][y] == 3 or self.maze[x][y] == 0:
                    self.maze[x][y] = non_visited_cell
                else:
                    self.maze[x][y] = non_removable_wall
        return

    def print_maze(self) -> None:
        """
        Вывод лабиринта в консоль.

        Returns:
            None
        """
        for row in self.maze:
            for elem in row:
                if elem:
                    print("[]", end="")
                else:
                    print("  ", end="")
            print()
        print()

    def print_solved_maze(self) -> None:
        """
        Вывод решенного лабиринта в консоль.

        Returns:
            None
        """
        for row_idx, row in enumerate(self.maze):
            for col_idx, elem in enumerate(row):
                pos = [row_idx, col_idx]
                if pos in self.path:
                    print("🐾", end="")
                elif elem:
                    print("[]", end="")
                else:
                    print("  ", end="")
            print()

    def solve_maze(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """
        Решение лабиринта от заданной начальной позиции к конечной.

        Args:
            start (Tuple[int, int]): Начальная позиция в виде кортежа (строка, столбец).
            end (Tuple[int, int]): Конечная позиция в виде кортежа (строка, столбец).

        Returns:
            None
        """
        # Получение размеров лабиринта
        rows, cols = len(self.maze), len(self.maze[0])

        # Проверка, что стартовая и конечная позиции в пределах лабиринта
        if not (0 <= start[0] < rows and 0 <= start[1] < cols) or not (0 <= end[0] < rows and 0 <= end[1] < cols):
            raise ValueError("Недопустимая начальная или конечная позиция")

        # Множество для отслеживания посещенных точек в лабиринте
        visited = set()

        # Приоритетная очередь для управления порядком обхода точек
        priority_queue = PriorityQueue()

        # Добавление стартовой точки в очередь с приоритетом, начальный путь - пустой список
        priority_queue.put((0, start, []))

        # Цикл продолжается, пока очередь не станет пустой
        while not priority_queue.empty():
            # Извлечение элемента из очереди с наименьшим приоритетом
            _, current_pos, path = priority_queue.get()

            # Если текущая позиция совпадает с конечной, сохранение найденного пути
            if current_pos == end:
                self.path = [list(p) for p in path] + [list(end)]

            # Если текущая позиция уже посещена, пропуск этой итерации цикла
            if current_pos in visited:
                continue

            # Добавление текущей позиции в список посещенных
            visited.add(current_pos)

            # Извлечение координат текущей позиции
            row, col = current_pos

            # Определение соседей текущей позиции
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

            # Обход соседей текущей позиции
            for neighbor in neighbors:
                n_row, n_col = neighbor

                # Проверка, что сосед находится в пределах лабиринта и не был посещен
                if rows > n_row >= 0 == self.maze[n_row][n_col] and 0 <= n_col < cols and neighbor not in visited:
                    # Вычисление приоритета для соседа с использованием эвристики
                    priority = abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])

                    # Добавление соседа в очередь с приоритетом с обновленным путем
                    priority_queue.put((priority, neighbor, path + [current_pos]))

    def import_maze_from_file(self, filename: str) -> None:
        """
        Импорт лабиринта из текстового файла.

        Args:
            filename (str): Имя текстового файла, содержащего лабиринт.

        Returns:
            None
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                maze_data = [list(map(int, line.strip())) for line in file.readlines()]
                self.maze = maze_data
                self.rows_fixed = len(maze_data)
                self.cols_fixed = len(maze_data[0])

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    def import_maze_from_image(self, filename: str) -> None:
        """
        Импорт лабиринта из изображения.

        Args:
            filename (str): Имя изображения, содержащего лабиринт.

        Returns:
            None
        """
        # Определение цветов для распознавания стен и проходов
        wall_color = (0, 0, 0)  # Черный цвет представляет стены
        path_color = (255, 255, 255)  # Белый цвет представляет проходы

        try:
            # Открываем изображение с помощью библиотеки PIL
            image = Image.open(filename)
            width, height = image.size  # Получаем размеры изображения

            # Список для хранения структуры лабиринта
            maze_data = []

            # Проходим по пикселям изображения с шагом 21 пиксель
            # Этот шаг используется для соответствия размеру клеток лабиринта
            for y in range(0, height, 21):  # Перебираем строки
                row = []  # Временный список для текущей строки
                for x in range(0, width, 21):  # Перебираем столбцы
                    # Получаем цвет текущего пикселя
                    pixel = image.getpixel((x, y))

                    # Определяем тип клетки на основе цвета
                    if pixel == wall_color:
                        row.append(1)  # 1 означает стену
                    elif pixel == path_color:
                        row.append(0)  # 0 означает проход
                    else:
                        # Если пиксель неизвестного цвета, выбрасываем исключение
                        raise ValueError("Неизвестный цвет пикселя на изображении")
                # Добавляем строку в структуру лабиринта
                maze_data.append(row)

            # Сохраняем данные лабиринта в экземпляре класса
            self.maze = maze_data
            self.rows_fixed = len(maze_data)  # Количество строк лабиринта
            self.cols_fixed = len(maze_data[0])  # Количество столбцов лабиринта

        except FileNotFoundError:
            # Если файл не найден, выводим сообщение об ошибке
            print(f"Файл {filename} не найден.")

    def export_maze_to_file(self, filename: str) -> None:
        """
        Экспорт лабиринта в текстовый файл.

        Args:
            filename (str): Имя текстового файла для сохранения лабиринта.

        Returns:
            None
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for row in self.maze:
                file.write(''.join(map(str, row)) + '\n')

    def create_maze_png(self, maze: List[List[int]]) -> Image.Image:
        """
        Создание изображения лабиринта с отмеченным путем, если он существует.

        Args:
            maze (List[List[int]]): Структура лабиринта в виде двумерного списка,
                                    где 1 - стена, 0 - проход.

        Returns:
            Image.Image: Изображение лабиринта в формате PIL.
        """
        # Размер одной клетки в пикселях
        cell_size = 20

        # Цвета для изображения
        wall_color = (0, 0, 0)  # Черный цвет для стен
        path_color = (255, 255, 255)  # Белый цвет для проходов
        find_color = (0, 255, 0)  # Зеленый цвет для пути

        # Рассчитываем размер изображения в зависимости от размеров лабиринта
        width = self.cols_fixed * cell_size  # Общая ширина изображения
        height = self.rows_fixed * cell_size  # Общая высота изображения

        # Создаем новое изображение с белым фоном (проходы)
        img = Image.new('RGB', (width, height), path_color)
        draw = ImageDraw.Draw(img)  # Создаем объект для рисования

        # Отрисовка стен лабиринта
        for i in range(self.rows_fixed):  # Проходим по строкам лабиринта
            for j in range(self.cols_fixed):  # Проходим по столбцам лабиринта
                if maze[i][j] == 1:  # Если текущая клетка - стена
                    # Рисуем черный прямоугольник для стены
                    draw.rectangle(
                        ((j * cell_size, i * cell_size),  # Верхний левый угол
                         ((j + 1) * cell_size, (i + 1) * cell_size)),  # Нижний правый угол
                        fill=wall_color
                    )

        # Если путь найден (self.path не пуст), то рисуем его
        if self.path:
            for position in self.path:  # Проходим по координатам пути
                # Рисуем зеленый прямоугольник для каждой клетки пути
                draw.rectangle(
                    ((position[1] * cell_size, position[0] * cell_size),  # Верхний левый угол
                     ((position[1] + 1) * cell_size, (position[0] + 1) * cell_size)),  # Нижний правый угол
                    fill=find_color
                )

        # Возвращаем сгенерированное изображение
        return img

