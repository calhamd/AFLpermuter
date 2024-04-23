import itertools
import random
import tqdm
import math 
from functools import reduce



def expected_probability(matchups, permutation, desired_rounds, starting_round):
    current_probability = 1    
    for round, team in enumerate(permutation, start=starting_round):
        if round > (desired_rounds+starting_round):
            break        
        current_probability *= matchups[round].get(team, 0) #random.random()# matchups[f'Round {round}'][team]        
    return current_probability


def expected_probability_(matchups, permutation, desired_rounds, starting_round):
    current_probability = []
    for round, team in enumerate(permutation, start=starting_round):
        if round > (desired_rounds+starting_round):
            break        
        current_probability.append((matchups[round].get(team, 0), team, round)) #random.random()# matchups[f'Round {round}'][team]        
    return reduce(lambda x, y: x * y, [a[0] for a in current_probability]), current_probability

def filtered_permutations(teams, tot_rounds, starting_round, filter_func, matchups):
    for perm in _dynamic_permutations(teams, tot_rounds, starting_round, filter_func, matchups):
        yield perm
        
        
def _dynamic_permutations(teams, tot_rounds, round, filter_func, matchups):
    if tot_rounds == 1:
        for team in teams:
            if filter_func(team, matchups, round):
                yield (team,)
    else:
        for i, team in enumerate(teams):
            if filter_func(team, matchups, round):
                remaining_teams = teams[:i] + teams[i+1:]
                for perm in _dynamic_permutations(remaining_teams, tot_rounds-1, round+1, filter_func, matchups):
                    yield (team,) + perm



def generate_matchups_random(teams,num_rounds):    
    matchups = {}

    for round_num in range(1, num_rounds + 1):
        round_matchups = {}
        remaining_teams = teams.copy()
        random.shuffle(remaining_teams)

        while remaining_teams:
            team1 = remaining_teams.pop(0)
            if remaining_teams:
                team2 = remaining_teams.pop(0)
                prob1 = random.uniform(0.1, 0.9)
                prob2 = 1 - prob1
                round_matchups[team1] = prob1
                round_matchups[team2] = prob2
            else:
                round_matchups[team1] = 1.0

        matchups[round_num] = round_matchups
    return matchups


# teams = ['Collingwood', 'Carlton', 'Essendon', 'Hawthorn', 'Melbourne', 'North Melbourne', 'Richmond', 'St Kilda', 'Western Bulldogs', 'Adelaide', 'Brisbane', 'Fremantle', 'Geelong', 'Gold Coast', 'Greater Western Sydney', 'Port Adelaide', 'Sydney', 'West Coast'] #[f'Team {a}' for a in range(18)]

# def calculate_likelihood(rating_a, rating_b):
#     total_rating = rating_a + rating_b
#     likelihood_a = rating_a / total_rating
#     likelihood_b = rating_b / total_rating
#     return likelihood_a, likelihood_b

def calculate_likelihood(rating_a, rating_b):
    expected_score_a = 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))
    expected_score_b = 1 - expected_score_a
    return expected_score_a, expected_score_b

def generate_matchups(team_ratings, rounds):
    matchups = {}

    for round_num, matchups_in_round in rounds.items():
        round_matchups = {}
        for team_a, team_b in matchups_in_round:
            rating_a = team_ratings[team_a]
            rating_b = team_ratings[team_b]
            likelihood_a, likelihood_b = calculate_likelihood(rating_a, rating_b)
            round_matchups[team_a] = round(likelihood_a, 2)
            round_matchups[team_b] = round(likelihood_b, 2)
        matchups[round_num] = round_matchups

    return matchups

