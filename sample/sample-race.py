import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd

# Setup plotting
plotting.setup_mpl()

# Enable the cache
ff1.Cache.enable_cache('cache')

# Get rid of some pandas warnings that are not relevant for us at the moment
pd.options.mode.chained_assignment = None

# ### Collect the data

# Load the session data
race = ff1.get_session(2022, 'Hungary', 'R')

# Get the laps
laps = race.load_laps(with_telemetry=True)

# Get laps of the drivers (LEC and SAI)
laps_driver1 = laps.pick_driver('LEC')
laps_driver2 = laps.pick_driver('RUS')

# # We are only analyzing stint 1, so select that one
# laps_driver1 = laps_driver1.loc[laps_driver1['Stint'] == 1]
# laps_driver2 = laps_driver2.loc[laps_driver2['Stint'] == 1]

laps_driver1['RaceLapNumber'] = laps_driver1['LapNumber'] - 1
laps_driver2['RaceLapNumber'] = laps_driver2['LapNumber'] - 1

full_distance_driver2_driver1 = pd.DataFrame()
summarized_distance_driver2_driver1 = pd.DataFrame()

for lap in laps_driver1.iterlaps():
    telemetry = lap[1].get_car_data().add_distance().add_driver_ahead()

    # Only run this loop when driver ahead is LEC, otherwise we compare wrong distance gaps
    telemetry = telemetry.loc[telemetry['DriverAhead'] == "63"]

    if len(telemetry) != 0:
        # Full distance
        lap_telemetry = telemetry[['Distance', 'DistanceToDriverAhead']]
        lap_telemetry.loc[:, 'Lap'] = lap[0] + 1

        full_distance_driver2_driver1 = full_distance_driver2_driver1.append(
            lap_telemetry)

        # Asaiage / median distance
        distance_mean = np.nanmean(telemetry['DistanceToDriverAhead'])
        distance_median = np.nanmedian(telemetry['DistanceToDriverAhead'])

        summarized_distance_driver2_driver1 = summarized_distance_driver2_driver1.append({
            'Lap': lap[0] + 1,
            'Mean': distance_mean,
            'Median': distance_median
        }, ignore_index=True)


plt.rcParams['figure.figsize'] = [10, 6]

fig, ax = plt.subplots(2)
fig.suptitle("LEC vs sai opening stint comparison")

ax[0].plot(laps_driver1['RaceLapNumber'],
           laps_driver1['LapTime'], label='LEC', color='red')
ax[0].plot(laps_driver2['RaceLapNumber'],
           laps_driver2['LapTime'], label='RUS', color='blue')
ax[0].set(ylabel='Laptime', xlabel='Lap')
ax[0].legend(loc="upper center")

ax[1].plot(summarized_distance_driver2_driver1['Lap'],
           summarized_distance_driver2_driver1['Mean'], label='Mean', color='red')
ax[1].plot(summarized_distance_driver2_driver1['Lap'],
           summarized_distance_driver2_driver1['Median'], label='Median', color='grey')
ax[1].set(ylabel='Distance (meters)', xlabel='Lap')
ax[1].legend(loc="upper center")

# Hide x labels and tick labels for top plots and y ticks for right plots.
for a in ax.flat:
    a.label_outer()

plt.show()

# Lap 4 Telemetry

# Get lap data
lap_telemetry_driver1 = laps_driver1.loc[laps_driver1['RaceLapNumber'] == 31].get_car_data(
).add_distance()
lap_telemetry_driver2 = laps_driver2.loc[laps_driver2['RaceLapNumber'] == 31].get_car_data(
).add_distance()

distance_lap29 = full_distance_driver2_driver1.loc[full_distance_driver2_driver1['Lap'] == 29]
distance_lap30 = full_distance_driver2_driver1.loc[full_distance_driver2_driver1['Lap'] == 30]
distance_lap31 = full_distance_driver2_driver1.loc[full_distance_driver2_driver1['Lap'] == 31]
distance_lap32 = full_distance_driver2_driver1.loc[full_distance_driver2_driver1['Lap'] == 32]

# Make plot a bit bigger
plt.rcParams['figure.figsize'] = [15, 15]

fig, ax = plt.subplots(5)
fig.suptitle("Lap 31 Telemetry Comparison (LEC overtakes RUS")

ax[0].title.set_text("Distance to RUS (m)")
ax[0].plot(distance_lap29['Distance'], distance_lap29['DistanceToDriverAhead'],
           label='Lap 29', linestyle='dotted', color='grey')
ax[0].plot(distance_lap30['Distance'],
           distance_lap30['DistanceToDriverAhead'], label='Lap 30')
ax[0].plot(distance_lap31['Distance'], distance_lap31['DistanceToDriverAhead'],
           label='Lap 31', linestyle='dotted', color='white')
ax[0].plot(distance_lap32['Distance'], distance_lap32['DistanceToDriverAhead'],
           label='Lap 32', linestyle='dashed', color='lightgrey')
ax[0].legend(loc="lower right")
ax[0].set(ylabel='Distance to RUS')

ax[1].title.set_text("Lap 31 telemetry")
ax[1].plot(lap_telemetry_driver1['Distance'],
           lap_telemetry_driver1['Speed'], label='LEC')
ax[1].plot(lap_telemetry_driver2['Distance'],
           lap_telemetry_driver2['Speed'], label='RUS')
ax[1].set(ylabel='Speed')
ax[1].legend(loc="lower right")

ax[2].plot(lap_telemetry_driver1['Distance'],
           lap_telemetry_driver1['Throttle'], label='LEC')
ax[2].plot(lap_telemetry_driver2['Distance'],
           lap_telemetry_driver2['Throttle'], label='RUS')
ax[2].set(ylabel='Throttle')

ax[3].plot(lap_telemetry_driver1['Distance'],
           lap_telemetry_driver1['Brake'], label='LEC')
ax[3].plot(lap_telemetry_driver2['Distance'],
           lap_telemetry_driver2['Brake'], label='RUS')
ax[3].set(ylabel='Brakes')

ax[4].plot(lap_telemetry_driver1['Distance'],
           lap_telemetry_driver1['DRS'], label='LEC')
ax[4].plot(lap_telemetry_driver2['Distance'],
           lap_telemetry_driver2['DRS'], label='RUS')
ax[4].set(ylabel='DRS')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for a in ax.flat:
    a.label_outer()

plt.show()
