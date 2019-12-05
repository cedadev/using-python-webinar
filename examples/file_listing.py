# encoding: utf-8
"""
Traverse the filesystem and get all the files of interest
"""
__author__ = 'Richard Smith'
__date__ = '04 Dec 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


import os
import glob

def get_options(path):

    # Initialise empty list
    dirs = []

    # Expand any '*' characters
    items = glob.glob(path)

    items = [x for x in items if os.path.isdir(x)]

    # Loop through directories and retrieve contents
    # Scandir is a lightweight way to scan the file system
    for directory in items:
        dirs.extend(os.scandir(directory))

    # Filter list to only include directories
    # Have used a set to filter out any duplicates
    dirs = {x.name for x in dirs if x.is_dir()}

    return sorted(dirs)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='Extract and area and timestamp and plot')

    # Add command line arguments
    parser.add_argument('directory',
                        help='Start directory')
    parser.add_argument('-o', '--output',
                        help='Output list of desired files')

    args = parser.parse_args()

    # Put the start directory in a list to build the selected path
    path = [args.directory]

    # Get the first options *path turns list
    # into a set of arguments for the function
    print(os.path.join(*path))
    options = get_options(os.path.join(*path))

    while options:

        # Base string for the user input
        text_options = "Please select an numbered option from the list:\n"

        # Automatically select the first option where there is only 1
        if len(options) == 1:
            value = 0

        else:

            # Add an option to select all items in the directory
            options.insert(0, '*')

            # Loop options and create a string to ask user to select
            for i, option in enumerate(options):
                text_options += f'{i}) {option}\n'

            value = input(text_options)

        # Select the option from the list and add to the path
        path.append(options[int(value)])

        # Get next options
        options = get_options(os.path.join(*path))

    # Generate the glob pattern
    glob_pattern = os.path.join(*path, '*.nc')

    # Display linux command to get the required files
    print(f'Command to get selected files: ls -l {glob_pattern}\n')

    # Get list of files that match your request
    files = glob.glob(glob_pattern)

    # Output to file if -o option set
    if args.output:
        with open(args.output, 'w') as writer:

            writer.writelines(map(lambda x: x+'\n', files))

    else:
        for file in files:
            print(file)
