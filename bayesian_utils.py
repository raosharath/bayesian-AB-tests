#!/usr/bin/python

import numpy as np

def draw_from_posterior(counts_vector, prior, reward_per_outcome_category, POSTERIOR_SAMPLECOUNT = 10000):
    '''
    computes posterior distribution given prior and likelihood (counts)
    generates K draws from this posterior and computes expected clicks per draw
    '''
    # posterior is sum of counts from data and prior => beauty of conjugagte prior
    # here is interpretation of prior as smoothing with 'pseudo-counts'
    posterior_vector = counts_vector + prior

    # Each draw is of row vector of values all > 0 but summing to 1
    # interpret kth element as the probability of K clicks for adunit
    posterior_draws = np.random.dirichlet(posterior_vector, size=POSTERIOR_SAMPLECOUNT) # dimension POSTERIOR_SAMPLECOUNT x (N+1)


    # going from distribution over number of clicks to expected number of clicks
    # posterior_draws: POSTERIOR_SAMPLECOUNT x (N+1)
    # reward_per_outcome_category: (N+1) x 1
    # expected_outcome: row vector with 1 row per draw
    expected_outcome = np.dot(posterior_draws, reward_per_outcome_category)

    return expected_outcome

def prob_A_better_than_B(counts_variantA, counts_variantB, prior, reward_per_outcome_category):
    expected_outcome_A  = draw_from_posterior(counts_variantA, prior, reward_per_outcome_category)
    expected_outcome_B  = draw_from_posterior(counts_variantB, prior, reward_per_outcome_category)

    # What is prob(A > B)
    # Having sampled from posterior P(A) and P(B), how often is A>B
    return 1. * np.sum(expected_outcome_A > expected_outcome_B)/len(expected_outcome_A)


def prob_A_better_than_B_dual_weights(counts_variantA, counts_variantB, prior, reward_per_OC_A, reward_per_OC_B):
    expected_clicks_A  = draw_from_posterior(counts_variantA, prior, reward_per_OC_A)
    expected_clicks_B  = draw_from_posterior(counts_variantB, prior, reward_per_OC_B)

    # What is prob(A > B)
    return 1. * np.sum(expected_clicks_A > expected_clicks_B)/len(expected_clicks_A)



