import numpy as np
from PIL import Image

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

print(matrix)

sol = np.linalg.solve(matrix, vet)

print(sol)
