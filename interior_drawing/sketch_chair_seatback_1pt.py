import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import random
import os
import cv2
from tqdm import tqdm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors

from chair_seatback import *


def create_env():
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', computed_zorder=False)
    ax.set_axis_off()

    # record the usage of the space
    interior_space = np.full((20, 20), False)

    vertices = np.array([
        [0, 0, 0],
        [10, 0, 0],
        [10, 0, 5],
        [0, 0, 5],
        [-10, 10, 15],
        [-10, 10, 0],
        [20, 10, 0],
        [20, 10, 15]
    ])

    # Define the edges of the box
    edges = [
        [0, 1], [0, 3], [0, 5],
        [1, 2], [1, 6], [2, 3],
        [2, 7], [3, 4], 
    ]

    # Draw edges of the box
    for edge in edges:
        ax.plot(
            [vertices[edge[0]][0], vertices[edge[1]][0]],
            [vertices[edge[0]][1], vertices[edge[1]][1]],
            [vertices[edge[0]][2], vertices[edge[1]][2]],
            c='w'
        )

    return fig, ax, vertices, interior_space




def draw(ax, interior_space, furniture_name="chair", furniture_num=1):

    seed = np.random.randint(0, 1000)

    for _ in range(furniture_num):

        if furniture_name == "chair_seatback":
            vertices, edges, faces, color, interior_space = chair_seatback(interior_space, seed)
        else:
            raise ValueError(f"NO existing furniture of {furniture_name}")

        for edge in edges:
            ax.plot(
                [vertices[edge[0]][0], vertices[edge[1]][0]],
                [vertices[edge[0]][1], vertices[edge[1]][1]],
                [vertices[edge[0]][2], vertices[edge[1]][2]],
                c='k'
            )
        
        # plot the faces
        if faces:
            faces = [[vertices[i] for i in face] for face in faces]
            collection = Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='k', alpha=1.0)
            collection.set_zorder(10)
            ax.add_collection3d(collection)
    
    return ax, interior_space


def generate_one_interior_space(save_path=None):

    fig, ax, vertices, interior_space = create_env()

    # random initialize furniture number
    chair_seatback_num = random.randint(1, 1)

    ## draw
    # bigger furniture should be placed first
    ax, interior_space = draw(ax, interior_space, "chair_seatback", chair_seatback_num)
    
    # Set the viewing angle
    elev = random.randint(15, 20)
    azim = random.randint(0, 90)
    dist = random.randint(3, 5)
    ax.view_init(elev=elev, azim=azim)
    ax.dist = dist

    # Show the plot
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()


def crop_view(save_path):
    view = cv2.imread(str(save_path), 0)

    object_pixels = np.argwhere(view == 0)

    min_x = np.min(object_pixels[:, 1])
    max_x = np.max(object_pixels[:, 1])
    min_y = np.min(object_pixels[:, 0])
    max_y = np.max(object_pixels[:, 0])

    new_view = view[min_y-2:max_y+2, min_x-2:max_x+2]

    cv2.imwrite(str(save_path), new_view)




if __name__ == "__main__":
    data_num = 2
    save_images = False
    save_dir = Path("./")
    save_dir.mkdir(parents=True, exist_ok=True)
    for i in tqdm(range(data_num)):
        save_path = save_dir / f"1point_{i}.png" if save_images else None
        generate_one_interior_space(save_path)  
        if save_images:
            crop_view(save_path)

