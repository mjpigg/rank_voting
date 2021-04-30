import csv

def get_ballots(file_name):
    votes = list()
    with open(file_name) as f:
        for line in csv.reader(f):
            votes.append([[candidate,0] for candidate in line])
            votes[-1][0][1]=1
    return votes

def droop_quota(num_votes, seats):
    return (num_votes//(seats+1))+1

def tally_votes(ballots):
    '''takes in all ballots returns dictionary of tally'''
    tally = {}
    for rank_list in ballots:
        tally[rank_list[0][0]] = tally.get(rank_list[0][0],0) + rank_list[0][1]
    return tally

def display_tally(tally):
    '''Nice print-out of the tally'''
    tally = [(candidate, count) for candidate, count in tally.items()]
    tally.sort(key=lambda k:(k[1],k[0]), reverse = True)
    for candidate,count in tally:
        print(f"{candidate}: {count:.2f} ({100*count/NUM_BALLOTS:.2f}%)")

def find_loser(tally):
    losers = []
    order = [(c,cnt) for c,cnt in tally.items()]
    order.sort(key=lambda k:k[1], reverse=True)
    for candidate,count in tally.items():
        if count == order[-1][1]:
            losers.append(candidate)
    return losers


def find_winner(tally, quota):
    winners = []
    for candidate,count in tally.items():
        if count>=quota:
            winners.append(candidate)
    return winners

def remove_candidate(ballots, candidate, surplus_pct = 1):
    '''This goes through the ballots
    removes the candidate and gives any votes for
    that candidate to next candidate in list
    if surplus pct is passed, then only that pct of vote moves to
    next candidate'''
    # first loop through votes and remove this candidate from 2nd and greater position
    new_ballots = []
    for ballot in ballots:

        if ballot[0][0] != candidate:
            new_ballot = [ballot[0]]
        else:
            ballot[0][1] *= surplus_pct
            new_ballot = []

        if len(ballot)>1:
            new_ballot +=[c for c in ballot[1:] if c[0] != candidate]

        if len(new_ballot)>0 and surplus_pct>0:
            new_ballot[0][1] = ballot[0][1]
            new_ballots.append(new_ballot)

    return new_ballots

def ballot_info(ballots):
    num_ballots = len(ballots)
    votes = 0
    for ballot in ballots:
        votes+= ballot[0][1]
    return num_ballots,votes


# step 1
# get ballots
BALLOTS = get_ballots('votes_milly_30.csv')
NUM_BALLOTS = len(BALLOTS)
SEATS = 2
QUOTA = droop_quota(NUM_BALLOTS, SEATS)
WINNERS = []
print(f"There are {NUM_BALLOTS} valid ballots cast.")
print(f"{QUOTA} votes are required to be elected to 1 of {SEATS} seats")

# next steps will be done in loop until winners + remaining candidates == SEATS
# step 2
# tally votes
ROUND = 1
while len(WINNERS) < SEATS:
    print(f"\n*** ROUND {ROUND} ***")
    n, v = ballot_info(BALLOTS)
    print(f'{n} unexausted ballots remaining worth {v:.2f} votes')
    ROUND += 1
    tally = tally_votes(BALLOTS)
    display_tally(tally)

    # step 3
    # if winner(s), remove them and add them to WINNERS
    # report out
    winners = find_winner(tally,QUOTA)

    if len(winners)>0:
        WINNERS += winners
        for candidate in winners:
            print(f"*** {candidate} is a WINNER ***")
            surplus_votes = tally[candidate]-QUOTA
            print(f"{candidate} has {surplus_votes} surplus votes")
            surplus_pct = surplus_votes/QUOTA
            print(f'{surplus_pct:.2f} of each {candidate} vote will go to second choices for those ballots.')
            BALLOTS = remove_candidate(BALLOTS,candidate,surplus_pct)
    else:
        # step 4
        # if no winners, remove those that are lowest on tally
        # report out
        losers = find_loser(tally)

        # check to see if race is over
        if len(WINNERS) + (len(tally)-len(losers)) < SEATS:
            # print("Check Tally for Final Result")
            break
        for loser in losers:
            print(f'{loser} is being removed and ballots redistributed to next choices')
            BALLOTS = remove_candidate(BALLOTS,loser)

print("\n")
print(f'These Candidate(s) are the winners: {WINNERS}')
if len(WINNERS) != SEATS:
    print(f'Review Tally from last round to determine remaining Winners or Run-Off')
    display_tally(tally)






