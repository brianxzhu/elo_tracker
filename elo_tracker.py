# ELO tracker
# Brian - 03.08.2018
import os, pandas as pd, trueskill as tru, xlsxwriter
# Set filepaths for the source data, make sure directories are double slashed
filepath = 'C:\\Users\\Brian\\Desktop\\'
filename = 'asdf.xlsx'
file = filepath + filename

# Read the excel sheet with the match history into Python
df = pd.read_excel(file, sheetname = 'match history')

# Create a master player list from the history sheet
player_list = []
for x in df['player 1']:
    player_list.append(x)

for y in df['player 2']:
    player_list.append(y)

# Create dictionary with unique player list and assign the default ELO
unique_player_list = set(player_list)
data_array = []
for i in unique_player_list:
    data_array.append(i)

# Assign the default elo to each player in the list
elo_dict = dict()
for i in unique_player_list:
    elo_dict[i] = tru.Rating(25)


# ELO calculation logic
winner = ''
loser = ''

# Checks for player 1 winning, player 2 winning, or a draw
tru.draw_probability=.333
tru.sigma = 8.333333333333334
tru.beta = 4.166666666666667
tru.tau = 0.08333333333333334
for i in range(0,len(df)):
    if (df['score'][i] > df['score.1'][i]) == True:
        # Identifies the winner/loser name based on the if statement
        winner = df['player 1'][i]
        loser = df['player 2'][i]
        # Changes the elo of the winner and loser based on the match outcome
        elo_dict[winner], elo_dict[loser] = tru.rate_1vs1(elo_dict[winner],elo_dict[loser])
        print('Winner is: ' + winner + ' ' + str(elo_dict[winner]))
        print('Loser is: ' + loser + ' ' + str(elo_dict[loser]))
    elif (df['score.1'][i] > df['score'][i]) == True:
        winner = df['player 2'][i]
        loser = df['player 1'][i]
        elo_dict[winner], elo_dict[loser] = tru.rate_1vs1(elo_dict[winner],elo_dict[loser])
        print('Winner is: ' + winner + ' ' + str(elo_dict[winner]))
        print('Loser is: ' + loser + ' ' + str(elo_dict[loser]))
    elif (df['score.1'][i]==df['score'][i]) == True:
        draw1 = df['player 1'][i]
        draw2 = df['player 2'][i]
        elo_dict[draw1], elo_dict[draw2] = tru.rate_1vs1(elo_dict[draw1],elo_dict[draw2], drawn = True)
        print('Draw!' + draw1 + ' = ' + str(elo_dict[draw1]) + ' ' + draw2 + ' = ' + str(elo_dict[draw2]))

# Write the results to an excel file (not working)
workbook = xlsxwriter.Workbook(filepath + 'Results.xlsx')
worksheet = workbook.add_worksheet()
for key in elo_dict.keys():
    print(key + ' ' + str(elo_dict[key]))
    #worksheet.write(key,elo_dict[key])

workbook.close()
