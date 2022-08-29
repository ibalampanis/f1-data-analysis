import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd

img_dir = '../img/'
cache_dir = '../../cache'

# Setup plotting
plotting.setup_mpl()

# Enable the cache
ff1.Cache.enable_cache(cache_dir)

# Get rid of some pandas warnings that are not relevant for us at the moment
pd.options.mode.chained_assignment = None

# Load the session data
race = ff1.get_session(2022, 'Hungary', 'R')

# Get the laps
laps = race.load_laps(with_telemetry=True)

driver_stints = laps[['Driver', 'Stint', 'Compound', 'LapNumber']].groupby(
    ['Driver', 'Stint', 'Compound']).count().reset_index()

driver_stints = driver_stints.rename(columns={'LapNumber': 'StintLength'})
driver_stints = driver_stints.sort_values(by=['Stint'])

compound_colors = {
    'SOFT': '#FF3333',
    'MEDIUM': '#FFF200',
    'HARD': '#EBEBEB',
    'INTERMEDIATE': '#39B54A',
    'WET': '#00AEEF',
}

plt.rcParams["figure.figsize"] = [12, 4]
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()

# drivers = race.results['Abbreviation'].head(6)
drivers = ['VER', 'RUS', 'PER', 'HAM', 'SAI', 'LEC']

for driver in drivers:
    stints = driver_stints.loc[driver_stints['Driver'] == driver]

    previous_stint_end = 0
    for _, stint in stints.iterrows():
        plt.barh(
            [driver],
            stint['StintLength'],
            left=previous_stint_end,
            color=compound_colors[stint['Compound']],
            edgecolor="black"
        )

        previous_stint_end = previous_stint_end + stint['StintLength']

plt.title(f'Hungary GP 2022 - Race Strategy (Top 6 Drivers)')
plt.xlabel('Lap')
plt.gca().invert_yaxis()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.savefig(img_dir + 'strategy_top6_hungaryGP2022.png', dpi=300)
# plt.show()

laps_driver1 = laps.pick_driver('VER')
laps_driver2 = laps.pick_driver('HAM')
laps_driver3 = laps.pick_driver('RUS')
laps_driver4 = laps.pick_driver('SAI')
laps_driver5 = laps.pick_driver('PER')
laps_driver6 = laps.pick_driver('LEC')

laps_driver1['RaceLapNumber'] = laps_driver1['LapNumber'] - 1
laps_driver2['RaceLapNumber'] = laps_driver2['LapNumber'] - 1
laps_driver3['RaceLapNumber'] = laps_driver3['LapNumber'] - 1
laps_driver4['RaceLapNumber'] = laps_driver4['LapNumber'] - 1
laps_driver5['RaceLapNumber'] = laps_driver5['LapNumber'] - 1
laps_driver6['RaceLapNumber'] = laps_driver6['LapNumber'] - 1

plt.rcParams['figure.figsize'] = [12, 7]

plt.plot(laps_driver1['RaceLapNumber'],
         laps_driver1['LapTime'], label='VER', color='blue')
plt.plot(laps_driver2['RaceLapNumber'],
         laps_driver2['LapTime'], label='HAM', color='green')
plt.plot(laps_driver3['RaceLapNumber'],
         laps_driver3['LapTime'], label='RUS', color='grey')
plt.plot(laps_driver4['RaceLapNumber'],
         laps_driver4['LapTime'], label='SAI', color='black')
plt.plot(laps_driver5['RaceLapNumber'],
         laps_driver5['LapTime'], label='PER', color='yellow')
plt.plot(laps_driver6['RaceLapNumber'],
         laps_driver6['LapTime'], label='LEC', color='red')
# plt.set(ylabel='Laptime', xlabel='Lap')
plt.title(f'Hungary GP 2022 - Race Pace (Top 6 Drivers)')
plt.legend(loc="upper center", ncol=2)
plt.savefig(img_dir + 'race_pace_top6_hungaryGP2022.png', dpi=300)
# plt.show()

laps_driver1 = laps.pick_driver('VER')
laps_driver3 = laps.pick_driver('RUS')
laps_driver5 = laps.pick_driver('PER')

laps_driver1['RaceLapNumber'] = laps_driver1['LapNumber'] - 1
laps_driver3['RaceLapNumber'] = laps_driver3['LapNumber'] - 1
laps_driver5['RaceLapNumber'] = laps_driver5['LapNumber'] - 1

plt.rcParams['figure.figsize'] = [12, 7]

plt.plot(laps_driver1['RaceLapNumber'],
         laps_driver1['LapTime'], label='VER', color='blue')
plt.plot(laps_driver3['RaceLapNumber'],
         laps_driver3['LapTime'], label='RUS', color='grey')
