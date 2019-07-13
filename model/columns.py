import pandas as pd

df = pd.read_csv('ExtractedTweets.csv')
e = df.groupby(['Handle', 'Party'])['Tweet'].apply('^%^'.join)
e.reset_index(inplace=True)

for i, row in e.iterrows():
    temp = row['Tweet']
    le = temp.split('^%^')
    for j in range(len(le)):
        col = 'Tweet' + str(j)
        e.loc[i, col] = le[j]

e.drop('Tweet', axis=1, inplace=True)

e.to_csv('Final.csv')

print(e.head(10))