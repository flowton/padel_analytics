import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.markdown("""
# :tennis:Padel Analytics

###  Analytical approach to the hyped match on Center Court at 2021-04-23

*Data can be viewed in:*
* **Result** (if the ball was won)
* **Playstyle** (how the ball was won)

""")

df = pd.read_csv('padel_analytics.csv')

st.sidebar.markdown("""
## :mag:Select filters for the game

"""
)
selected_sets = st.sidebar.multiselect(
    'Sets',
    (1,2,3),
    default = (1,2,3)
)
selected_games = st.sidebar.multiselect(
    'Game',
    (1,2,3,4,5,6,7,8,9,10),
    default = (1,2,3,4,5,6,7,8,9,10)
)

selected_players = st.sidebar.multiselect(
    'Server',
    ('Anton', 'Simon', 'Fredrik', 'Olle'),
    default = ('Anton', 'Simon', 'Fredrik', 'Olle')
)

inverse_order = st.sidebar.checkbox(
    'View the win/lose from Fredrik&Olles point of view'
)
df = df[df['set'].isin(selected_sets)]
df = df[df['game'].isin(selected_games)]
df = df[df['server'].isin(selected_players)]



# Check values of columns
#for col in df.columns:
#    print('__' + col + '__')
#    print(df[col].unique())



## ___DATA CLEANING___

df['set_game'] = df['set']* 100+  df['game']
df['set_game'] = df['set_game'].values.astype(str)

def extract_string(order, dict):
    array = []
    for input in df['raw_input']:
        char = input[order:order+1]
        res = dict[char]
        array.append(res)
    return array

# Create conversion dictionaries from single char into full name

win_type_dict = {
    'U': 'Unforced',
    'S': 'Strike',
    'P': 'Play'
}

shot_type_dict = {
    'V': 'Volley',
    'O': 'Overhead',
    'B': 'Base',
    'N': 'NA'
}

location_dict = {
    'N': 'Net',
    'G': 'Glass',
    '-': 'NA',
}

player_dict = {
    'A': 'Anton',
    'O': 'Olle',
    'F': 'Fredrik',
    'S': 'Simon'
}

result_dict = {
    'W': True,
    'L': False
}

# Assign values to arrays

win_type_arr = extract_string(0, win_type_dict)
shot_type_arr = extract_string(1, shot_type_dict)
location_arr = extract_string(2, location_dict)
player_arr = extract_string(3, player_dict)
result_arr = extract_string(4, result_dict)

# Assign arrays to Dataframe

df['win_type'] = win_type_arr
df['shot_type'] = shot_type_arr
df['location'] = location_arr
df['player'] = player_arr
df['result'] = result_arr

## ___Result Analysis___
result_view = st.checkbox('Show Result View')
if(result_view):

    # Check if result should be reveresed in case of other viewpoint
    if(inverse_order):
        df['result'] = [not res for res in df['result']]

    colors = ['green' if win else 'red' for win in df['result']]
    time = [1 if win else -1 for win in df['result']]

    plt.bar(df['ball_in_game'], time, color = colors)

    net_win_arr = []
    net = 0
    for point in df['result']:
        if point:
            net = net + 1
        else:
            net = net -1
        net_win_arr.append(net)
        print(net)

    plt.plot(df['ball_in_game'], net_win_arr)
    ax = plt.gca()
    #ax.axes.yaxis.set_visible(False)
    ax.axhline(linewidth = 1, color = 'grey')
    plt.xlabel('ball', fontsize = 16)
    plt.ylabel('net games won', fontsize = 16)
    plt.title('Result for each ball in the game', fontsize='20', fontweight='bold')

    st.pyplot(plt.gcf())
    plt.clf()

## ___Playstyle analysis___
playstyle_view = st.checkbox('Show Playstyle View')

if playstyle_view:
    st.markdown("""
    * By default, won/lose is viewed from Anton/Simon side. Use checkbox in sidebar to change point of view. 
    """)
    ## Initialize array to store values for the stacked bar chart.
    setgames_list = []

    setgame_unforced = []
    setgame_strike = []
    setgame_play = []

    setgame_base = []
    setgame_volley = []
    setgame_overhead = []

    # Loop over all set_game, count number of occurence of each type.
    for set_game in df['set_game'].unique():
        df_temp = df[df['set_game'] == set_game]

        unforced = 0
        strike = 0
        play = 0
        for i in df_temp['win_type']:
            if i == 'Unforced' :
                unforced = unforced +1
            if i == 'Strike' :
                strike = strike + 1
            if i == 'Play':
                play = play +1

        base = 0
        volley = 0
        overhead = 0
        for i in df_temp['shot_type']:
            if i == 'Overhead':
                overhead = overhead +1
            if i == 'Volley':
                volley = volley + 1
            if i == 'Base':
                base = base +1

        setgames_list.append(set_game)
        setgame_unforced.append(unforced)
        setgame_strike.append(strike)
        setgame_play.append(play)
        setgame_overhead.append(overhead)
        setgame_volley.append(volley)
        setgame_base.append(base)


    ## Display Cause of Win
    p1_win = plt.bar(setgames_list, setgame_play, color = 'grey', label = 'normal play')
    p2_win = plt.bar(setgames_list, setgame_unforced, bottom = setgame_play, color = 'red', label = 'unforced error')
    p3_win = plt.bar(setgames_list, setgame_strike, bottom = np.asarray(setgame_play) + np.asarray(setgame_unforced), color = 'green', label = 'strike')
    plt.xticks(rotation = 90)
    plt.ylabel('Amount in the game')
    plt.xlabel('Set-Game \n')
    plt.title('Cause of win', fontsize = 20)
    plt.legend()

    st.pyplot(plt.gcf())
    plt.clf()



    ## Display final type of shot
    p1_shot = plt.bar(setgames_list, setgame_base, color = 'grey', label = 'base')
    p2_shot = plt.bar(setgames_list, setgame_volley, bottom = setgame_base, color = 'cornflowerblue', label = 'volley')
    p3_shot = plt.bar(setgames_list, setgame_overhead, bottom = np.asarray(setgame_base) + np.asarray(setgame_volley), color = 'royalblue', label = 'overhead')
    plt.xticks(rotation = 90)
    plt.ylabel('Amount in the game')
    plt.xlabel('Set-Game \n')
    plt.title('Final type of shot', fontsize = 20)
    plt.legend()

    st.pyplot(plt.gcf())
    plt.clf()




