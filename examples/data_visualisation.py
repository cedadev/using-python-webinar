# encoding: utf-8
"""
Use xarray and matplotlib to plot the given timestep and bounding box
"""
__author__ = 'Richard Smith'
__date__ = '04 Dec 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


import xarray as xr
from collections import namedtuple
import os
import glob
import cartopy.crs as ccrs
import argparse

# Need to set backend for use on JASMIN
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt


# Create a BoundingBox object for convenience and make
# it clear what is being used where
BoundingBox = namedtuple(
    'BoundingBox',
    ['max_lat','min_lat','max_lon','min_lon']
)

valid_timesteps = ['0000','0600','1200','1800']


def extract_area(files, bbox):
    """
    Extract the given area from the given files

    :param files: List of one or more files
    :param bbox: The extent of the region of interest (ROI)
    :return: xarray.Dataset
    """

    with xr.open_mfdataset(files, combine='by_coords') as ds:

        # Reassign the longitude coordinates to give a -180:180 grid instead
        # of 0:360
        ds = ds.roll(longitude=(ds.dims['longitude'] // 2), roll_coords=True)

        new_lons = ds.longitude.values[:]
        new_lons[:ds.dims['longitude'] // 2] = new_lons[:ds.dims['longitude'] // 2] - 360
        ds = ds.assign_coords(longitude=new_lons)

        region = ds.sel(
            latitude=slice(bbox.max_lat, bbox.min_lat),
            longitude=slice(bbox.min_lon, bbox.max_lon)
        )

        return region


def check_timestep(value):
    """
    Validation function to check whether the user has supplied a valid timestep
    :param value: user inputted value
    :return:
    """
    if value not in valid_timesteps:
        raise argparse.ArgumentTypeError(f'Invalid timestep. Choose one of {valid_timesteps}')
    return value


def create_bounding_box(coordinates_list):
    """
    Process command line arguments and create a bounding box
    :param coordinates_list: list of strings from command line
    :return: BoundingBox
    """

    # Turn bounding box arguments into integers
    coords = [int(x) for x in coordinates_list]

    # Create the bounding box
    return BoundingBox(*coords)


def parse_args():
    """
    Parse command line arguments
    :return: Argparse object
    """

    parser = argparse.ArgumentParser(
        description='Extract and area and timestamp and plot')

    # Add command line arguments
    parser.add_argument('directory',
                        help='Directory containing source files')

    parser.add_argument('--timestep', type=check_timestep, help='Options: 0000 0600 1200 1800. Default: 0000', default='0000')

    parser.add_argument('--bbox',nargs=4, metavar='COORDINATE', help='Format: N,S,E,W. Default: global', default=[90,-90, 180, -180])

    parser.add_argument('--output', default='.', help='Directory to place the plot. Default: .')

    return parser.parse_args()


def main():
    """
    The main script
    """

    args = parse_args()

    # Get the files to process
    print(f'[INFO] Finding files...')
    files = glob.glob(os.path.join(args.directory, f'*{args.timestep}.nc'))

    bbox = create_bounding_box(args.bbox)

    # Extract the region of interest
    print(f'[INFO] Extracting region of interest: {bbox}')
    roi = extract_area(files, bbox)

    # Plot wind variable
    print(f'[INFO] Generating plot')
    ax = plt.axes(projection=ccrs.PlateCarree())
    roi.WIND.isel(t=0, ht=0).plot.contourf(ax=ax)

    # Set the plot extent to match the ROI
    ax.set_extent([bbox.min_lon, bbox.max_lon, bbox.min_lat, bbox.max_lat])

    # Add coastlines
    ax.coastlines()

    # Output file
    output = os.path.join(args.output, f'{args.timestep}_wind.png')

    # Save plot
    plt.savefig(output)
    print(f'[INFO] Saved output to: {output}')


if __name__ == '__main__':

    main()

