# TODO
while True:
    try:
        i = int(input("Height: "))
        f = i
        if i<= 0 or i >= 9:
            print("wrong")
        else:
            break
    except:
        pass
for j in range(i):
    print(" "*(i-j-1), end="")
    for k in range(j+1):
        print("#", end="")
    print("  ", end="")
    for l in range(j+1):
        print("#", end="")
    f +=- 1
    print()