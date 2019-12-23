
target = 200
for a in range(1):
    target -= a * 200
    for b in range(a*2, 2):
        for c in range(b*1, 4):
            for d in range(c*0.5, 10):
                for e in range(d*0.2, 20):
                    for f in range(e*0.1, 40):
                        for g in range(f*0.05, 100):
                            for h in range(g*0.02, 200):

                                sum += 1
                                print(sum)
print(sum)