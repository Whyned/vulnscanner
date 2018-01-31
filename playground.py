def generator():
    for i in range(0, 20):
        yield (1,2,3)

for a,b,c in generator():
    print(a,b,c)
