import os
import glob
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
from alive_progress import alive_bar

import conway

# Settings
GRID_SIZE = 128
FRAMES = 200
CELL_SIZE = 4

img_file_path = 'images/'
video_file = 'videos/conway.mp4'


def save_image(img, id):
    """Saves a numbered image in PNG-format"""
    img.save(img_file_path + "img" + str(id).zfill(3) + ".png", "PNG")


def render_image(grid, fill=(30, 255, 100)):
    """Renders a 2 dimensional nparray as a PNG-image"""
    img_size = GRID_SIZE * CELL_SIZE
    img = Image.new("RGB", (img_size, img_size))
    draw = ImageDraw.Draw(img)

    for index, value in np.ndenumerate(grid):
        if value == 1:
            gx = index[0]
            gy = index[1]

            ix = gx * CELL_SIZE
            iy = gy * CELL_SIZE

            draw.rectangle([(ix, iy), (ix + CELL_SIZE, iy + CELL_SIZE)], 
                           fill=fill)
    return img


def create_video():
    """Renders a sequence of images as a video"""
    images = sorted(glob.glob(os.path.join(img_file_path, '*.png')))

    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

    with alive_bar(len(images)) as bar:
        for image in images:
            frame = cv2.imread(image)
            video.write(frame)
            bar()

    video.release()

def delete_images():
    """Delete image files"""
    files = glob.glob(img_file_path + '*')
    for f in files:
        os.remove(f)

def main():
    delete_images()

    grid = conway.setup_grid(GRID_SIZE)
    grid = conway.randomize_grid(grid)

    print('--- Running generations - creating images ---')
    with alive_bar(FRAMES) as bar:
        for i in range(FRAMES):
            grid = conway.update_grid(grid)
            img = render_image(grid)
            save_image(img, i)
            bar()

    print('--- Creating video ---')
    create_video()

if __name__ == '__main__':
    main()