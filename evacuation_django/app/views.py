from django.shortcuts import render
from django.http import JsonResponse
import numpy as np


# Функция для построения кратчайшего пути
def shortest_path(grid, start, end):
    # Размеры двумерного массива
    rows, cols = grid.shape

    # Создаем массив для хранения минимальных расстояний от начальной точки
    distances = np.full((rows, cols), np.inf)
    distances[start] = 0

    # Создаем массив для хранения предыдущей точки на кратчайшем пути
    previous_points = np.full((rows, cols), None)

    # Массив для хранения посещенных точек
    visited = np.zeros((rows, cols), dtype=bool)

    # Пока не достигнута конечная точка
    while True:
        # Найти точку с минимальным расстоянием
        min_distance = np.inf
        current_point = None
        for i in range(rows):
            for j in range(cols):
                if not visited[i, j] and distances[i, j] < min_distance:
                    min_distance = distances[i, j]
                    current_point = (i, j)

        # Если текущая точка не найдена, значит путь не существует
        if current_point is None:
            break

        # Отметить текущую точку как посещенную
        visited[current_point] = True

        # Проверить соседние точки
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = current_point
            nx, ny = x + dx, y + dy

            # Проверяем, что новая точка находится в пределах массива
            if 0 <= nx < rows and 0 <= ny < cols:
                new_point = (nx, ny)
                weight = grid[nx, ny]

                distance = min_distance + weight

                # Если найден более короткий путь, обновляем расстояние и предшествующую точку
                if distance < distances[new_point]:
                    distances[new_point] = distance
                    previous_points[new_point] = current_point

    # Построить путь от конечной точки до начальной точки
    path = []
    current_point = end
    while current_point is not None:
        path.insert(0, current_point)
        current_point = previous_points[current_point]

    # Возвращаем кратчайший путь и его длину
    return path, distances[end]


def index_page(request):
    context={}
    rooms={"room1":"0 0 35 21", "room2":"37 0 58 21", "room3":"0 22 35 57",
           "room4":"37 22 58 45", "room5":"37 46 58 57"}
    ''' координаты комнаты
        roomK - x1, y1, x2, y2
        y1, x1-----------x
        |                |
        |                |
        |                |
        |                |
        |                |
        y-----------y2, x2   '''

    rooms_with_index = ["0 0 35 21", "37 0 58 21", "0 22 35 57",
                        "37 22 58 45", "37 46 58 57"]
    size = (58, 59)
    a = [[0 for j in range(size[1])] for i in range(size[0])]
    for k in range(5):
        x1, y1, x2, y2 = rooms_with_index[k].split()
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        for i in range(x1, x2 + 1):
            a[y1][i] = 1
            a[y2][i] = 1
        for j in range(y1, y2 + 1):
            a[j][x1] = 1
            a[j][x2] = 1
        for i in range(size[0]):
            for j in range(size[1]):
                if j == 36:
                    a[i][j] = 1

    a[22][17] = a[21][17] = a[22][47] = a[21][47] = 0
    a[33][35] = a[33][36] = a[33][37] = 0
    a[51][35] = a[51][36] = a[51][37] = 0
    a[57][47] = 0

    grid = np.array(a)

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        # TODO: тут нужны не константные значения
        start = (1, 1)
        end = (57, 47)

        path, distance = shortest_path(grid, start, end)
        print("Кратчайший путь:", path)
        print("Длина кратчайшего пути:", distance)
        # TODO: тут вернуть в виде render(...)
        return JsonResponse({'message': 'Success'})

    # Если метод запроса GET, просто отображаем шаблон с фотографией этажа
    return render(request, 'index.html')
