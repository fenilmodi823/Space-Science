import os
import numpy as np
import lightkurve as lk
from lightkurve import search_targetpixelfile, TessTargetPixelFile
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

def download_and_unzip(url, extract_to='.'):  
    """Downloads and extracts a ZIP file from the given URL."""
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    os.makedirs(extract_to, exist_ok=True)
    zipfile.extractall(path=extract_to)
    print(f"Files successfully downloaded and extracted to: {extract_to}")

def get_light_curve(target_id, author="kepler", cadence="long", quarter=4):
    """Fetches and processes the light curve for a given target star."""
    pixel_file = search_targetpixelfile(target_id, author=author, cadence=cadence, quarter=quarter).download()
    pixel_file.plot(frame=42)
    lc = pixel_file.to_lightcurve(aperture_mask=pixel_file.pipeline_mask)
    lc.plot()
    flat_lc = lc.flatten()
    flat_lc.plot()
    return flat_lc

def analyze_transit_signal(lc):
    """Finds and analyzes the most prominent transit signal."""
    period = np.linspace(1, 5, 10000)
    bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)
    bls.plot()
    planet_x_period = bls.period_at_max_power
    planet_x_t0 = bls.transit_time_at_max_power
    planet_x_dur = bls.duration_at_max_power
    print(f"Detected period: {planet_x_period}")
    print(f"Transit time: {planet_x_t0}")
    print(f"Transit duration: {planet_x_dur}")
    ax = lc.fold(period=planet_x_period, epoch_time=planet_x_t0).scatter()
    ax.set_xlim(-3, 3)

def load_tess_data(file_path):
    """Loads TESS Target Pixel File and processes it."""
    tpf = TessTargetPixelFile(file_path)
    tpf.plot(frame=42)
    lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)
    lc.plot()
    return lc.flatten()

if __name__ == "__main__":
    # Example usage
    # Download data (update with actual Product Group ID)
    product_group_id = '62323123'
    url = f'https://mast.stsci.edu/api/v0.1/Download/bundle.zip?previews=false&obsid={product_group_id}'
    destination = r'D:\VS Code\Science\Exoplanet Finder'
    download_and_unzip(url, destination)
    
    # Get and analyze Kepler data
    flat_lc = get_light_curve('KIC 6922244')
    analyze_transit_signal(flat_lc)
    
    # Load and analyze TESS data (update with actual file path)
    tess_file = r"D:\VS Code\Science\Exoplanet Finder\MAST_2025-03-07T1630\TESS\tess2019357164649-s0020-0000000309661100-0165-s\tess2019357164649-s0020-0000000309661100-0165-s_tp.fits"
    tess_lc = load_tess_data(tess_file)
    analyze_transit_signal(tess_lc)
