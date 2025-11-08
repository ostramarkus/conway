import os
import glob
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
from alive_progress import alive_bar

import conway

# Settings
grid_size = 100
cell_size = 4
ticks = 10
img_frames = []
ims = []
img_file_path = 'images/'
video_file = 'videos/conway.mp4'


def save_image(img, id):
    """Saves a numbered image in PNG-format"""
    img.save(img_file_path + "img" + str(id).zfill(3) + ".png", "PNG")

def render_pil_image(grid, fill=(30, 255, 100)):
    """Renders a 2 dimensional nparray as a PNG-image"""
    img_size = grid_size * cell_size
    img = Image.new("RGB", (img_size, img_size))
    draw = ImageDraw.Draw(img)

    for index, value in np.ndenumerate(grid):
        if value == 1:
            gx = index[0]
            gy = index[1]

            ix = gx * cell_size
            iy = gy * cell_size

            draw.rectangle([(ix, iy), (ix + cell_size, iy + cell_size)], 
                           fill=fill)
    return img


def create_video():
    """Renders a sequence of images as a video"""
    images = sorted(glob.glob(os.path.join(img_file_path, '*.png')))

    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

    print('Creating video')
    with alive_bar(len(images)) as bar:
        for image in images:
            frame = cv2.imread(image)
            video.write(frame)
            bar()

    video.release()


def main():
    grid = conway.setup_grid(grid_size)
    grid = conway.randomize_grid(grid)

    print('Generating images')

    img_counter = 0
    with alive_bar(ticks) as bar:
        for i in range(ticks):
            grid = conway.update_grid(grid)
            img = render_pil_image(grid)
            save_image(img, img_counter)
            img_counter += 1
            bar()
        
    create_video()

if __name__ == '__main__':
    main()