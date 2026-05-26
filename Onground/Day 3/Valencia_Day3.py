import numpy as np

arr = np.arange(1, 21)
matrix = arr.reshape (4, 5)


print(f"\nNUMBER 1")
print(matrix)
print(f"The mean is: {matrix.mean()}")

print(f"\nNUMBER 2")
arr2 = np.arange(1, 21)
print(arr)

print(f"\nNUMBER 3")
matrix2 = arr.reshape(4,5)
print(matrix2)

print(f"\nNUMBER 4")
print(matrix2)
print(f"The mean is: {matrix2.mean()}")
print(f"The median is: {np.median(matrix2)}")
print(f"The maximum value is: {matrix2.max()}")

print(f"\nNUMBER 5")
matrix_1 = np.arange(11, 20).reshape(3, 3)
matrix_2 = np.arange(1, 10).reshape(3, 3)
print(matrix_1)
print(matrix_2)

print(f"\nNUMBER 6")
matrix_3 = matrix_1 + matrix_2
print(matrix_3)

print(f"\nNUMBER 7")
matrix_4 = matrix_1 * matrix_2
print(matrix_4)

print(f"\nNUMBER 8")
matrix_5 = matrix_1 @ matrix_2
print(matrix_5)

print(f"\nNUMBER 9")
rand = np.random.normal(loc = 0, scale = 1, size = 100)
print(rand)

