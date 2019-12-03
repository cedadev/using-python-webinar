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


def process_csv(filename, header_line):
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
    date = df.ob_date.min()
    year = parse(date).year

    return pd.DataFrame(
        {'year': [year], 'min': [min_p], 'max': [max_p], 'mean':[mean_p]},
        columns=['min', 'max','mean'],
        index=[year]
    )


if __name__ == '__main__':

    import argparse
    import os
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(
        description='Generate a plot of yearly, max, mean and '
                    'min from a series of csv files in the midas open'
                    'precipitation timeseries')

    # Add command line arguments
    parser.add_argument('directory',
                        help='Directory containing csv files')

    parser.add_argument('-o',
                        help='Directory to output the graph, defaults to the run directory',
                        default='.')

    args = parser.parse_args()

    # Remove trailing path seperator
    if args.directory.endswith(os.path.sep):
        args.directory = args.directory[:-1]

    # Get a list of all the csv files in the directory
    files = os.listdir(args.directory)

    # Join the directory to the filenames
    files = [os.path.join(args.directory, file) for file in files]

    # Filter files to make sure they they are all csv files
    files = filter(lambda x: os.path.isfile(x), files)

    precip_ts = pd.DataFrame(columns=['min','max','mean'])

    for file in files:

        # Extract the annual values from the file
        annual_data = process_csv(file, 61)

        # Merge the extracted dataframe into the timeseries
        precip_ts = precip_ts.append(annual_data)

    # Extract the start and end years
    min_year = precip_ts.index.min()
    max_year = precip_ts.index.max()

    # Get the station name
    station_name = os.path.basename(
        os.path.dirname(args.directory)
    )

    # Plot the timeseries
    precip_ts.plot()
    plt.title(f'Annual Precipitation from {min_year} to {max_year}: {station_name}')

    # Create the plot output filename
    filename = f'{station_name}_precipitation_{min_year}_{max_year}.png'

    # Save the plot
    plt.savefig(filename)

