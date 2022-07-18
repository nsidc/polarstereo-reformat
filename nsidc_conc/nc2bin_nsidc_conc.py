"""
nc2bin_nsidc_conc.py

Converts NSIDC sea ice concentration fields from netCDF files -- currently
  NSIDC-0051 and NSIDC-0081 -- to their legacy-equivalent raw binary file
  names

Sample usage:
    python nc2bin_conc.py NSIDC0051_SEAICE_PS_N25km_20210828_v2.0.nc
    python nc2bin_conc.py NSIDC0051_SEAICE_PS_S25km_20210828_v2.0.nc

    python nc2bin_conc.py NSIDC0081_SEAICE_PS_N25km_20210828_v2.0.nc
    python nc2bin_conc.py NSIDC0081_SEAICE_PS_S25km_20210828_v2.0.nc

    python nc2bin_conc.py NSIDC0051_SEAICE_PS_N25km_202108_v2.0.nc
    python nc2bin_conc.py NSIDC0051_SEAICE_PS_S25km_202108_v2.0.nc

    python nc2bin_conc.py NSIDC0081_SEAICE_PS_N25km_202108_v2.0.nc
    python nc2bin_conc.py NSIDC0081_SEAICE_PS_S25km_202108_v2.0.nc

Input files can be:
    0051 or 0081
    daily or monthly
    NH or SH
"""

import re
import sys
from pathlib import Path

import numpy as np
from netCDF4 import Dataset


def get_fnver(prodid, fn):
    # Extract the version string from the filename
    # Assumes filename of the form "..._v?[.?].nc"
    # Note: NRT products will return version string 'nrt'
    if prodid == 'nsidc0081':
        verstr = 'nrt'
    else:
        vstr_loc = fn.find('_v')
        endstr = fn[vstr_loc:]
        verstr = endstr.replace('.nc', '')[1:]

    return verstr


def get_fndate(fn):
    # Extract the datestring of the filename: YYYYMMDD or YYYYMM
    try:
        # Attempt to file YYYYMMDD (daily)
        datestr = re.findall(r'\d{7,8}', fn)[0]
    except IndexError:
        # If no daily datestring found, try to find monthly (YYYYMM)
        try:
            datestr = re.findall(r'\d{5,6}', fn)[0]
        except IndexError:
            raise RuntimeError(
                f'Unable to find YYYYMMDD or YYYYMM in filename: {fn}')

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


def get_prodid(fn):
    # Determine which NSIDC product is being used
    #  Currently NSIDC-0051 and NSIDC-0081 are supported
    prodid_dict = {
        'nsidc0051': 'NSIDC0051',
        'nsidc0081': 'NSIDC0081',
    }

    prod_id = None
    for key in prodid_dict.keys():
        val = prodid_dict[key]
        if val in fn:
            prod_id = key

    if prod_id is None:
        error_message = f"""
        Product ID cannot be determined
            File name: {fn}
            valid product ids: {prodid_dict.keys()}
        """
        raise RuntimeError(error_message)

    return prod_id


def get_legacy_fn_template(prodid):
    # Return a string template for the filename for this product id
    # Note: for 0081, 'verstr' should evaluate to 'nrt' instead of a 
    #       numbered version
    legacy_fn_templates = {
        'nsidc0051': 'nt_{datestr}_{sat}_{verstr}_{h}.bin',
        'nsidc0081': 'nt_{datestr}_{sat}_{verstr}_{h}.bin',
    } 
    try:
        fn_template = legacy_fn_templates[prodid]
    except KeyError:
        raise RuntimeError(f'No legacy filename template for prodid {prodid}')

    return fn_template


def extract_legacy_conc(ifn, outdir):
    # Writes the legacy-format-equivalent output file for each ICECON field
    
    prod_id = get_prodid(ifn)
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

        vals = np.array(var).astype(np.uint8).flatten()

        ofn = Path(outdir) / \
            fn_template.format(
                datestr=fndate,
                sat=sat.lower(),
                h=hemlet,
                verstr=verstr,
            )

        hdr = ds.variables[varname].legacy_binary_header

        outbytes = np.concatenate(
            (hdr.flatten(), vals)
        )

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

    # Filename template
    # fn0051_ = 'nt_{datestr}_{sat}_{verstr}_{h}.bin'

    outdir = Path('./extracted_bins')
    outdir.mkdir(parents=True, exist_ok=True)
    print(f'Writing extracted output to directory: {outdir}')

    extract_legacy_conc(str(ifn), outdir)
