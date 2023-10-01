from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import json


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
    coords_rooms = {"room1": [3, 3], "room2": [6, 3], "room3": [9, 2], "room5": [1, 5],
                    "room6": [1, 11], "room7": [7, 10], "room9": [7, 5], "room10": [8, 7],
                    "room11": [10, 11], "room12": [1, 16], "room13": [8, 15], "room14": [3, 19], "room15": [1, 22],
                    "room16": [10, 11], "room17": [1, 16], "room18": [8, 15], "room19": [17, 3], "room20": [1, 22],
                    "room21": [12, 20], "room22": [13, 22], "room23": [14, 3], "room24": [17, 3], "room25": [15, 5],
                    "room26": [15, 8], "room27": [17, 11], "room28": [17, 15], "room29": [15, 17], "room30": [14, 20],
                    "room31": [17, 20], "room32": [20, 22], "room33": [24, 1], "room34": [27, 11], "room35": [29, 1],
                    "room36": [30, 11], "room37": [31, 3], "room38": [33, 3], "room39": [32, 5], "room40": [32, 8],
                    "room41": [32, 14], "room42": [34, 20], "room43": [33, 22], "room44": [39, 1], "room45": [40, 1],
                    "room46": [38, 11], "room47": [43, 20], "room48": [41, 22], "room49": [46, 11], "room50": [45, 17],
                    "room73": [45, 6], "room74": [57, 4], "room75": [56, 1],
                    "room76": [49, 2], "room77": [49, 6], "room78": [49, 16], "room79": [51, 21], "room80": [56, 21],
                    "room81": [57, 18], "room82": [60, 18], "room83": [61, 21], "room85": [63, 20],
                    "room86": [64, 18], "room87": [57, 11], "room88": [65, 11], "room89": [62, 5], "room90": [59, 1],
                    "room91": [69, 20], "room92": [72, 17], "room93": [75, 10], "room94": [69, 11], "room95": [69, 5],
                    "room96": [67, 3], "room97": [65, 1], "room98": [71, 3], "room99": [75, 3], "room100": [75, 1]}


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
        json_data = json.loads(request.body)
        room_id = json_data.get('room_id')
        print("room: ", room_id)
        start = (coords_rooms[room_id])
        # TODO: тут нужно сделать несколько выходов и в итоге использовать ближайший
        end = (26,0)

        path, distance = shortest_path(grid, start, end)
        print("Кратчайший путь:", path)
        print("Длина кратчайшего пути:", distance)
        return render(request, 'index.html', {'path': path})

    # Если метод запроса GET, просто отображаем шаблон с фотографией этажа
    return render(request, 'index.html')

def plan(request):
    return render(request, 'plan.html')