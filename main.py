"""
CLI-модуль для взаимодействия с классом Maze.
Генерация лабиринта, его решение, импорт лабиринта из файла|изображения(png), экспорт лабиринта в файл|изображение.
"""
import argparse

from maze import Maze

#python main.py --import_file maze.png --filename ahaha --text_output

def main():
    parser = argparse.ArgumentParser(description="Генератор и решатель лабиринтов CLI")
    parser.add_argument("--size", type=str, help="Размер лабиринта в формате 'строки,столбцы'")
    parser.add_argument("--seed", type=str, help="Выбор блока для генерации лабиринта")
    parser.add_argument("--solve_indecies", type=str,
                        help="Индексы для решения лабиринта в формате "
                             "'начало_строка,начало_столбец,конец_строка,конец_столбец'")
    parser.add_argument("--import_file", type=str,
                        help="Путь к файлу для импорта (используйте .png для изображений и .txt для текста)")
    parser.add_argument("--filename", type=str, help="Имя выходных файлов")
    parser.add_argument("--console_output", action="store_true", help="Вывести лабиринт в консоль")
    parser.add_argument("--text_output", action="store_true", help="Вывести лабиринт в текстовый файл")
    parser.add_argument("--image_output", action="store_true", help="Вывести лабиринт в изображение")

    args = parser.parse_args()
    maze = None

    if args.size:
        size = args.size.split(",")
        if len(size) != 2:
            print("Ошибка: Укажите размеры в формате 'строки,столбцы'.")
            return

        rows, cols = map(int, size)
        if args.seed:
            seed = int(args.seed)
            maze = Maze(rows, cols, seed)
        else:
            maze = Maze(rows, cols)
        maze.generate_maze()

    if args.solve_indecies:
        solve_indecies = args.solve_indecies.split(",")
        if len(solve_indecies) != 4:
            print("Ошибка: Укажите координаты для решения в формате"
                  " 'начало_строка,начало_столбец,конец_строка,конец_столбец'.")
            return
        start, end = tuple(map(int, solve_indecies[:2])), tuple(map(int, solve_indecies[2:]))
        maze.solve_maze(start, end)

    if args.console_output:
        maze.print_maze()
        if maze.path:
            maze.print_solved_maze()

    if args.filename:
        if args.text_output:
            maze.export_maze_to_file(args.filename + ".txt")
        if args.image_output:
            maze.create_maze_png(maze.maze).save(args.filename + ".png", "PNG")



if __name__ == "__main__":
    main()

#Просто генерация
#python main.py --size 15,15 --seed 63  --console_output


#Генерация и сохранение в файл
#python main.py --size 15,15 --seed 63 --text_output --filename mazeitog1

#Генерация и сохранение в фото
#python main.py --size 15,15 --seed 63 --image_output --filename mazeitog2

#Чтение с файла и вывод в консоль, фото.
#python main.py --import_file mazeitog2 --size 15,15 --solve_indecies 1,1,15,15  --filename mazeitog3 --console_output --text_output --image_output
#python main.py --import_file mazeitog2 --size 15,15 --solve_indecies 1,1,15,15 --seed 63 --filename mazeitog3 --console_output --text_output --image_output

#По рандомной генирации
#python main.py --size 15,15 --solve_indecies 1,1,15,15 --seed 63 --filename mazeitog3 --console_output --text_output --image_output


# python main.py --size 11,11 --solve_indecies 1,1,11,11 --filename mazeitog3 --console_output --text_output --image_output
# python main.py --size 3,3 --solve_indecies 1,1,3,3 --filename maze11 --console_output --text_output --image_output
# python main.py --size 40,40 --solve_indecies 1,1,40,40 --filename maze11 --console_output --text_output --image_output



#python main.py --size 11,11 --solve_indecies 1,1,11,11 --filename maze7 --console_output --text_output --image_output

#Для создания лабиринта алгоритм использует стек для хранения стен, которые можно удалить. Каждая стена проверяется,
# и если вокруг нее есть непосещенные клетки, она превращается в проход

#Приоритет для каждого соседа вычисляется с помощью эвристической
# функции — это манхэттенское расстояние - |x1-x2| + |y1-y2|