"""
nc2bin_nsidc0001.py

Convert a version 6.0 NSIDC-0001 netCDF file
to the version 5.0 equivalent raw binary files

usage:
    python nc2bin_nsidc0001.py <nc_filename>

    Example: for 1991-12-15

        python nc2bin_nsidc0001.py NSIDC0001_TB_PS_N25km_19911215_v6.0.nc

    Output:  for 1991-12-15

        tb_f08_19911215_v5_n19h.bin
        tb_f08_19911215_v5_n19v.bin
        tb_f08_19911215_v5_n22v.bin
        tb_f08_19911215_v5_n37h.bin
        tb_f08_19911215_v5_n37v.bin
        tb_f11_19911215_v5_n19h.bin
        tb_f11_19911215_v5_n19v.bin
        tb_f11_19911215_v5_n22v.bin
        tb_f11_19911215_v5_n37h.bin
        tb_f11_19911215_v5_n37v.bin
"""
import datetime as dt
import os
import re
import sys

import numpy as np
from netCDF4 import Dataset




def get_version_string(fn, default_version=5):
    """Derive the (major) version number to use from the filename"""
    ver_expr = re.findall('v\d{1,1}', fn)[0]
    if len(ver_expr) == 2:
        return ver_expr
    else:
        print(f'Using default version: {default_version}')
        return f'v{default_version}'


def extract_raw_binary_files(fn):
    """Extract the original (v5) filenames for the raw binary files"""
    # Open netCDF file
    try:
        ds = Dataset(fn)
        ds.set_auto_maskandscale(False)  # don't unpack data when reading, use actual array
    except OSError:
        raise RuntimeError(f'ERROR: file is not netCDF: {fn}')

    # Determine date of date in file
    data_datestring = dt.datetime.strptime(
        ds.getncattr('time_coverage_start')[:10],
        '%Y-%m-%d').date().strftime('%Y%m%d')

    # Determine data hemisphere
    crs_name = ds.variables['crs'].getncattr('long_name')

    if '_NH_' in crs_name:
        hem = 'n'
    elif '_SH_' in crs_name:
        hem = 's'

    version_string = get_version_string(fn)

    # Extract all TB fields in this netCDF data set
    for sat in ds.groups.keys():
        for tbfield in ds.groups[sat].variables.keys():
            chan = tbfield[-3:].lower()
            ofn = f'tb_{sat.lower()}_{data_datestring}_{version_string}_{hem}{chan}.bin'

            tbdata = np.array(ds.groups[sat].variables[tbfield])

            tbdata.tofile(ofn)
            print(f'  Wrote: {ofn}')


if __name__ == '__main__':
    try:
        ifn = sys.argv[1]
    except IndexError:
        raise RuntimeError('ERROR: No filename (first argument) given.')

    if not os.path.isfile(ifn):
        raise RuntimeError(f'ERROR: File does not exist: {ifn}')

    extract_raw_binary_files(ifn)
