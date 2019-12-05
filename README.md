# Using Python on JASMIN: Webinar Example Scripts

A selection of scripts to serve as an example of some of the things that you can
do on JASMIN.

## Using Pandas to process CSV files

Pandas is a really powerful library for creating and manipulating data tables.
With Pandas you can easily read in CSV files, do some processing on them and 
visualise them.

This example uses rainfall data from the UK Met Office Midas Open dataset.

The headers are ignored and the data is read into a Pandas DataFrame. 

Example path: `/badc/ukmo-midas-open/data/uk-hourly-rain-obs/dataset-version-201908/oxfordshire/00605_brize-norton/qc-version-1`

###Usage:

<pre>
usage: csv_pandas.py [-h] [-o OUTPUT] directory
<br>
Generate a plot of yearly, max, mean and min from a series of csv files in the midas open
precipitation timeseries
<br>
positional arguments:
  directory             Directory containing csv files
<br>
optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Directory to output the graph, defaults to the run directory. Default: [.]
</pre>

## Using Xarray to extract timeseries from netCDF

Xarray uses Dask on the backend to parallelise operations and speed up the workflow.
You can use Xarray to work with NetCDF files and extract specific regions and do some processing.

This example uses Xarray to read a timeseries of NetCDF files, extract the UK region and calculate the 
annual mean temperature for each grid box. The result is then written to a new NetCDF file.

Example path: `/badc/cmip6/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/amip/r1i1p1f3/Amon/tas/gn/v20190903`

### Usage:
<pre>
usage: netcdf_xarray.py [-h] [-o OUTPUT] directory
<br>
Extract a time series of annual surface temperature over the UK
<br>
positional arguments:
  directory             Directory containing source files
<br>
optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Directory to output the netcdf file, defaults to the run directory. Default
                        [.]
</pre>


## Using Xarray and matplotlib to plot data

Xarray can also be used with matplotlib to plot data directly. This can be used to 
visualise the data during analysis or as an output.

This example uses xarray to extract a region from a dataset with a specific timestep and plot
the wind variable.

Example path: `/badc/ecmwf-era-interim/data/wa/as/2017/04/04`

### Usage:
<pre>
usage: data_visualisation.py [-h] [--timestep TIMESTEP]
                             [--bbox COORDINATE COORDINATE COORDINATE COORDINATE]
                             directory
<br>
Extract and area and timestamp and plot
<br>
positional arguments:
  directory             Directory containing source files
<br>
optional arguments:
  -h, --help            show this help message and exit
  --timestep TIMESTEP   Options: 0000 0600 1200 1800
  --bbox COORDINATE COORDINATE COORDINATE COORDINATE
                        Format: N,S,E,W
</pre>


## Using python to get a list of files which match your requirements

Python has a suite of useful filepath manipulation tools included with the standard library such
as `os` and `glob`.

The filesystem on JASMIN contains useful metadata about the files at the end of the hierarchy. 
For example the path `/neodc/esacci/sea_ice/data/sea_ice_thickness/L2P/envisat/v2.0/NH/2012/01` contains
useful metadata and is of the format: 

/neodc/esacci/sea_ice/data/`<variable>`/L2P/envisat/v2.0/`<hemisphere>`/`<year>`/`<month>`/*.nc


This example script will start in the directory supplied then proceed to give you a series of options
as to which directory you wish to take next or even all of them. You can then either put the output into a file or
print to the terminal. Before outputting your files, the script will display the glob pattern to get you files using a
linux command.

Example path: `/neodc/esacci/sea_ice/data/`

### Usage:
<pre>
usage: file_listing.py [-h] [-o OUTPUT] directory
<br>
Extract and area and timestamp and plot
<br>
positional arguments:
  directory             Start directory
<br>
optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output list of desired files
</pre>


