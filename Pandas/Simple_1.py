import pandas as pd

data = {
    'bitches' : [2,5,7,8],
    'Hunde' : [9,4,5,3]
}

df = pd.DataFrame(data)

df = pd.DataFrame(data, index=['April', 'may', 'June', 'August'])

print(df)


april = df.loc['April']
may = df.loc['may']

print(april)

print(april - may)