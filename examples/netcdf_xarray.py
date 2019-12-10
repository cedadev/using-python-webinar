# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '03 Dec 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import xarray as xr
import argparse
import os
import glob


def extract_uk_timeseries(files):
    """
    Extract the uk region from a series of NetCDF files
    :param files:
    :return:
    """

    # UK coordinates
    min_lon, max_lon = -12, 3
    min_lat, max_lat = 48, 60

    # Open all files into one dataset
    with xr.open_mfdataset(files, combine='by_coords') as ds:

        # Reassign the longitude coordinates to give a -180:180 grid instead
        # of 0:360
        ds = ds.roll(lon=(ds.dims['lon'] // 2), roll_coords=True)

        new_lons = ds.lon.values[:]
        new_lons[:ds.dims['lon'] // 2] = new_lons[:ds.dims['lon'] // 2] - 360
        ds = ds.assign_coords(lon=new_lons)

        # Select the UK coordinates
        uk_region = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))

    return uk_region


def parse_args():
    """
    Parse command line arguments
    :return: Command line arguments object
    """
    parser = argparse.ArgumentParser(
        description='Extract a time series of annual surface temperature over the UK')

    # Add command line arguments
    parser.add_argument('directory',
                        help='Directory containing source files')

    parser.add_argument('-o', '--output',
                        help='Directory to output the netcdf file, defaults to the run directory. Default [.]',
                        default='.')

    return parser.parse_args()


def main():
    """
    Main script
    """

    args = parse_args()

    files = glob.glob(os.path.join(args.directory, '*.nc'))

    uk_region = extract_uk_timeseries(files)

    # Resample to get average annual temperature
    uk_region = uk_region.resample(time='1Y').mean()

    # Write the output
    output_path = os.path.join(args.output, 'uk_annual_tas.nc')
    uk_region.to_netcdf(output_path)

if __name__ == '__main__':
    main()




