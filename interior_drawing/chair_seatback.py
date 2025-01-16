import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import random



def assign_random_location(interior_space, vertices):

    # first move the furniture to the first quadrant
    if np.min(vertices[:, 0]) < 0:
        vertices[:, 0] -= np.min(vertices[:, 0])
    if np.min(vertices[:, 1]) < 0:
        vertices[:, 1] -= np.min(vertices[:, 1])
    if np.min(vertices[:, 2]) < 0:
        vertices[:, 2] -= np.min(vertices[:, 2])

    # find the boundary of the furniture
    min_x, max_x = np.min(vertices[:, 0]), np.max(vertices[:, 0])
    min_y, max_y = np.min(vertices[:, 1]), np.max(vertices[:, 1])

    # generate 10 random coord and find the best location to place the furniture
    iteration = 100
    best_cover_area = np.inf
    best_x, best_y = None, None
    for i in range(iteration):
        random_x_loc, random_y_loc = np.random.randint(low=0, high=5, size=(2,))
        new_min_x, new_max_x = int(min_x + random_x_loc), int(max_x + random_x_loc)
        new_min_y, new_max_y = int(min_y + random_y_loc), int(max_y + random_y_loc)
        cover_existed_furniture_area = np.sum(interior_space[new_min_x:new_max_x+1, new_min_y:new_max_y+1])
        # print(f"iter: {i}, best_cover_area: {best_cover_area}, current_area: {cover_existed_furniture_area}")
        if cover_existed_furniture_area < best_cover_area:
            best_cover_area = cover_existed_furniture_area
            best_x, best_y = random_x_loc, random_y_loc
            if best_cover_area == 0:
                break
    
    vertices[:, 0] += best_x
    vertices[:, 1] += best_y
    new_min_x, new_max_x = int(min_x + best_x), int(max_x + best_x)
    new_min_y, new_max_y = int(min_y + best_y), int(max_y + best_y)
    # print("new boundary:", new_min_x, new_max_x, new_min_y, new_max_y)
    interior_space[new_min_x:new_max_x+1, new_min_y:new_max_y+1] = True

    return interior_space, vertices





def chair_seatback(interior_space, seed):
    # Generate random size for the box
    size_x = np.random.uniform(low=0.5, high=0.8, size=(1,))
    size_y = np.random.uniform(low=0.5, high=0.8, size=(1,))
    size_z = np.random.uniform(low=0.7, high=2, size=(1,))
    size = np.concatenate([size_x, size_y, size_z])

    # Define the vertices of the box
    vertices = np.array([
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 0],
        [1, -1, 0],
        [1, 1, 0],
        [-1, 1, 0],

        [1, 1, -2],
        [-1, 1, -2],
        [1, -1, -2],
        [-1, -1, -2],
        
        [-1, -1, 2],
        [1, -1, 2],
    ])

    # Scale the vertices by the random size
    vertices = vertices * size

    # assign good random location
    interior_space, vertices = assign_random_location(interior_space, vertices)

    # Define the edges of the box
    edges = [
        [0, 1],[1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7],

        [0, 11], [1, 10], [2, 8], [3, 9],
        
        [12, 4],[13, 5],[12, 13]
    ]

    # Define faces for coloring and the random color
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [0, 4, 7, 3],
        [4, 5, 13, 12]
    ]
    cmap = plt.get_cmap('RdGy')
    random.seed(seed)
    rand_num = random.uniform(0.05, 1)
    color = cmap(rand_num)
    color = colors.to_rgb(color)
    
    return vertices, edges, faces, color, interior_space