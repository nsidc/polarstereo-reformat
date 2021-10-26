![NSIDC logo](/images/NSIDC_DAAC_2018_smv2.jpg)

# nsidc0081

Scripts for converting Near-Real-Time DMSP SSMIS Daily Polar Gridded Sea Ice Concentrations, Version 2 NetCDF data to the original binary format from earlier versions.

## Level of Support

<b>This directory is fully supported by the NSIDC DAAC</b>. If you discover any problems or
bugs, please submit an Issue. If you would like to contribute to this
repository, you may fork the repository and submit a pull request.

See the [LICENSE](../LICENSE) for details on permissions and warranties. Please
contact nsidc@nsidc.org for more information.

## Requirements

This package requires:
* [`netcdf4`](https://unidata.github.io/netcdf4-python/) python library

These requirements are also included in the provided `environment.yml` file,
which can be used with [conda](https://docs.conda.io/en/latest/) to install the
requirements into a `conda` environment.

## Installation

It is reccomended to install the requirements for the included scripts with `conda`:

```
$ conda env create -f environment.yml
$ conda activate nsidc0081
```

## Usage

The `nsidc0081` directory contains a python script which converts [Near-Real-Time DMSP SSMIS Daily Polar Gridded Sea Ice Concentrations, Version 2](https://nsidc.org/data/nsidc-0081) 
NetCDF data to the original binary format from earlier versions. The script is written in `python`.

The script takes the path to an NetCDF file as an argument and produces
binary files corresponding to sea ice concentration estimates from DMSP satellite (e.g., `f16`, `f17`, `f18`) contained in the NetCDF file.

The script produces outputs in the directory from which the program was invoked.

#### Python script

Requires `netcdf4` python library.


```
$ python nc2bin_nsidc0081.py /path/to/existing/netcdf/NSIDC0081_SEAICE_PS_N25km_20211101_v2.0.nc 
  Wrote: ./nt_20211101_f16_nrt_n.bin
  Wrote: ./nt_20211101_f17_nrt_n.bin
  Wrote: ./nt_20211101_f18_nrt_n.bin
$ python nc2bin_nsidc0081.py /path/to/existing/netcdf/NSIDC0081_SEAICE_PS_S25km_20211101_v2.0.nc 
  Wrote: ./nt_20211101_f16_nrt_s.bin
  Wrote: ./nt_20211101_f17_nrt_s.bin
  Wrote: ./nt_20211101_f18_nrt_s.bin
```

## License

See [LICENSE](../LICENSE).

## Code of Conduct

See [Code of Conduct](../CODE_OF_CONDUCT.md).

## Credit

This software was developed by the NASA National Snow and Ice Data Center Distributed Active Archive Center.
