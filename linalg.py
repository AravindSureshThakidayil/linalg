import math
from copy import deepcopy 

def sub_matrix(matrix, row=0, column=0):
    new_matrix = deepcopy(matrix)
    new_matrix.remove(matrix[row])
    for i in new_matrix:
        del i[column]
    return new_matrix
def determinant(matrix):
    rows = len(matrix)
    if rows == 1:
        return matrix[0][0]
    elif rows == 2:
        simple_determinant = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return simple_determinant
    else:
        det = 0
        for j in range(rows):
            cofactor = (-1) ** j * matrix[0][j] * determinant(sub_matrix(matrix, column=j))
            det += cofactor
        return det
      
class Vector():
    def __init__(self, a, b):
        self.norm = (a**2 + b**2) ** 0.5
        self.arg = math.atan(b / a)
        self.grid = [a, b]
        self.slope = b / a

class Matrix():
    def __init__(self, rows = 2, columns = 2, grid = [[1, 0], [0, 1]]):
        for row in grid:
            if len(row) != columns:
                raise DimensionalError("Invalid columns")
        if len(grid) == rows:
            self.grid = grid
            self.order = (rows, columns)
            if rows == columns:
                self.determinant = determinant(grid)
                self.square_matrix = True
        else:
            raise DimensionalError("Number of rows do not match")
    def transpose(self):
        buffer = self.grid
        new_grid =[]
        for i in range(self.order[1]):
          new_grid.append([])
          for j in range(self.order[0]):
            new_grid[i].append(buffer[j][i])
        self.grid = new_grid
        self.order = (self.order[1], self.order[0])
    def inverse(self):
        if self.square_matrix and self.determinant != 0:
            o = self.order[0]
            g = self.grid
            buffer = deepcopy(self.grid)
            for i in range(o):
                for j in range(o):
                    self.grid[i][j] = (-1)**(i+j) * determinant(sub_matrix(buffer, j, i))/self.determinant
        elif self.determinant == 0:
            raise NonInvertibleMatrix("This is a singular matrix")
        else:
            raise NonInvertibleMatrix("Non-square matrices do not have an inverse")
    def multiply(self, other):
        if self.order[1] == other.order[0]:
            a, b, c, d = self.order[0], self.order[1], other.order[0], other.order[1]
            buffer_1, buffer_2 = deepcopy(self.grid), deepcopy(other.grid)
            product = []
            for i in range(a):
                product.append([])
                for j in range(d):
                    sum = 0
                    for k in range(b):
                        sum += buffer_1[i][k] * buffer_2[k][j]
                    product[-1].append(sum)
            return Matrix(rows=a, columns=d, grid=product) 
                
        else:
            raise DimensionalError("Cannot multiply these matrices")

class NonInvertibleMatrix(Exception):
    pass
class DimensionalError(Exception):
    pass
