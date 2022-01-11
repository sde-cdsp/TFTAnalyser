

import numpy as np
import pandas as pd
import plotly.express

def draw_roll_probs_figure(player_lvl, champ_tier, golds_to_roll,
        n_cards_out_champ, n_cards_out_tier):
    """TODO: Docstring for .
    """
    number_of_rolls = golds_to_roll / 4
    champ_pool_size, tier_pool_size, tier_prob = get_tier_info(
            player_lvl, champ_tier)

    transition_probability_matrix = np.matrix(
            [[
                probability_one_roll(
                    tier_prob,
                    champ_pool_size-n_cards_out_champ-i,
                    tier_pool_size-n_cards_out_tier-n_cards_out_champ-i,
                    j-i
                )
                for j in range(0,10)] for i in range(10)]
            )
    numpy.fill_diagonal(transition_probability_matrix, 1-transition_probability_matrix.sum(1))

    probabilities = np.pow(transition_probability_matrix, number_of_rolls)[0,:]

    fig = plotly.express.line(probabilities, x="N cards found", y="Probability")

    return fig

def get_tier_info(player_lvl, champ_tier):
    """Returns champion tier pool size and probability

    :player_lvl: int
    :champ_tier: int
    :returns: 
        champ_pool_size : int
            Total size of the pool of the disered champ
        tier_pool_size : int
            Total size of the pool of the disered tier
        tier_prob : float
            Probability, between 0 and 1, that one card is rolled in the desired champ tier.
    """
    tier_data = pd.read_csv("data/tier_stats.csv", header=0, index_col=0)[str(champ_tier)]

    return tier_data["pool"], tier_data["N_champs"]*tier_data["pool"], tier_data[str(player_lvl)]/100

def probability_one_roll(tier_prob, champ_remaining_in_pool, remaining_tier_pool, n_cards_found):
    """Returns the probability to find n_cards_found cards of the desired champ in the total pool

    :tier_prob: float
    :champ_remaining_in_pool: int
        number of champs remaining in the pool
    :remaining_tier_pool: int
        total size of the tier pool
    :n_cards_found: int
        the number of cards of the desired champ found

    :returns: float
        The probability
    """
    if n_cards_found > 5 or n_cards_found < 0:
        return 0

    return maths.comb(5, n_cards_found) * ((tier_prob * champ_remaining_in_pool / remaining_tier_pool) ** n_cards_found) \
            ((1-(tier_prob * champ_remaining_in_pool / remaining_tier_pool)) ** n_cards_found)

