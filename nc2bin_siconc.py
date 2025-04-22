"""
nc2bin_siconc.py

Converts NSIDC sea ice concentration fields from netCDF files -- currently
  NSIDC-0051, NSIDC-0081, NSIDC-0079 -- to their legacy-equivalent
  raw binary file names

Sample usage:
  Daily:
    python nc2bin_siconc.py NSIDC0051_SEAICE_PS_N25km_20210828_v2.0.nc
    python nc2bin_siconc.py NSIDC0051_SEAICE_PS_S25km_20210828_v2.0.nc

    python nc2bin_siconc.py NSIDC0081_SEAICE_PS_N25km_20210828_v2.0.nc
    python nc2bin_siconc.py NSIDC0081_SEAICE_PS_S25km_20210828_v2.0.nc

    python nc2bin_siconc.py NSIDC0079_SEAICE_PS_N25km_20210828_v4.0.nc
    python nc2bin_siconc.py NSIDC0079_SEAICE_PS_S25km_20210828_v4.0.nc

  Monthly:
    python nc2bin_siconc.py NSIDC0051_SEAICE_PS_N25km_202108_v2.0.nc
    python nc2bin_siconc.py NSIDC0051_SEAICE_PS_S25km_202108_v2.0.nc

    python nc2bin_siconc.py NSIDC0081_SEAICE_PS_N25km_202108_v2.0.nc
    python nc2bin_siconc.py NSIDC0081_SEAICE_PS_S25km_202108_v2.0.nc

    python nc2bin_siconc.py NSIDC0079_SEAICE_PS_N25km_202108_v4.0.nc
    python nc2bin_siconc.py NSIDC0079_SEAICE_PS_S25km_202108_v4.0.nc

Input files can be:
    0051, 0081, or 0079
    daily or monthly  (note: the 0081 product does not have files)
    NH or SH
"""

import re
import sys
from pathlib import Path

import numpy as np
from netCDF4 import Dataset


def get_fnver(prod_id, fn):
    # Extract the version string from the filename
    # Assumes filename of the form "..._v?[.?].nc"
    # Note: NRT products will return version string 'nrt'
    if prod_id == 'nsidc0081':
        verstr = 'nrt'
    else:
        vstr_loc = fn.find('_v')
        endstr = fn[vstr_loc:]
        verstr = endstr.replace('.nc', '')[1:]

    return verstr


def get_fndate(fullpath):
    # Extract the datestring of the filename: YYYYMMDD or YYYYMM
    import os

    fn = os.path.basename(fullpath)
    try:
        # Attempt to file YYYYMMDD (daily)
        datestr = re.findall(r'\d{7,8}', fn)[0]
    except IndexError:
        # If no daily datestring found, try to find monthly (YYYYMM)
        try:
            datestr = re.findall(r'\d{5,6}', fn)[0]
        except IndexError:
            print('===========================')
            print('===========================')
            print('bad filename:')
            print(fn)
            print('===========================')
            print('===========================')
            datestr = None

    return datestr


def get_hemlet(fn):
    # Extract the letter designating the hemisphere from the filename
    if 'N25' in fn:
        hemlet = 'n'
    elif 'S25' in fn:
        hemlet = 's'
    else:
        raise RuntimeError(f'Could not find N25 or S25 in fn: {fn}')
    return hemlet


def get_prod_id(fn):
    # Determine which NSIDC product is being used
    #  Currently NSIDC-0051 and NSIDC-0081 are supported
    prod_id_dict = {
        'nsidc0051': 'NSIDC0051',
        'nsidc0081': 'NSIDC0081',
        'nsidc0079': 'NSIDC0079',
    }

    prod_id = None
    for key in prod_id_dict.keys():
        val = prod_id_dict[key]
        if val in fn:
            prod_id = key

    if prod_id is None:
        error_message = f"""
        Product ID cannot be determined
            File name: {fn}
            valid product ids: {prod_id_dict.keys()}
        """
        raise RuntimeError(error_message)

    return prod_id


def get_legacy_fn_template(prod_id):
    # Return a string template for the filename for this product id
    # Note: for 0081, 'verstr' should evaluate to 'nrt' instead of a 
    #       numbered version
    legacy_fn_templates = {
        'nsidc0051': 'nt_{datestr}_{sat}_{verstr}_{h}.bin',
        'nsidc0081': 'nt_{datestr}_{sat}_{verstr}_{h}.bin',
        'nsidc0079': 'bt_{datestr}_{sat}_{verstr}_{h}.bin',
    } 
    try:
        fn_template = legacy_fn_templates[prod_id]
    except KeyError:
        raise RuntimeError(f'No legacy filename template for prod_id {prod_id}')

    return fn_template


def get_bin_dtype(prod_id):
    # Return the data type for the raw binary (legacy) data field
    # for this prod_id
    legacy_dtypes = {
        'nsidc0051': np.uint8,
        'nsidc0081': np.uint8,
        'nsidc0079': np.int16,
    } 
    try:
        legacy_dtype = legacy_dtypes[prod_id]
    except KeyError:
        raise RuntimeError(f'Could not determine dtype for: {prod_id}')

    return legacy_dtype


def product_has_header(prod_id):
    # Returns True if the legacy binary file for this product has a header
    products_with_header = ('nsidc0051', 'nsidc0081')

    return prod_id in products_with_header


def extract_legacy_siconc(ifn, outdir):
    # Writes the legacy-format-equivalent output file for each ICECON field
    
    prod_id = get_prod_id(ifn)
    verstr = get_fnver(prod_id, ifn)
    fn_template = get_legacy_fn_template(prod_id)
    hemlet = get_hemlet(ifn)
    fndate = get_fndate(ifn)

    ds = Dataset(ifn, 'r')
    ds.set_auto_maskandscale(False)

    # sat is first 3 chars of variable of form xxx_ICECON
    sat_list = [key[:3] for key in list(ds.variables.keys()) if 'ICECON' in key]  # noqa

    for sat in sat_list:
        varname = f'{sat}_ICECON'

        try:
            var = ds.variables[varname]
        except KeyError:
            print(f'  No such conc var found: {varname}')
            continue

        bin_dtype = get_bin_dtype(prod_id)

        vals = np.array(var).astype(bin_dtype).flatten()

        ofn = Path(outdir) / \
            fn_template.format(
                datestr=fndate,
                sat=sat.lower(),
                h=hemlet,
                verstr=verstr,
            )

        if product_has_header(prod_id):
            hdr = ds.variables[varname].legacy_binary_header
            outbytes = np.concatenate(
                (hdr.flatten(), vals)
            )
        else:
            outbytes = vals

        outbytes.tofile(ofn)
        print(f'  Wrote: {ofn}')


if __name__ == '__main__':
    try:
        ifn = Path(sys.argv[1])
        assert ifn.is_file()
    except IndexError:
        print(f'Usage: python {Path(__file__).name} <fn>')
        raise RuntimeError('No filename given')
    except AssertionError:
        print(f'Not a file: {ifn}')
        raise RuntimeError('Given filename is not a file')

    outdir = Path('./')
    """
    # Code which can be used to write outputs to a different directory
    outdir = Path('./extracted_bins')
    outdir.mkdir(parents=True, exist_ok=True)
    print(f'Writing extracted output to directory: {outdir}')
    """

    extract_legacy_siconc(str(ifn), outdir)
