"""
nc2bin_nsidc0051.py

Sample usage:
    python nc2bin_nsidc0051.py NSIDC0051_SEAICE_PS_N25km_20210828_v2.0.nc
    python nc2bin_nsidc0051.py NSIDC0051_SEAICE_PS_S25km_20210828_v2.0.nc

If the original binary files are placed in subdir orig/ and the output of
this code is placed in a directory called checkfiles/ then simple bash
loops to check pre-existing orig/ and these checkfiles/ might be:

    d=19900301
    sat=f08
    binver=v1.1
    echo "$d"
    for h in n s; do
      echo "  Hemisphere: $h";
      binfn="nt_${d}_${sat}_${binver}_${h}.bin"
      echo "    $binfn";
      cmp -l orig/${binfn} checkfiles/${binfn}
    done

    d=20200901
    sat=f17
    binver=v1.1
    echo "$d"
    for h in n s; do
      echo "  Hemisphere: $h";
      binfn="nt_${d}_${sat}_${binver}_${h}.bin"
      echo "    $binfn";
      cmp -l orig/${binfn} checkfiles/${binfn}
    done
"""

import os
import re
import sys
from pathlib import Path

import numpy as np
from netCDF4 import Dataset


def get_fnver(fn):
    # Extract the version string from the filename
    # Assumes filename of the form "..._v?[.?].nc"
    vstr_loc = fn.find('_v')
    endstr = fn[vstr_loc:]
    verstr = endstr.replace('.nc', '')[1:]

    return verstr


def get_fndate(fn):
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


def extract_orig_0051(ifn, outdir, verstr):
    if 'N25' in ifn:
        hemlet = 'n'
    elif 'S25' in ifn:
        hemlet = 's'
    else:
        raise RuntimeError(f'Could not find N25 or S25 in fn: {ifn}')

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

        ofn = os.path.join(
            outdir,
            fn0051_.format(
                datestr=fndate,
                sat=sat.lower(),
                h=hemlet,
                verstr=verstr,
            )
        )

        hdr = ds.variables[varname].legacy_binary_header

        outbytes = np.concatenate(
            (hdr.flatten(), vals)
        )

        outbytes.tofile(ofn)
        print(f'  Wrote: {ofn}')


if __name__ == '__main__':
    outdir = './extracted_bins'
    os.makedirs(outdir, exist_ok=True)

    # Filename template
    fn0051_ = 'nt_{datestr}_{sat}_{verstr}_{h}.bin'

    try:
        ifn = sys.argv[1]
        assert os.path.isfile(ifn)
    except IndexError:
        print(f'Usage: python {Path(__file__).name} <fn>')
        raise RuntimeError('No filename given')
    except AssertionError:
        print(f'Not a file: {ifn}')
        raise RuntimeError('Given filename is not a file')

    # Note: The last version of the raw binary 0051 fns was "v1.1"
    verstr = get_fnver(ifn)

    extract_orig_0051(ifn, outdir, verstr)
