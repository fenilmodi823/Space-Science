# Import modules
import datetime
import spiceypy
import numpy as np
from matplotlib import pyplot as plt

# Clear any previously loaded kernels
spiceypy.kclear()

# Load kernels manually
spiceypy.furnsh('../kernels/lsk/naif0012.tls')  # Leap Seconds
spiceypy.furnsh('../kernels/spk/de432s.bsp')    # Ephemeris Data
spiceypy.furnsh('../kernels/pck/pck00010.tpc')  # Planet Constants

print("Total Kernels Loaded:", spiceypy.ktotal("ALL"))

# Set Initial Time in UTC
init_time_utc = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
delta_days = 10000  # 10,000 days
end_time_utc = init_time_utc + datetime.timedelta(days=delta_days)

# Convert datetime to strings
init_time_utc_str = init_time_utc.strftime('%Y-%m-%dT%H:%M:%S')
end_time_utc_str = end_time_utc.strftime('%Y-%m-%dT%H:%M:%S')

# Convert UTC to Ephemeris Time (ET)
init_time_et = spiceypy.utc2et(init_time_utc_str)
end_time_et = spiceypy.utc2et(end_time_utc_str)

# Time Interval for Calculations
time_interval_et = np.linspace(init_time_et, end_time_et, delta_days)
ssb_wrt_sun_position = []

# Calculate SSB Position w.r.t Sun
for time_et in time_interval_et:
    position, _ = spiceypy.spkgps(targ=0, et=time_et, ref='ECLIPJ2000', obs=10)
    ssb_wrt_sun_position.append(position)

# Convert to numpy array
ssb_wrt_sun_position = np.array(ssb_wrt_sun_position)

# Get Sun Radius
_, radii_sun = spiceypy.bodvcd(bodyid=10, item='RADII', maxn=3)
radius_sun = radii_sun[0]

# Scale Position by Sun Radius
ssb_wrt_sun_position_scaled = ssb_wrt_sun_position / radius_sun

# Plot the SSB Trajectory
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8))
sun_circle = plt.Circle((0.0, 0.0), 1.0, color='yellow', alpha=0.8)
ax.add_artist(sun_circle)
ax.plot(ssb_wrt_sun_position_scaled[:, 0], ssb_wrt_sun_position_scaled[:, 1], color='royalblue')
ax.set_aspect('equal')
ax.grid(True, linestyle='dashed', alpha=0.5)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel('X (Sun Radius)')
ax.set_ylabel('Y (Sun Radius)')
plt.savefig('SSB_WRT_SUN.png', dpi=300)

# Calculate Time Outside the Sun
ssb_distance_scaled = np.linalg.norm(ssb_wrt_sun_position_scaled, axis=1)
ssb_outside_days = len(np.where(ssb_distance_scaled > 1)[0])

print(f"Total Computation Days: {delta_days}")
print(f"SSB Outside Sun Fraction: {100 * ssb_outside_days / delta_days:.2f}%")