plt.plot(laps_driver5['RaceLapNumber'],
         laps_driver5['LapTime'], label='PER', color='yellow')

# plt.set(ylabel='Laptime', xlabel='Lap')
plt.title(f'Hungary GP 2022 - Race Pace (VER vs RUS vs PER)')
plt.legend(loc="lower right")
plt.savefig(img_dir + 'race_pace_ver_rus_per_hungaryGP2022.png', dpi=300)
# plt.show()

laps_driver1 = laps_driver1.loc[laps_driver1['Stint'] == 3]
laps_driver3 = laps_driver3.loc[laps_driver3['Stint'] == 3]
laps_driver5 = laps_driver5.loc[laps_driver5['Stint'] == 3]

laps_driver1['RaceLapNumber'] = laps_driver1['LapNumber'] - 1
laps_driver3['RaceLapNumber'] = laps_driver3['LapNumber'] - 1
laps_driver5['RaceLapNumber'] = laps_driver5['LapNumber'] - 1

plt.rcParams['figure.figsize'] = [12, 7]

plt.plot(laps_driver1['RaceLapNumber'],
         laps_driver1['LapTime'], label='VER', color='blue')
plt.plot(laps_driver3['RaceLapNumber'],
         laps_driver3['LapTime'], label='RUS', color='grey')
plt.plot(laps_driver5['RaceLapNumber'],
         laps_driver5['LapTime'], label='PER', color='yellow')
# plt.set(ylabel='Laptime', xlabel='Lap')
plt.title(f'Hungary GP 2022 - Last Stint Race Pace (VER vs RUS vs PER)')
plt.legend(loc="lower right")
plt.savefig(img_dir + 'race_pace_ver_rus_per_last_stint_hungaryGP2022.png', dpi=300)
# plt.show()

laps_driver2 = laps.pick_driver('HAM')
laps_driver4 = laps.pick_driver('SAI')

laps_driver2['RaceLapNumber'] = laps_driver2['LapNumber'] - 1
laps_driver4['RaceLapNumber'] = laps_driver4['LapNumber'] - 1


plt.rcParams['figure.figsize'] = [12, 7]

plt.plot(laps_driver2['RaceLapNumber'],
         laps_driver2['LapTime'], label='HAM', color='grey')
plt.plot(laps_driver4['RaceLapNumber'],
         laps_driver4['LapTime'], label='SAI', color='red')
# plt.set(ylabel='Laptime', xlabel='Lap')
plt.title(f'Hungary GP 2022 - Race Pace (HAM vs SAI)')
plt.legend(loc="lower right")
plt.savefig(img_dir + 'race_pace_ham_sai_hungaryGP2022.png', dpi=300)
# plt.show()

laps_driver2 = laps_driver2.loc[laps_driver2['Stint'] == 3]
laps_driver4 = laps_driver4.loc[laps_driver4['Stint'] == 3]

laps_driver2['RaceLapNumber'] = laps_driver2['LapNumber'] - 1
laps_driver4['RaceLapNumber'] = laps_driver4['LapNumber'] - 1

plt.rcParams['figure.figsize'] = [12, 7]

plt.plot(laps_driver2['RaceLapNumber'],
         laps_driver2['LapTime'], label='HAM', color='grey')
plt.plot(laps_driver4['RaceLapNumber'],
         laps_driver4['LapTime'], label='SAI', color='red')
# plt.set(ylabel='Laptime', xlabel='Lap')
plt.title(f'Hungary GP 2022 - Last Stint Race Pace (HAM vs SAI)')
plt.legend(loc="lower right")
plt.savefig(img_dir + 'race_pace_ham_sai_last_stint_hungaryGP2022.png', dpi=300)
# plt.show()

laps_driver5 = laps.pick_driver('PER')
laps_driver6 = laps.pick_driver('LEC')

laps_driver5 = laps_driver5.loc[laps_driver5['Stint'] == 3]
laps_driver6 = laps_driver6.loc[laps_driver6['Stint'] >= 3]

laps_driver5['RaceLapNumber'] = laps_driver5['LapNumber'] - 1
laps_driver6['RaceLapNumber'] = laps_driver6['LapNumber'] - 1

plt.rcParams['figure.figsize'] = [12, 7]

plt.plot(laps_driver5['RaceLapNumber'],
         laps_driver5['LapTime'], label='PER', color='blue')
plt.plot(laps_driver6['RaceLapNumber'],
         laps_driver6['LapTime'], label='LEC', color='red')
# plt.set(ylabel='Laptime', xlabel='Lap')
plt.title(f'Hungary GP 2022 - Last Stints Race Pace (PER vs LEC)')
plt.legend(loc="lower right")
plt.savefig(img_dir + 'race_pace_per_lec_last_stints_hungaryGP2022.png', dpi=300)
# plt.show()
