

import numpy as np
import pandas as pd
import plotly.express
import math

from compute.transition_matrix import TransitionMatrix

def draw_roll_probs_figure(player_lvl, champ_tier, golds_to_roll,
                           n_cards_out_champ, n_cards_out_tier):
    """Returns a figure giving the probabilities to find a certain number
    of cards from a champ when rolling golds_to_roll.

    :player_lvl: int
    :champ_tier: int
    :golds_to_roll: int
    :n_cards_out_champ: (int)
        The number of cards of the champ already out of the pool
    :n_cards_out_tier: (int)
        The number of cards of the pool already out not counting the champion
    """
    n_rolls = int(golds_to_roll / 4)
    champ_pool_size, tier_pool_size, tier_prob = get_tier_info(
            player_lvl, champ_tier)

    transition_probability_matrix = TransitionMatrix(
            tier_prob, champ_pool_size, 
            n_cards_out_champ,
            tier_pool_size-n_cards_out_tier-n_cards_out_champ
            )

    probabilities = pd.DataFrame(
            transition_probability_matrix.get_probabilities(n_rolls),
            columns=["Probability"],
            )
    fig = plotly.express.line(probabilities,  y="Probability")

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
            Probability, between 0 and 1, that one card is rolled in the 
            desired champ tier.
    """
    tier_data = pd.read_csv("data/tier_stats.csv", 
            header=0, index_col=0)[str(champ_tier)]

    return (tier_data["pool"], 
            tier_data["N_champs"]*tier_data["pool"], 
            tier_data[str(player_lvl)]/100)

if __name__=="__main__":
    draw_roll_probs_figure(8, 3, 200,
                           10, 35).write_image("test/image1.png")
