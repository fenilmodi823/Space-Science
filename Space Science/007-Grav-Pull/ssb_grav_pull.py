# Import modules
import datetime

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import spiceypy

# Clear any previously loaded kernels
spiceypy.kclear()

# Load kernels via meta file
spiceypy.furnsh('kernel_meta.txt')
print("Meta Kernel Loaded:", spiceypy.ktotal("ALL"))

# Manually load kernels (in correct order)
spiceypy.furnsh('../kernels/lsk/naif0012.tls')  # Leap Seconds
spiceypy.furnsh('../kernels/spk/de432s.bsp')    # Ephemeris Data
spiceypy.furnsh('../kernels/pck/pck00010.tpc')  # Planet Constants

# Time interval setup
init_time_utc = datetime.datetime(2000, 1, 1)
delta_days = 10000
end_time_utc = init_time_utc + datetime.timedelta(days=delta_days)

init_time_utc_str = init_time_utc.strftime('%Y-%m-%dT%H:%M:%S')
end_time_utc_str = end_time_utc.strftime('%Y-%m-%dT%H:%M:%S')

print(f'Init time in UTC: {init_time_utc_str}')
print(f'End time in UTC: {end_time_utc_str}\n')

# Convert UTC to Ephemeris Time (ET)
init_time_et = spiceypy.utc2et(init_time_utc_str)
end_time_et = spiceypy.utc2et(end_time_utc_str)

# Time interval array
time_interval_et = np.linspace(init_time_et, end_time_et, delta_days)

# Sun radius for scaling
_, radii_sun = spiceypy.bodvcd(10, 'RADII', 3)
radius_sun = radii_sun[0]

# Dataframe initialization
solar_system_df = pd.DataFrame({'ET': time_interval_et})
solar_system_df['UTC'] = solar_system_df['ET'].apply(lambda x: spiceypy.et2datetime(x).date())

# SSB position and scaled position
solar_system_df['POS_SSB_WRT_SUN'] = solar_system_df['ET'].apply(lambda x: spiceypy.spkgps(0, x, 'ECLIPJ2000', 10)[0])
solar_system_df['POS_SSB_WRT_SUN_SCALED'] = solar_system_df['POS_SSB_WRT_SUN'].apply(lambda x: x / radius_sun)
solar_system_df['SSB_WRT_SUN_SCALED_DIST'] = solar_system_df['POS_SSB_WRT_SUN_SCALED'].apply(spiceypy.vnorm)

# Planet tracking
NAIF_ID_DICT = {'JUP': 5, 'SAT': 6}

for planet, naif_id in NAIF_ID_DICT.items():
    pos_col = f'POS_{planet}_WRT_SUN'
    angle_col = f'PHASE_ANGLE_SUN_{planet}2SSB'
    solar_system_df[pos_col] = solar_system_df['ET'].apply(lambda x: spiceypy.spkgps(naif_id, x, 'ECLIPJ2000', 10)[0])
    solar_system_df[angle_col] = solar_system_df.apply(lambda row: np.degrees(spiceypy.vsep(row[pos_col], row['POS_SSB_WRT_SUN'])), axis=1)

# Plotting
plt.style.use('dark_background')
fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 15))

colors = {'JUP': 'tab:cyan', 'SAT': 'tab:orange'}

for ax, (planet, name) in zip(axes[:2], [('JUP', 'Jupiter'), ('SAT', 'Saturn')]):
    ax.set_title(f'{name} Distance and Phase Angle', color=colors[planet])
    ax.plot(solar_system_df['UTC'], solar_system_df['SSB_WRT_SUN_SCALED_DIST'], color=colors[planet], label='SSB Distance')
    ax.set_ylabel('SSB Dist. in Sun Radii')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='dashed', alpha=0.5)

    ax_twin = ax.twinx()
    ax_twin.plot(solar_system_df['UTC'], solar_system_df[f'PHASE_ANGLE_SUN_{planet}2SSB'], color='tab:red', linestyle='--', label='Phase Angle')
    ax_twin.set_ylabel('Phase Angle (deg)')
    ax_twin.legend(loc='upper right')
    ax_twin.invert_yaxis()

axes[2].set_title('Combined Phase Angles', color='tab:green')
axes[2].plot(solar_system_df['UTC'], solar_system_df['PHASE_ANGLE_SUN_JUP2SSB'], color='tab:cyan', label='Jupiter')
axes[2].plot(solar_system_df['UTC'], solar_system_df['PHASE_ANGLE_SUN_SAT2SSB'], color='tab:orange', label='Saturn')
axes[2].set_ylabel('Phase Angle (deg)')
axes[2].invert_yaxis()
axes[2].legend()
axes[2].grid(True, linestyle='dotted', alpha=0.7)

axes[2].set_xlabel('Date in UTC')
fig.tight_layout()
plt.subplots_adjust(hspace=0.3)
plt.savefig('PLANETS_SUN_SSB_PHASE_ANGLE_COMPLEX.png', dpi=300)
plt.show()