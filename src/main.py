from PIL import Image

from src.polygon import Orientation
from src.projection import get_transformation_matrix, project_texture_on_image
from src.selector import PointSelector


def main():
    # open images
    texture = Image.open('../statics/generic-diva-sim.jpg')
    image = Image.open('../statics/aula-raquel.jpeg')
    # request four points as a quadrilateral from user
    quadrilateral = PointSelector().request_polygon_from('../statics/aula-raquel.jpeg', n=4)
    # calculate projective coordinates of the mapping of the texture onto the base image
    (x_tex, y_tex) = texture.size
    p = [(0, 0, 1), (x_tex, 0, 1), (x_tex, y_tex, 1), (0, y_tex, 1)]
    q = [(point[0], point[1], 1) for point in quadrilateral.as_list(orientation=Orientation.CLOCKWISE)]
    # calculate matrix of the mapping
    transformation = get_transformation_matrix(p, q)
    # put pixels of the texture on the base image
    project_texture_on_image(base=image, texture=texture, transformation=transformation)
    # save base image
    image.save("out.jpg")


if __name__ == '__main__':
    main()
