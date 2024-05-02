import random


def generato_random_number(n, min_val, max_val):

    for n in range(2):
        yield n
        n = n + 1




r = generato_random_number(0, 1, 10)
print(next(r))
print(next(r))
