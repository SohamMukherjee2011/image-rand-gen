'''
##### GENERATES RANDOM NUMBERS USING BUILT-IN LIBRARY #####
This file is used for benchmarking the custom-made RNG with an established PRNG
'''
import random
file1 = open("floats_test.txt", 'w')
file2 = open("numbers_test.txt", 'w')
L = []

for i in range(6000):
    x = random.random()
    x = str(x)
    x = x[0:6]
    x = float(x)
    file1.write(str(x) + '\n')
    file2.write(str(random.randint(0, 100)) + '\n')
file1.close()
file2.close()
    
    
