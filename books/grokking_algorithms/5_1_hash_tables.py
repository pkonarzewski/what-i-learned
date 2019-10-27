#%% hash table
voted = {}

def check_voter(name):
    if voted.get(name):
        print('You voted already!')
    else:
        voted[name] = True
        print('You can vote')


check_voter('Alec')
check_voter('May')
check_voter('May')
