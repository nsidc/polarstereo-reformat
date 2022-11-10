"""
nc2bin_tb.py

From a NSIDC brightness temperature netCDF file -- eg NSIDC0001 or
NSIDC-0080 -- extract the tb fields and output in legacy format

Sample usage:
    python nc2bin_tb.py <nc_filename>

"""
import datetime as dt
import re
import sys
from pathlib import Path

import numpy as np
from netCDF4 import Dataset


def get_version_string(prodid, fn, default_version=5):
    """
    Derive the (major) version number to use from the filename
    This expects the version to be all digits and decimal point between
    the letter 'v' and the extension '.nc'

    If product ID is 0080 (NRT TBs), then verstr is 'nrt'
    """
    print(f'in get_version_string(), prodid: {prodid}')
    if prodid == 'nsidc0080':
        ver_string = 'nrt'
    else:
        fn_str = str(fn)
        print(f're.findall: {re.findall("v(.*?).nc", fn_str)}')
        ver_string = f"v{re.findall('v(.*?).nc', fn_str)[0]}"

    return ver_string


def get_prodid(fn):
    """
    Return the NSIDC product name from this filename or filename string
    """
    if isinstance(fn, str):
        fn_str = fn
    else:
        fn_str = str(fn)

    if 'NSIDC0001' in fn_str:
        prodid = 'nsidc0001'
    elif 'NSIDC0080' in fn_str:
        prodid = 'nsidc0080'
    else:
        raise RuntimeError(f'Product ID not 0001 or 0080: {fn_str}')

    return prodid


def extract_raw_binary_files(fn, outdir):
    """Extract the original (v5) filenames for the raw binary files"""
    # Open netCDF file
    try:
        ds = Dataset(fn)
        ds.set_auto_maskandscale(False)  # don't unpack data when reading, use actual array
    except OSError:
        raise TypeError(f'ERROR: file is not netCDF: {fn}')

    # Determine date of date in file
    data_datestring = dt.datetime.strptime(
        ds.getncattr('time_coverage_start')[:10],
        '%Y-%m-%d').date().strftime('%Y%m%d')

    # Determine data hemisphere from the name of the
    # Coordinate Reference System (crs) variable
    crs_name = ds.variables['crs'].getncattr('long_name')
    if '_NH_' in crs_name:
        hem = 'n'
    elif '_SH_' in crs_name:
        hem = 's'

    prod_id = get_prodid(fn)
    version_string = get_version_string(prod_id, fn)

    # Extract all TB fields in this netCDF data set
    fn_template = 'tb_{sat}_{datestr}_{ver}_{hem}{chan}.bin'
    for sat in ds.groups.keys():
        for tbfield in ds.groups[sat].variables.keys():
            chan = tbfield[-3:].lower()
            ofn = Path(outdir) / \
                fn_template.format(
                    sat=sat.lower(),
                    datestr=data_datestring,
                    ver=version_string,
                    hem=hem,
                    chan=chan
                )


            tbdata = np.array(ds.groups[sat].variables[tbfield])

            tbdata.tofile(ofn)
            print(f'  Wrote: {ofn}')


if __name__ == '__main__':
    try:
        ifn = Path(sys.argv[1])
    except IndexError:
        raise RuntimeError('ERROR: No filename (first argument) given.')
    except AssertionError:
        print(f'Not a file: {ifn}')
        raise RuntimeError('Given filename is not a file')

    try:
        outdir_name = sys.argv[2]
    except IndexError:
        outdir_name = './extracted_bins'
    outdir = Path(outdir_name)
    outdir.mkdir(parents=True, exist_ok=True)
    print(f'Extracting legacy-format files to: {outdir_name}')

    extract_raw_binary_files(ifn, outdir)
