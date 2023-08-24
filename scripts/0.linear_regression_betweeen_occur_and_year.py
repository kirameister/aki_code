from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import json
import numpy as np
import sys


with open('./data/wikipedia_joyo_kanji_freq.json', 'r') as f:
    wikipedia_occur_data = json.load(f)

rank = []
year = []
for i, v in enumerate(wikipedia_occur_data):
    rank.append(i)
    for v2 in v.values():
        year.append(int(v2[1]))
rank = np.array(rank)

if(len(rank) != len(year)):
    print(f'number of rank ({len(rank)}) does not match against number of extracted years ({len(year)})')
    sys.exit(1)

# plot the linear regression graph
coef = np.polyfit(rank,year,1)
poly1d_fn = np.poly1d(coef)

plt.plot(rank,year, 'ro', rank, poly1d_fn(rank), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlim(0, 2400)
plt.ylim(1, 7)
plt.savefig('image/wikipedia_kanji_occur_rank_to_educational_year.png')

# calculate the linear regression score
rank = rank.reshape(-1, 1)
model = LinearRegression().fit(rank, year)
r_sq = model.score(rank, year)
print(f"r^2 score: {r_sq}")
