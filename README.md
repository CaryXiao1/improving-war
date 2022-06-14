# improving-war
This was my submission for the Stanford Spring 2022 CS 109 Contest, where I simulated thousands of games of 
stock war and some of its variations to determine how long each game type will take.
You can find my full writeup at https://www.overleaf.com/read/xywjmxyqmhmr.
### Simulating Games and Calculating P-Values
To use the python code in this repository, download both python programs and place them in the same folder 
on your computer. Next, run war-time-simulator.py, which will simulate each of the game types and store 
the resulting list of number of flips required to finish the game in individaul .csv in the same folder. 

Finally, run war-time-analyzer.py, specify the files corresponding to each distribution, and the program
will calculate the sample mean, variance, and generate the sample PMF for each game type. Finally, it
calculates the p-value for null hypotheses for each sequential game type, as found in the writeup.
