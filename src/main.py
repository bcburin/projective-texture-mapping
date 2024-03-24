import numpy as np
from PIL import Image

# interpolação onde d é a distância entre os pixels e f00 e f01 representam a cor em cada pixel
def interpolacao(f00, f01, d):
    return (1-d)*f00 + d*f01
def bilinear(f00, f01, f10, f11, d1, d2):
    return int(interpolacao(interpolacao(f00,f01,d1), interpolacao(f10,f11,d1), d2))


im1 = Image.open("../statics/generic-diva-sim.jpg")
im2 = Image.open("../statics/aula-raquel.jpeg")

(x,y) = im1.size
(z,w) = im2.size

# Pontos da textura
p = [(0, 0, 1), (x, 0, 1), (0, y, 1), (x, y, 1)]

# Pontos de destino
q = [(212, 152, 1), (723, 203, 1), (191, 566, 1), (711, 569, 1)]

a = np.array([[p[k][j] for j in range(3)] for k in range(4)])
b = [np.diag([-q[k][i] for k in range(4)]) for i in range(3)]

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

vet = np.zeros(13)
vet[-1] = 1

sol = np.linalg.solve(matrix, vet)
print(sol)

coefficients = sol[:9]
print(coefficients)
coefficients = coefficients.reshape(3, 3)
print(coefficients)

p = [[0, 0, 1], [x, 0, 1], [0, y, 1], [x, y, 1]]

coefficients_inv = np.linalg.inv(coefficients)


# a varia em x na imagem de destino
# b varia em y na imagem de destino
for a in range(z):
    for b in range(w):
        v = [a, b, 1]
        i, j, k = coefficients_inv @ v
        i = float(i) / k
        j = float(j) / k
        if 0 <= i < (x - 1) and 0 <= j < (y - 1):
            p00 = (int(i), int(j))
            p10 = (int(i) + 1, int(j))
            p01 = (int(i), int(j) + 1)
            p11 = (int(i) + 1, int(j) + 1)

            Ff00 = im1.getpixel((p00))
            Ff10 = im1.getpixel(p10)
            Ff01 = im1.getpixel(p01)
            Ff11 = im1.getpixel(p11)

            R = bilinear(Ff00[0], Ff01[0], Ff10[0], Ff11[0], i - int(i), j - int(j))
            G = bilinear(Ff00[1], Ff01[1], Ff10[1], Ff11[1], i - int(i), j - int(j))
            B = bilinear(Ff00[2], Ff01[2], Ff10[2], Ff11[2], i - int(i), j - int(j))

            im2.putpixel((a, b), (R, G, B))

im2.save("produto_final.jpg")

