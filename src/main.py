from argparse import ArgumentParser
from pathlib import Path

from PIL import Image

from src.polygon import Orientation
from src.projection import get_transformation_matrix, project_texture_on_image
from src.selector import PointSelector

Pathstr = Path | str


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('image', help='base image onto which project texture')
    parser.add_argument('texture', help='texture image to be projected')
    parser.add_argument('-o', '--out',
                        help='name of the output file for the image, no file extension', default='out')
    parser.add_argument('--out-extension',
                        help='extension to use in the output file, same as base image by default')
    parser.add_argument('--out-directory',
                        help='directory where the output image file should be saved, by default same as base image')
    return parser


def main():
    # parse arguments
    args = create_parser().parse_args()
    path_base_image = Path(args.image)
    path_texture = Path(args.texture)
    out_extension = '.' + args.out_extension if args.out_extension else path_base_image.suffix
    dir_out_file = args.out_directory or path_base_image.parent
    path_out_file = dir_out_file / (args.out + out_extension)
    # do projection calculations and save output file
    do_projection_and_save_output(path_base_image, path_texture, path_out_file)


def do_projection_and_save_output(path_base_image: Pathstr, path_texture: Pathstr, path_out_file: Pathstr):
    # open images
    image = Image.open(path_base_image)
    texture = Image.open(path_texture)
    # request four points as a quadrilateral from user
    quadrilateral = PointSelector().request_polygon_from(path_base_image, n=4)
    # calculate projective coordinates of the mapping of the texture onto the base image
    (x_tex, y_tex) = texture.size
    p = [(0, 0, 1), (x_tex, 0, 1), (x_tex, y_tex, 1), (0, y_tex, 1)]
    q = [(point[0], point[1], 1) for point in quadrilateral.as_list(orientation=Orientation.CLOCKWISE)]
    # calculate matrix of the mapping
    transformation = get_transformation_matrix(p, q)
    # put pixels of the texture on the base image
    project_texture_on_image(base=image, texture=texture, transformation=transformation)
    # save base image
    image.save(path_out_file)
    # release resources
    image.close()
    texture.close()


if __name__ == '__main__':
    main()
