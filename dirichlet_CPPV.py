#!/usr/bin/python
import numpy as np, scipy.stats as spstats, os
import matplotlib.pyplot as plt, pandas as pd

import bayesian_utils

POSTERIOR_SAMPLECOUNT = 100000

os.system('clear')
'''
Assume 2 variants A and B, each of them with 500 page views
Assume N = 3 ads per ad unit, we have N+1 dimensional vector for each variant

Count vectors below summarize the distibution over 4 outcome categories
i.e. the number of clicks per page view
'''

#Variant A: 300 page views have no clicks, 50 have 1 click ...110 have 3 clicks
count_vector_variantA = np.array([ 300, 50, 40, 110 ])

# Start off similar to A but will change shortly
count_vector_variantB = np.array([ 300, 50, 40, 110 ])


'''
Priors: Common for both variants. If you are unsure what the priors should be, this is ok to stick to
It is more important that the priors are the same for both variants and not very sharp i.e. opinionated
'''
prior_vector = np.array([ 2, 2, 2, 2 ])

'''
Designate reward for each outcome category, which in this case is number of clicks
It is like saying that value of each outcome category is proportional to the #clicks
It could potentially be more complex if say 3 clicks is more than 3x valuable than 1 click
For now, 1 click = 1 unit reward
'''
reward_per_outcome_category = np.array(range(0, len(count_vector_variantA)))


'''
As a one-off lets do inference on the A and B with above count vectors
Prob(A better than B) should be around 0.5 because counts_variantA and counts_variantB are very similar
'''
print 'To start with, A and B have same count vector. Hence, evenly placed. Prob(A > B): ', bayesian_utils.prob_A_better_than_B(count_vector_variantA, count_vector_variantB, prior_vector, reward_per_outcome_category)

'''
Lets explore a bit by keeping variant A constant and changing B
Change B such that more page views have 0 clicks and fewer with 3 clicks
such that total page views remain constant at 500
'''
print '\n\nAnd now we start making B progressively worse than A: '
xaxis_vector = list()
yaxis_vector = list()
for incremental_pvs_with_zero_clicks in range(0, 50, 5):
    regenerated_count_vector_variantB = count_vector_variantB + [ incremental_pvs_with_zero_clicks, 0, 0, -incremental_pvs_with_zero_clicks ]
    prob_of_better = bayesian_utils.prob_A_better_than_B(count_vector_variantA, regenerated_count_vector_variantB, prior_vector, reward_per_outcome_category)
    xaxis_vector.append( incremental_pvs_with_zero_clicks )
    yaxis_vector.append( prob_of_better)
    print xaxis_vector
    print '# incremental page views with 0 clicks:', incremental_pvs_with_zero_clicks, ' count_vector_variantA:', count_vector_variantA, ' count_vector_variantB:', regenerated_count_vector_variantB, ' Prob(A > B): ', prob_of_better

FONTSIZE = 20
plt.plot(xaxis_vector, yaxis_vector)
plt.xlabel('Incremental page views in B with 0 clicks', fontsize = FONTSIZE)
plt.ylabel('P(A > B)', fontsize = FONTSIZE)
plt.title('Evolution of P(A > B) as B gets worse', fontsize = FONTSIZE)



