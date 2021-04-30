# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import random
import csv
seed = "guacamole"
random.seed(seed)
candidates = [letter for letter in "ABCDEFG"]
random.shuffle(candidates)
votes = 9200
ballots = []
with open(f'votes_{seed}_{votes}.csv','w') as f:
    csv_file = csv.writer(f)
    for i in range(votes):
        ballot = random.choices(candidates,weights=[1,2,3,7,6,3,2],k=random.randint(1,7))
        csv_file.writerow(ballot)



