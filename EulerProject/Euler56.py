def digitalSum_wrong(n):
    sum = 0
    while n > 0:
        sum += n%10
        print(n%10)
        n = int(n/10)
    return sum

def digitalSum(n):
    n_str = str(n)
    sum =0
    for n in n_str:
        sum += int(n)
    return sum

max = 0




for a in range(100):
    for b in range(100):
        d = digitalSum(a**b)

        if d > max:
            max = d
            a_max = a
            b_max = b

print(max)
print(a_max)
print(b_max)



