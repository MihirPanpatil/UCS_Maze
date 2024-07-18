from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#import random
import heapq

def index(request):
    return render(request, 'maze/index.html')

@csrf_exempt
def solve_maze(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        maze = data['maze']
        start = tuple(data['start'])
        end = tuple(data['end'])
        
        path, cost = uniform_cost_search(maze, start, end)
        
        return JsonResponse({'path': path, 'cost': cost})

def uniform_cost_search(maze, start, end): #Applying Uniform Cost Search
    rows = len(maze)
    cols = len(maze[0])
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, (x, y), path = heapq.heappop(queue)

        if (x, y) == end:
            return path+[(x, y)], cost
        
        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx = x+dx
            ny = y+dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                heapq.heappush(queue, (cost + 1, (nx, ny), path + [(x, y)]))

    return None, None