"""
reconstruct_0081.py

Sample usage:
    python reconstruct_0081.py NSIDC0081_SEAICE_PS_N25km_20210828_v2.0.nc
    python reconstruct_0081.py NSIDC0081_SEAICE_PS_S25km_20210828_v2.0.nc

If the original binary files are placed in subdir orig/ and the output of
this code is placed in a directory called checkfiles/ then simple bash
loops to check pre-existing orig/ and these checkfiles/ might be:

    for d in 20210828 20210829; do
        echo " ";
      echo "$d"
      for h in n s; do
        echo "  Hemisphere: $h";
        for sat in f16 f17 f18; do
          binfn="nt_${d}_${sat}_nrt_${h}.bin"
          echo "    $binfn";
          cmp -l orig/${binfn} checkfiles/${binfn}
        done
        echo " "
      done
    done

"""

import os
import re
import sys
import numpy as np
from netCDF4 import Dataset


outdir = './'
os.makedirs(outdir, exist_ok=True)

fn0081_ = 'nt_{ymd}_{sat}_nrt_{h}.bin'


def get_fndate(fn):
    ymd = re.findall(r'\d{7,8}', fn)[0]

    return ymd


def extract_orig_0081(ifn):
    if 'N25' in ifn:
        hemlet = 'n'
    elif 'S25' in ifn:
        hemlet = 's'
    else:
        raise RuntimeError(f'Could not find N25 or S25 in fn: {ifn}')

    fndate = get_fndate(ifn)

    ds = Dataset(ifn, 'r')
    ds.set_auto_maskandscale(False)

    for sat in ('F16', 'F17', 'F18'):
        varname = f'{sat}_ICECON'

        var = ds.variables[varname]
        vals = np.array(var).astype(np.uint8).flatten()

        ofn = os.path.join(
            outdir,
            fn0081_.format(
                ymd=fndate,
                sat=sat.lower(),
                h=hemlet))

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
        print('Usage: python reconstruct_0081.py <fn>')
        raise RuntimeError('No filename given')
    except AssertionError:
        print(f'Not a file: {ifn}')
        raise RuntimeError('Given filename is not a file')

    extract_orig_0081(ifn)
