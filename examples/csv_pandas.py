# encoding: utf-8
"""
Example python script to show how you can use Pandas and Python to process CSV files and produce plots
"""
__author__ = 'Richard Smith'
__date__ = '03 Dec 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


import pandas as pd
from dateutil.parser import parse
import os
import argparse
import glob
from tqdm import tqdm

# Need to set backend for use on JASMIN
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt


def extract_annual_statistics(filename, header_line):
    """
    Read the csv file and extract the min, max and mean
    precipitation for that year.

    :param filename: file to process
    :param header_line: Start of the csv table
    :return: pandas.DataFrame
    """

    # Read the csv file into a Pandas data frame
    df = pd.read_csv(filename, header=header_line)

    # Select the precipitation column
    precip = df.prcp_amt

    # Extract the min, max and mean annual precipitation amound
    min_p = precip.min()
    max_p = precip.max()
    mean_p = precip.mean()

    # Extract the year of the data from the first timestamp in the file
    date = df.ob_end_time.min()
    year = parse(date).year

    return pd.DataFrame(
        {'year': [year], 'min': [min_p], 'max': [max_p], 'mean':[mean_p]},
        columns=['min', 'max','mean'],
        index=[year]
    )


def get_station_name(directory):
    """
    Takes directory of format:
    /a/b/.../station_name/c

    and returns the station_name

    :param directory:
    :return: station_name
    """

    # Remove trailing path seperator
    if directory.endswith('/'):
        directory = directory[:-1]

    # Extract the directory above
    directory = os.path.dirname(directory)

    # Extract the station name
    station_name = os.path.basename(directory)

    return station_name


def process_files(files):
    """
    Process list of files
    :param files: list of files

    :return: Precipitation time series pandas DataFrame
    """

    precip_ts = pd.DataFrame(columns=['min', 'max', 'mean'])

    for file in tqdm(files, desc='Processing files'):
        # Extract the annual values from the file
        annual_data = extract_annual_statistics(file, 61)

        # Merge the extracted dataframe into the timeseries
        precip_ts = precip_ts.append(annual_data)

    return precip_ts


def parse_args():
    """
    Get the command line arguments
    :return: arguments object
    """

    parser = argparse.ArgumentParser(
        description='Generate a plot of yearly, max, mean and '
                    'min from a series of csv files in the midas open'
                    ' precipitation timeseries')

    # Add command line arguments
    parser.add_argument('directory',
                        help='Directory containing csv files')

    parser.add_argument('-o', '--output',
                        help='Directory to output the graph, defaults to the run directory. Default: [.]',
                        default='.')

    return parser.parse_args()


def main():
    """
    The main script
    """

    # Get command line arguments
    args = parse_args()

    # Get a list of all the csv files in the directory
    files = glob.glob(os.path.join(args.directory, '*.csv'))

    # Extract the precipitation time series
    precip_ts = process_files(files)

    # Extract the start and end years
    min_year = precip_ts.index.min()
    max_year = precip_ts.index.max()

    # Get the station name
    station_name = get_station_name(args.directory)

    # Plot the time series
    print('[INFO] Generating plot of annual precipitation...')
    precip_ts.plot()
    plt.title(f'Annual Precipitation from {min_year} to {max_year}: {station_name}')

    # Create the plot output filename
    filename = f'{station_name}_precipitation_{min_year}_{max_year}.png'

    # Save the plot
    output_path = os.path.join(args.output,filename)
    plt.savefig(output_path)
    print(f'[INFO] Saved output to: {output_path}')


if __name__ == '__main__':

    main()






