# Import necessary modules
import spiceypy
import datetime
import math

# Get today's date and set time to midnight
date_today = datetime.datetime.today().strftime('%Y-%m-%dT00:00:00')
print(f"Today's date (midnight): {date_today}")

# Load SPICE kernels for leapseconds and planetary data
spiceypy.furnsh('../kernels/lsk/naif0012.tls')
spiceypy.furnsh('../kernels/spk/de432s.bsp')


# Compute Ephemeris Time (ET) from UTC
et_today_midnight = spiceypy.utc2et(date_today)
print(f"The Ephemeris Time: {et_today_midnight}")

# Compute Earth's state vector with respect to the Sun
earth_state_wrt_sun, earth_sun_light_time = spiceypy.spkgeo(targ=399, et=et_today_midnight, ref='ECLIPJ2000', obs=10)
print('State vector of the Earth w.r.t. the Sun for "today" (midnight):\n', earth_state_wrt_sun)

# Calculate Euclidean distance between Earth and Sun in km
earth_sun_distance = math.sqrt(sum(earth_state_wrt_sun[i]**2 for i in range(3)))

# Convert distance to astronomical units (AU)
earth_sun_distance_au = spiceypy.convrt(earth_sun_distance, 'km', 'AU')
print('Current distance between the Earth and the Sun in AU:', earth_sun_distance_au)
