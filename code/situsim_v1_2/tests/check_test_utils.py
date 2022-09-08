from test_utils import near

# should all result in false
print(near(1, 1.1))
print(near(1, 1.1, 0.09))
print(near(-1, -1.1))
print(near(-1, 1))

print()

# should all result in true
print(near(1, 1-1E-7))
print(near(1, 1.1, 0.11))
print(near(-1, -1.01, 0.1))
