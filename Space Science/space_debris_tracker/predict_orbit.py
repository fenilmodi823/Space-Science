from sgp4.api import Satrec, jday
import datetime
import os

def read_tle(filename="tle_data.txt", satellite_index=0):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)

    with open(filepath, "r") as file:
        lines = file.readlines()

    # Remove blank lines
    lines = [line.strip() for line in lines if line.strip() != '']

    line0 = lines[satellite_index * 3 + 0]
    line1 = lines[satellite_index * 3 + 1]
    line2 = lines[satellite_index * 3 + 2]

    satellite = Satrec.twoline2rv(line1, line2)
    return satellite

def propagate_satellite(satellite, minutes=90):
    positions = []
    now = datetime.datetime.now(datetime.UTC)

    for minute in range(0, minutes):
        future_time = now + datetime.timedelta(minutes=minute)

        year = future_time.year
        month = future_time.month
        day = future_time.day
        hour = future_time.hour
        minute_part = future_time.minute
        second = future_time.second

        jd, fr = jday(year, month, day, hour, minute_part, second)
        e, r, v = satellite.sgp4(jd, fr)

        if e == 0:
            positions.append(r)
        else:
            positions.append((None, None, None))

    return positions

if __name__ == "__main__":
    sat = read_tle()
    positions = propagate_satellite(sat)
    for pos in positions[:5]:
        print(pos)
