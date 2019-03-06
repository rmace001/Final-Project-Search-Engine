import os
directory = 'data/level2/'

for filename in os.listdir(directory):
    print(filename)
    file = open(directory + filename, "r")
    print(file.readline())

