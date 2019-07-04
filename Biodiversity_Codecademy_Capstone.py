from matplotlib import pyplot as plt
import pandas as pd
import os
from scipy.stats import chi2_contingency

os.chdir('''C:/Users/Adrian/Documents/Codecademy Intensives/Introduction to\
 Data Analysis''')

species = pd.read_csv('species_info.csv')
observations = pd.read_csv('observations.csv')

print(species.head())
print(observations.head())

# How many different species are in the species DataFrame?
print(species['category'].nunique())
# What are the different values of `category` in `species`?
print(species['category'].unique())
# What are the different values of conservation_status?
print(species['conservation_status'].unique())

'''The column conservation_status has several possible values:

Species of Concern: declining or appear to be in need of conservation
Threatened: vulnerable to endangerment in the near future
Endangered: seriously at risk of extinction
In Recovery: formerly Endangered, but currnetly neither in danger of extinction
throughout all or a significant portion of its range
We'd like to count up how many species meet each of these criteria. Use groupby
to count how many scientific_name meet each of these criteria.
'''

print(species.groupby('conservation_status')
      .scientific_name.nunique().reset_index())
species.fillna('No Intervention', inplace=True)
print(species.groupby('conservation_status')
      .scientific_name.nunique().reset_index())

protection_counts = species.groupby('conservation_status')\
    .scientific_name.count().reset_index()\
    .sort_values(by='scientific_name')

print(protection_counts)

'''Now let's create a bar chart!

Start by creating a wide figure with figsize=(10, 4)
Start by creating an axes object called ax using plt.subplot.
Create a bar chart whose heights are equal to scientific_name column of
protection_counts.
Create an x-tick for each of the bars.
Label each x-tick with the label from conservation_status in protection_counts
Label the y-axis Number of Species
Title the graph Conservation Status by Species
Plot the grap using plt.show()
'''

plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)), protection_counts
        .scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()

'''
Let's create a new column in species called is_protected, which is True if
conservation_status is not equal to No Intervention, and False otherwise.
'''

species['is_protected'] = species['conservation_status'] != 'No Intervention'
# Let's group by *both* `category` and `is_protected`.
# Save your results to `category_counts`.
category_counts = species.groupby(['category', 'is_protected'])\
                         .scientific_name.nunique().reset_index()\
                         .sort_values(by='scientific_name')

print(category_counts.head())

'''
It's going to be easier to view this data if we pivot it.
Using pivot, rearange category_counts so that:

columns is is_protected
index is category
values is scientific_name
Save your pivoted data to category_pivot. Remember to reset_index() at the end.
'''

category_pivot = category_counts.\
    pivot(columns='is_protected', index='category', values='scientific_name').\
    reset_index()
print(category_pivot)

'''Use the .columns property to rename the categories True and False
to something more description:

Leave category as category
Rename False to not_protected
Rename True to protected
'''
category_pivot.columns = ['category', 'not_protected', 'protected']

'''
Let's create a new column of category_pivot called percent_protected,
which is equal to protected (the number of species that are protected)
divided by protected plus not_protected (the total number of species).
'''

category_pivot['percent_protected'] = category_pivot['protected']\
    / (category_pivot['not_protected'] + category_pivot['protected'])

print(category_pivot)

'''
It looks like species in category Mammal are more likely to be endangered than
species in Bird. We're going to do a significance test to see if this
statement is true. Before you do the significance test,
consider the following questions:

Is the data numerical or categorical?
How many pieces of data are you comparing?
Based on those answers, you should choose to do a chi squared test.
In order to run a chi squared test, we'll need to create a contingency table.
Our contingency table should look like this:

||protected|not protected| |-|-|-| |Mammal|?|?| |Bird|?|?|

Create a table called contingency and fill it in with the correct numbers
'''
contingency = [[146, 30], [413, 75]]
print(chi2_contingency(contingency))
contingency2 = [[73, 5], [146, 30]]
print(chi2_contingency(contingency2))

# Use apply and a lambda function to create a new column in species called
# is_sheep which is True if the common_names contains 'Sheep',
# and False otherwise.

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
print(species.head())

# Select the rows of `species` where `is_sheep` is `True` and
# examine the results.

print(species[species.is_sheep])

# Many of the results are actually plants.
# Select the rows of species where is_sheep is True and category is Mammal.
# Save the results to the variable sheep_species.

sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]

# Now merge `sheep_species` with `observations` to get a
# DataFrame with observations of sheep.
# Save this DataFrame as `sheep_observations`.

sheep_observations = observations.merge(sheep_species)

print(sheep_observations.head())

'''
How many total sheep observations (across all three species)
were made at each national park?
Use groupby to get the sum of observations for each park_name.
Save your answer to obs_by_park.

This is the total number of sheep observed in each park over the past 7 days.
'''

obs_by_park = sheep_observations.groupby('park_name')\
    .observations.sum().reset_index().sort_values(by='observations')
print(obs_by_park)

'''
Create a bar chart showing the different number of
observations per week at each park.

Start by creating a wide figure with figsize=(16, 4)
Start by creating an axes object called ax using plt.subplot.
Create a bar chart whose heights are equal to observations
column of obs_by_park.
Create an x-tick for each of the bars.
Label each x-tick with the label from park_name in obs_by_park
Label the y-axis Number of Observations
Title the graph Observations of Sheep per Week
Plot the grap using plt.show()
'''
plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)), obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park.park_name)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()
# usedhttps://s3.amazonaws.com/codecademy-content
# /courses/learn-hypothesis-testing/a_b_sample_size/index.html
minimum_detectable_effect = 100 * (0.05 / 0.15)
print(minimum_detectable_effect)
# Needs to see 870 sheep. One week of sheep observations at Bryce National Park
# yielded 250. Will need about 4 weeks
print(870/250)
# One week of sheep observations at Yellowstone produced 507.
# Will need about 2 weeks
print(870/507)
