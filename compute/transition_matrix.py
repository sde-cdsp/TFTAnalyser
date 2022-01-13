

import numpy as np
import math

class TransitionMatrix(np.matrix):
    """ The transition matrix of the markov chain representing the number of 
    cards of the desired champ allready found
    """
    def __new__(cls, tier_prob, champ_pool_size, 
                 n_cards_out_champ, remaining_cards_in_tier):
        """
        :tier_prob: float
            The probability to draw a card from the tier
        :champ_pool_size: int
            Number of copies of the champ in the pool
        :n_cards_out_champ: int
            Number of copies of the champ already out of the pool
        :remaining_cards_in_tier: int
            Number of cards remaining in the tier pool, desierd champ included
            
        """
        matrix = super().__new__(cls, [[
                TransitionMatrix.probability_one_roll(
                    tier_prob,
                    champ_pool_size-n_cards_out_champ-i,
                    remaining_cards_in_tier-i,
                    j-i
                )
                for j in range(0,10)] for i in range(10)]
            )
        
        # Along the diagonal, the probability to stay in the same state is 
        # 1 minus the probability of other states
        np.fill_diagonal(matrix, 1-matrix.sum(1))

        return matrix

    def get_probabilities(self, n_rolls):
        """ Returns the probability to have found between 1 and 9 cards 

        :n_rolls: int
            Number of rolls

        :returns: (10,1) np.matrix
        """

        return  (np.linalg.matrix_power(self, n_rolls)[0,:]
                .transpose())

    @staticmethod
    def probability_one_roll(tier_prob, champ_remaining_in_pool,
                             remaining_tier_pool, n_cards_found):
        """Returns the probability to find n_cards_found cards 
        of the desired champ in the total pool

        :tier_prob: float
        :champ_remaining_in_pool: int
            number of champs remaining in the pool
        :remaining_tier_pool: int
            Number of cards remaining in the tier pool, desierd champ included
        :n_cards_found: int
            the number of cards of the desired champ found

        :returns: float
            The probability
        """
        # You can't find more than 5 cards or less than 0
        # And there must be some cards in the pool
        if (n_cards_found > 5 
            or n_cards_found <= 0 
            or champ_remaining_in_pool < 0):
            return 0

        # The probability to find n cards in one roll is 
        # $C_n^5 x (p x n_champ/pool_size)^n x (1 - p x n_champ/pool_size)^(5-n)$
        return (math.comb(5, n_cards_found) 
                * ((tier_prob * champ_remaining_in_pool / remaining_tier_pool) 
                    ** n_cards_found) 
                * ((1-(tier_prob * champ_remaining_in_pool / remaining_tier_pool)) 
                    ** (5-n_cards_found)))


if __name__=="__main__":
    matrix = TransitionMatrix(0.3, 18, 10, 200, 50)
    print(matrix)

