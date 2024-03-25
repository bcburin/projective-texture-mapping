import numpy as np
from PIL import Image
from numpy import array


def linear_interpolation(f00, f01, d):
    return (1-d)*f00 + d*f01


def bilinear_interpolation(f00, f01, f10, f11, d1, d2):
    return int(linear_interpolation(linear_interpolation(f00, f01, d1), linear_interpolation(f10, f11, d1), d2))


def get_transformation_matrix(p, q) -> array:
    a = np.array([[p[k][j] for j in range(3)] for k in range(4)])
    b = [np.diag([-q[k][i] for k in range(4)]) for i in range(3)]
    # build matrix
    matrix = np.zeros((12, 13))
    # Insert submatrices into the final matrix
    matrix[:4, :3] = a
    matrix[4:8, 3:6] = a
    matrix[8:12, 6:9] = a
    matrix[:4, 9:] = b[0]
    matrix[4:8, 9:] = b[1]
    matrix[8:12, 9:] = b[2]
    # Add a final row with all zeros except the last element as 1
    matrix = np.vstack((matrix, np.append(np.zeros(12), 1)))
    # solve system to find matrix coefficients and multipliers
    solution = np.linalg.solve(matrix, np.append(np.zeros(12), 1))
    # build and return matrix H
    coefficients = solution[:9]
    return coefficients.reshape(3, 3)


def project_texture_on_image(base: Image, texture: Image, transformation: array):
    (x_tex, y_tex) = texture.size
    (x_img, y_img) = base.size
    transformation_inv = np.linalg.inv(transformation)
    for x_pixel in range(x_img):
        for y_pixel in range(y_img):
            v = [x_pixel, y_pixel, 1]
            i, j, k = transformation_inv @ v
            i = float(i) / k
            j = float(j) / k
            if 0 <= i < (x_tex - 1) and 0 <= j < (y_tex - 1):
                p00 = (int(i), int(j))
                p10 = (int(i) + 1, int(j))
                p01 = (int(i), int(j) + 1)
                p11 = (int(i) + 1, int(j) + 1)

                f00 = texture.getpixel(p00)
                f10 = texture.getpixel(p10)
                f01 = texture.getpixel(p01)
                f11 = texture.getpixel(p11)

                r = bilinear_interpolation(f00[0], f01[0], f10[0], f11[0], i - int(i), j - int(j))
                g = bilinear_interpolation(f00[1], f01[1], f10[1], f11[1], i - int(i), j - int(j))
                b = bilinear_interpolation(f00[2], f01[2], f10[2], f11[2], i - int(i), j - int(j))

                base.putpixel((x_pixel, y_pixel), (r, g, b))


