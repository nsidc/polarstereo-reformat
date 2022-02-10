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


outdir = './'
os.makedirs(outdir, exist_ok=True)
verstr = 'v1.1'

fn0051_ = 'nt_{ymd}_{sat}_{verstr}_{h}.bin'


def xwm(m='exiting in xwm'):
    raise SystemExit(m)


def get_fndate(fn):
    ymd = re.findall(r'\d{7,8}', fn)[0]

    return ymd


def extract_orig_0051(ifn):
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
                ymd=fndate,
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
    try:
        ifn = sys.argv[1]
        assert os.path.isfile(ifn)
    except IndexError:
        print(f'Usage: python {Path(__file__).name} <fn>')
        raise RuntimeError('No filename given')
    except AssertionError:
        print(f'Not a file: {ifn}')
        raise RuntimeError('Given filename is not a file')

    extract_orig_0051(ifn)
