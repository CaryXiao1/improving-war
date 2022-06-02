"""
war-time-analyzer.py
author: cary xiao
---------------------------------
This file takes in generated .csv files from war-time-simulator.py
and plots each sample's PMF, calculates sample mean and variance,
and estimates the p-value for each null hypothesis that each subsequent 
variation is from the same distribution. 

This program assumes that all .csv files are in the same folder as 
war-time-analyzer.py, that samples inputted are formatted correctly
and that each sample size is identical.
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
import pathlib


# converts data from .csv file into a list. 
# used to extract sample saved data.    
def read_from_file(file_name: str):
    list = []
    with open(file_name, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            if not row[0] == 'number of cards flipped':
                value = int(row[0])
                list.append(value)
    return list


# gets a valid file name or path for a csv file. used by the program
# to create / write into a file 
def get_valid_file_name(display_name: str, default: str):
    file_name = input('input file name for the csv of ' + display_name + ' (or press ENTER if name is ' + default + '): ')
    if file_name == '':
        file_name = default
    # check for ending .csv
    end_name = ''
    if (len(file_name) > 4):
        end_name = file_name[len(file_name) - 4:]
    # if there is no .csv, add it
    if not (end_name == '.csv'):
        file_name += '.csv'
    # return full directory of current directory + file name
    return file_name 


# Gets .csv files corresponding to each distribution and returns
# a list containing each sample list in order. 
def load_data(game_types):
    dists = [0] * 5
    
    file_names = ['default_times.csv', '3card_times.csv', '5card_times.csv', 'reduction_times.csv', 'reduction_5card_times.csv']
    print('default file names, corresponding to their respective game type distributions: ', 
            file_names[0] + ',', file_names[1] + ',', file_names[2] + ',', file_names[3] + ',', file_names[4])
    response = input('do each of your files correspond to the default file names (Y/n)? ')
    response = response.lower()
    while (not response == 'y') and (not response == 'n'):
        response = input("incorrect input. please input Y or n: ")
        response = response.lower()
    if (response == 'n'):
        # get real file names
        for i in range(len(file_names)):
            file_names[i] = get_valid_file_name(game_types[i], file_names[0])
    print('-----------------------------------------------')
    print('importing data from each .csv file...')
    for i in range(5):
        dists[i] = read_from_file(str(pathlib.Path(__file__).parent.resolve()) + '\\' + file_names[i])
    # check that all distributions were correctly loaded in
    return dists
                

#############################################################################
# Main code
#############################################################################

# load all the files into their respective element of dists
game_types = ['stock war', '3-card war','5-card war','reduction war', '5-card reduction war']
dists = load_data(game_types)

NUM_TRIALS = len(dists[0])

print('-----------------------------------------------')
print('calculating sample means, sample variances, and PMFs for each game type...')
means = [0] * 5
vars = [0] * 5
for i in range(len(dists)):
    print()
    means[i] = np.mean(dists[i])
    vars[i] = np.var(dists[i])
    print('sample mean for ' + game_types[i] + ':', means[i])
    print('sample variance for ' + game_types[i] + ':', vars[i])
    print('showing PMF...')
    plt.hist(dists[i], bins = 200, density=True)
    plt.show()

# use bootstrapping on each list to calculate each p-value:
print('-----------------------------------------------')
print('calculating p-values with boostrapping...')

# build universal distribution for each h_0
h0_dists = [0] * 4
for i in range(4):
    h0_dists[i] = dists[i] + dists[i + 1]

# calculate observed differences for each null hypothesis
mean_diffs = [0] * 4  # correspond to H0_1m through H0_4m
var_diffs = [0] * 4 # correspond to H0_1v through H0_4v
for i in range(4):
    mean_diffs[i] = abs(means[i] - means[i + 1])
    var_diffs[i] = abs(vars[i] - vars[i + 1])

# simulate resamples and find probability for both to be the same sample size
p_vals_m = [0] * 4
p_vals_v = [0] * 4

progress = 0
print()

for x in range(NUM_TRIALS):
    # get random samples
    resamples = [0] * 8 # each 2 indeces correspond to the two samples needed from each subsequent universal distribution
    for i in range(4):
        resamples[2 * i] = np.random.choice(h0_dists[i], NUM_TRIALS, replace=True)
        resamples[(2 * i) + 1] = np.random.choice(h0_dists[i], NUM_TRIALS, replace=True)
    
    # calculate the difference between each resample
    resample_mean_diffs = [0] * 4
    resample_var_diffs = [0] * 4
    for i in range(4):
        resample_mean_diffs[i] = abs(np.mean(resamples[2 * i]) - np.mean(resamples[(2 * i) + 1]))
        resample_var_diffs[i] = abs(np.var(resamples[2 * i]) - np.var(resamples[(2 * i) + 1]))
    
    # temporarily treat p_vals to count the number of games where assuming H0 leads to an equal or greater difference
    for i in range(4):
        if (resample_mean_diffs[i] >= mean_diffs[i]):
            p_vals_m[i] += 1
        if (resample_var_diffs[i] >= var_diffs[i]):
            p_vals_v[i] += 1
    
    # update loading percentage
    if (int(round(x / NUM_TRIALS * 100, 2)) > progress):
        progress = int(round(x / NUM_TRIALS * 100, 2))
        sys.stdout.write("\033[F") # Cursor up one line
        print(progress, "%")

sys.stdout.write("\033[F") # Cursor up one line
print(100, '%')

# divide all counts by NUM_TRIALS to get each probability for p_vals:
for i in range(4):
    p_vals_m[i] /= NUM_TRIALS
    p_vals_v[i] /= NUM_TRIALS

# print results
print()
print("Bootstrap calculation of p-values for mean of each successive variation:")
print("-----------------------------------------------------")
for i in range(4):
    print("calculated p-value for H0_" + str(i + 1) + "m: ", p_vals_m[i])

print()
print("Bootstrap calculation of p-values for variance of each successive variation:")
print("-----------------------------------------------------")
for i in range(4):
    print("calculated p-value for H0_" + str(i + 1) + "v: ", p_vals_v[i])
    