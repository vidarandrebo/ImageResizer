import os
import sys

import cv2


def resolve_file_conflict(path):
    filename = os.path.basename(path)
    folder = os.path.dirname(path)
    name, extension = os.path.splitext(filename)
    n = 0
    while os.path.exists(os.path.join(folder, filename)):
        n += 1
        filename = '%s_%d%s' % (name, n, extension)
    return os.path.join(folder, filename)


def find_dimension(new_width: int, new_height: int, old_width: int, old_height: int):
    if new_width != 0:
        ratio = new_width / old_width
        new_height = old_height * ratio
    else:
        ratio = new_height / old_height
        new_width = old_width * ratio
    return int(new_width), int(new_height)


def resize_image(path, new_width, new_height):
    image = cv2.imread(path)
    dim = find_dimension(new_width, new_height, int(image.shape[1]), int(image.shape[0]))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    name, extension = os.path.splitext(path)
    resolution = '%dX%d' % (dim[0], dim[1])
    path = '%s_%s%s' % (name, resolution, extension)
    path = resolve_file_conflict(path)
    cv2.imwrite(path, resized)


def main(args):
    width = 0
    height = 0
    if args[0] == "-h" or args[0] == "--height":
        height = int(args[1])
    elif args[0] == "-w" or args[0] == "--width":
        width = int(args[1])
    else:
        print("invalid args")
        return
    for file in args[2:]:
        resize_image(file, width, height)
        print(file)


if __name__ == '__main__':
    main(sys.argv[1:])
