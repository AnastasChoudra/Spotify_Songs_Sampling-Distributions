from helper_functions import choose_statistic, population_distribution, sampling_distribution
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# task 1: load in the spotify dataset
spotify_data = pd.read_csv('spotify_data.csv')
# task 2: preview the dataset
print(spotify_data.head())
# task 3: select the relevant column
song_tempos = spotify_data.tempo
# task 5: plot the population distribution with the mean labeled
population_distribution(song_tempos)
# task 6: sampling distribution of the sample mean
sampling_distribution(song_tempos, 30, 'Mean')
# task 8: sampling distribution of the sample minimum
sampling_distribution(song_tempos, 30, 'Minimum')
# task 10: sampling distribution of the sample variance
sampling_distribution(song_tempos, 30, 'Variance')
# task 13: calculate the population mean and standard deviation
population_mean = np.mean(song_tempos)
population_std = np.std(song_tempos)
print(f'Mean = {population_mean:.2f}\nSTD = {population_std:.2f}')
# task 14: calculate the standard error
standard_error = population_std/(30**.5)
print(f'Standard error = {standard_error:.2f}')
# task 15: calculate the probability of observing an average tempo of 140bpm or lower from a sample of 30 songs
#print(stats.poisson.cdf(140, population_mean, standard_error)) #not the poisson
#CLT justifies normality for sample means. Poisson is for counts, not continuous averages.
#Poisson is inappropriate here: The Poisson distribution models counts of rare events (e.g., number of emails per hour). Your problem involves continuous data (tempo in bpm), not counts, and focuses on the mean of a sample, not discrete events.
#print(stats.norm.cdf(140, population_mean, standard_error))
print(f'Probability the beat is less than 140bpm: {stats.norm.cdf(140, population_mean, standard_error) * 100:.2f}%')
# alternative with round function
# print("Probability:", round(stats.norm.cdf(140, population_mean, standard_error) * 100, 2), "%")
# task 16: calculate the probability of observing an average tempo of 150bpm or higher from a sample of 30 songs
print(f'Probability the beat is more than 150bpm: {(1 - stats.norm.cdf(150, population_mean, standard_error)) * 100:.2f}%')