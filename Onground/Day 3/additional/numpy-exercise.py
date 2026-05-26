import numpy as np

arr = np.arange(1, 21)
matrix =arr.reshape(4,5)

print(matrix)
print(matrix.mean())

# create numpy array 1-20
arr = np.arange(1,21)
print("\n Array from 1-20: ")
print(arr)

# reshape array to 4x5 matrix
matrix =arr.reshape(4,5)
print("\n 4x5 Matrix: ")
print(matrix)

#find mean, median, max, min
print("\nMean: ", matrix.mean())
print("Median: ", np.median(matrix))
print("Max: ", matrix.max())
print("Min: ", matrix.min())

# create two 3x3 arrays and perform
matrix_1 = np.arange(11,20).reshape(3,3)
matrix_2 = np.arange(1,10).reshape(3,3)
print(matrix_1)
print(matrix_2)

#element wise addition
print("\nAddition")
result = matrix_1 + matrix_2
print(result)

#element wise multiplication
print("\nMultiplication")
result = matrix_1 * matrix_2
print(result)

#matrix muliplication
print("\nMatrix Multiplication")
print(matrix_1 @ matrix_2)

#generate 100 random nums from normal distribution and calc standard deviation
rand = np.random.normal(loc=0, scale=1, size=100)
print("Random normal nummbers: ")
print(rand)

#replace all values greateer than 50 in an array with 50
arr = np.arange(35,100)
arr[arr > 50] =50
print(arr)

#Given an array, find the indicies of all even number.
numbers = np.array([3,8,15,22,30,41])
even_idencies = np.where(numbers % 2==0)
print("\nIndecies of even numbers: ", even_idencies[0])

#normalize an array so its values are between 0 and 1
data = np.array([10,20,30,40,50])
normalized = (data - np.min(data)) / (np.max(data)) - (np.min(data))
print("\nNormalized array: ", normalized)

# create a 5x5 identity matrix
identity_matrix = np.eye(5)
print("\n5X5 identity matrix")
print(identity_matrix)

#compute the dot product of two vectors
v1 = np.array ([1,2,3])
v2 = np.array ([4,5,6])
dot_product = np.dot(v1, v2)
print(dot_product)
