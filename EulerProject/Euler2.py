def fibonacci():
    a, b = 1, 2
    while True:
        yield a
        (a,b) = (b, a+b)

sum = 0
for f in fibonacci():
    if f > 4_000_000:
        break
    if f %2==0:
        sum += f

print(sum)