if __name__ == "__main__":

    team_ratings = {
        'Geelong Cats': 1701,
        'Carlton': 1669,
        'Sydney Swans': 1636,
        'GWS Giants': 1626,
        'Collingwood': 1610,
        'Melbourne': 1583,
        'Port Adelaide': 1580,
        'Essendon': 1574,
        'Brisbane Lions': 1512,
        'Western Bulldogs': 1504,
        'Gold Coast Suns': 1455,
        'Fremantle': 1441,
        'St Kilda': 1425,
        'Adelaide Crows': 1408,
        'West Coast Eagles': 1404,
        'Richmond': 1345,
        'Hawthorn': 1324,
        'North Melbourne': 1195
    }


    rounds = {
        7: [['Richmond', 'Melbourne'], ['Essendon', 'Collingwood'], ['GWS Giants', 'Brisbane Lions'], ['Port Adelaide', 'St Kilda'], ['North Melbourne', 'Adelaide Crows'], ['Geelong Cats', 'Carlton'], ['Fremantle', 'Western Bulldogs'], ['Gold Coast Suns', 'West Coast Eagles'], ['Hawthorn', 'Sydney Swans']],
        8: [['Adelaide Crows', 'Port Adelaide'], ['Carlton', 'Collingwood'], ['Sydney Swans', 'GWS Giants'], ['St Kilda', 'North Melbourne'], ['Melbourne', 'Geelong Cats'], ['West Coast Eagles', 'Essendon'], ['Richmond', 'Fremantle'], ['Western Bulldogs', 'Hawthorn'], ['Brisbane Lions', 'Gold Coast Suns']],
        9: [['Carlton', 'Melbourne'], ['Geelong Cats', 'Port Adelaide'], ['Fremantle', 'Sydney Swans'], ['Hawthorn', 'St Kilda'], ['Essendon', 'GWS Giants'], ['Richmond', 'Western Bulldogs'], ['Gold Coast Suns', 'North Melbourne'], ['Collingwood', 'West Coast Eagles'], ['Adelaide Crows', 'Brisbane Lions']],
        10: [['Gold Coast Suns', 'Geelong Cats'], ['Sydney Swans', 'Carlton'], ['Collingwood', 'Adelaide Crows'], ['GWS Giants', 'Western Bulldogs'], ['St Kilda', 'Fremantle'], ['Brisbane Lions', 'Richmond'], ['Essendon', 'North Melbourne'], ['Port Adelaide', 'Hawthorn'], ['West Coast Eagles', 'Melbourne']],
        11: [['Western Bulldogs', 'Sydney Swans'], ['Fremantle', 'Collingwood'], ['North Melbourne', 'Adelaide Crows'], ['Carlton', 'Gold Coast Suns'], ['Geelong Cats', 'GWS Giants'], ['Richmond', 'Essendon'], ['Hawthorn', 'Brisbane Lions'], ['Melbourne', 'St Kilda'], ['Adelaide Crows', 'West Coast Eagles']],
        12: [['Port Adelaide', 'Carlton'], ['Collingwood', 'Western Bulldogs'], ['Hawthorn', 'Adelaide Crows'], ['West Coast Eagles', 'St Kilda'], ['Geelong Cats', 'Richmond'], ['Melbourne', 'Fremantle'], ['Gold Coast Suns', 'Essendon']],
        13: [['Adelaide Crows', 'Richmond'], ['Western Bulldogs', 'Brisbane Lions'], ['Hawthorn', 'GWS Giants'], ['West Coast Eagles', 'North Melbourne'], ['St Kilda', 'Gold Coast Suns'], ['Sydney Swans', 'Geelong Cats'], ['Essendon', 'Carlton'], ['Collingwood', 'Melbourne']],
        14: [['Brisbane Lions', 'St Kilda'], ['Western Bulldogs', 'Fremantle'], ['Richmond', 'Hawthorn'], ['Adelaide Crows', 'Sydney Swans'], ['North Melbourne', 'Collingwood'], ['GWS Giants', 'Port Adelaide']],
        15: [['Carlton', 'Geelong Cats'], ['Port Adelaide', 'Brisbane Lions'], ['GWS Giants', 'Sydney Swans'], ['Melbourne', 'North Melbourne'], ['Essendon', 'West Coast Eagles'], ['Fremantle', 'Gold Coast Suns']],
        16: [['Brisbane Lions', 'Melbourne'], ['Geelong Cats', 'Essendon'], ['Gold Coast Suns', 'Collingwood'], ['North Melbourne', 'Western Bulldogs'], ['Richmond', 'Carlton'], ['St Kilda', 'Port Adelaide'], ['Sydney Swans', 'Fremantle'], ['Adelaide Crows', 'GWS Giants'], ['West Coast Eagles', 'Hawthorn']],
        17: [['Brisbane Lions', 'Adelaide Crows'], ['Collingwood', 'Essendon'], ['Geelong Cats', 'Hawthorn'], ['GWS Giants', 'Carlton'], ['Melbourne', 'West Coast Eagles'], ['North Melbourne', 'Gold Coast Suns'], ['St Kilda', 'Sydney Swans'], ['Port Adelaide', 'Western Bulldogs'], ['Fremantle', 'Richmond']],
        18: [['Collingwood', 'Geelong Cats'], ['Gold Coast Suns', 'Port Adelaide'], ['Hawthorn', 'Fremantle'], ['Melbourne', 'Essendon'], ['Richmond', 'GWS Giants'], ['Sydney Swans', 'North Melbourne'], ['Western Bulldogs', 'Carlton'], ['Adelaide Crows', 'St Kilda'], ['West Coast Eagles', 'Brisbane Lions']],
        19: [['Brisbane Lions', 'Sydney Swans'], ['Carlton', 'North Melbourne'], ['Essendon', 'Adelaide Crows'], ['Geelong Cats', 'Western Bulldogs'], ['GWS Giants', 'Gold Coast Suns'], ['Hawthorn', 'Collingwood'], ['St Kilda', 'West Coast Eagles'], ['Port Adelaide', 'Richmond']],
        20: [['Carlton', 'Port Adelaide'], ['Collingwood', 'Richmond'], ['Gold Coast Suns', 'Brisbane Lions'], ['Melbourne', 'GWS Giants'], ['North Melbourne', 'Geelong Cats'], ['St Kilda', 'Essendon'], ['Sydney Swans', 'Western Bulldogs'], ['Adelaide Crows', 'Hawthorn'], ['Fremantle', 'West Coast Eagles']],
        21: [['Collingwood', 'Carlton'], ['Essendon', 'Fremantle'], ['Geelong Cats', 'Adelaide Crows'], ['GWS Giants', 'Hawthorn'], ['North Melbourne', 'Richmond'], ['St Kilda', 'Brisbane Lions'], ['Western Bulldogs', 'Melbourne'], ['Port Adelaide', 'Sydney Swans'], ['West Coast Eagles', 'Gold Coast Suns']],
        22: [['Brisbane Lions', 'GWS Giants'], ['Carlton', 'Hawthorn'], ['Essendon', 'Gold Coast Suns'], ['Melbourne', 'Port Adelaide'], ['North Melbourne', 'West Coast Eagles'], ['Richmond', 'St Kilda'], ['Sydney Swans', 'Collingwood'], ['Adelaide Crows', 'Western Bulldogs'], ['Fremantle', 'Geelong Cats']],
        23: [['Collingwood', 'Brisbane Lions'], ['Essendon', 'Sydney Swans'], ['Gold Coast Suns', 'Melbourne'], ['GWS Giants', 'Fremantle'], ['Hawthorn', 'Richmond'], ['St Kilda', 'Geelong Cats'], ['Western Bulldogs', 'North Melbourne'], ['Port Adelaide', 'Adelaide Crows']],
        24: [['Brisbane Lions', 'Essendon'], ['Carlton', 'St Kilda'], ['Geelong Cats', 'West Coast Eagles'], ['Hawthorn', 'North Melbourne'], ['Melbourne', 'Collingwood'], ['Richmond', 'Gold Coast Suns'], ['Sydney Swans', 'Adelaide Crows'], ['Western Bulldogs', 'GWS Giants'], ['Fremantle', 'Port Adelaide']]
        # Add matches for other rounds
    }


    matchups = generate_matchups(team_ratings, rounds)

    num_rounds = 16
    # matchups = generate_matchups(teams, num_rounds=num_rounds)
    # print(matchups)

    def filter_func(team, matchups, round):
        score = matchups[round].get(team, 0)
        return score >= 0.6

    pauls_matchups = ['Sydney Swans', 'St Kilda', 'Gold Coast Suns', 'Port Adelaide', 'Adelaide Crows', 'Geelong Cats', 'GWS Giants', 'Brisbane Lions', 'Essendon', 'Western Bulldogs', 'Fremantle', 'Melbourne' ,'Carlton', 'Collingwood', 'Richmond', 'West Coast Eagles', 'Hawthorn', 'North Melbourne']
    score, deets = expected_probability_(matchups, pauls_matchups, 16, 7)
    print(f'Paul score {score}')
    for i, deet in enumerate(deets):
        score = deet[0]
        team = deet[1]
        round = deet[2]
        for matches in rounds[round]:
            if team in matches:
                opponent = [a for a in matches if a != team][0]
        # print(f"ROUND {round} \t Team: {team} \t \t Opponent:{opponent} \t \t Predcted Win Likelihood:{score}")
        print(f"ROUND {round:<5} \t Team: {team:<20} \t Opponent: {opponent:<20} \t Predcted Win Likelihood: {score:<10}")
        
    best_score = 0
    for perm in tqdm.tqdm(filtered_permutations(list(team_ratings.keys()), num_rounds, 7, filter_func, matchups)):
        score, deets = expected_probability_(matchups, perm, num_rounds, 7)
        if score > best_score:
            print(f"Permutation: {perm}, score {score}")    
            best_score = score
            best_permutation = deets

    for i, deet in enumerate(deets):
        score = deet[0]
        team = deet[1]
        round = deet[2]
        for matches in rounds[round]:
            if team in matches:
                opponent = [a for a in matches if a != team][0]
        # print(f"ROUND {round} \t Team: {team} \t \t Opponent:{opponent} \t \t Predcted Win Likelihood:{score}")
        print(f"ROUND {round:<5} \t Team: {team:<20} \t Opponent: {opponent:<20} \t Predcted Win Likelihood: {score:<10}")

    