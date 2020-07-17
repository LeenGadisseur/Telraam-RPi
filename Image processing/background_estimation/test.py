import backEstimation as be
import numpy as np

b = np.array([[1.1, 2.2, 3.3], [1.2, 1.3, 1.4]])
c = np.array([[1.1, 2.2, 3.3], [1.2, 1.3, 1.4]])
#be.example(b)
be.helloworld()
a = 2
d = be.verdubbel(a)
print("originele a: ", a)

print("verdubbelde a : ", d)
array = [1, 2]
print("array: ", array)

print("array b: ", b)
be.example(b)
print("array b na example: ", b)
