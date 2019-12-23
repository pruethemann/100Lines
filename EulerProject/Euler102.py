file = open('p102_triangles.txt', 'r')



with open('p102_triangles.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
triangles = [x.strip().split(',') for x in content]
t = []
for d in triangles:
    t.append( list(map(int, d)))

triangles = t
#triangles = list(map(int, triangles))

def checkSign(x,y,z):
    if x > 0 and y>0 and z<0:
        return True
    if x < 0 and y<0 and z>0:
        return True
    if x < 0 and y>0 and z<0:
        return True
    if x > 0 and y < 0 and z > 0:
        return True
    if x > 0 and y < 0 and z < 0:
        return True
    if x < 0 and y > 0 and z > 0:
        return True
    return False

count = 0
for t in triangles:

    if checkSign(t[0],t[2],t[4]) and checkSign(t[1],t[3],t[5]):
        count += 1
        print(t, "correct")
    else:
        print(t, "incorrect")





print(count)