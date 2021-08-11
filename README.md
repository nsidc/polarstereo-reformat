![NSIDC logo](/images/NSIDC_logo_2018_poster-1.png)

# Polar Stereographic Reading, Reformatting, and Visualizing

Scripts for working with NSIDC data in polar stereographic projections.

## Level of Support

This repository is fully supported by NSIDC. If you discover any problems or
bugs, please submit an Issue. If you would like to contribute to this
repository, you may fork the repository and submit a pull request.

See the [LICENSE](LICENSE) for details on permissions and warranties. Please
contact nsidc@nsidc.org for more information.

## Requirements

This package requires:
* [`netcdf4`](https://unidata.github.io/netcdf4-python/) python library
* [`nco`](https://github.com/nco/nco)

These requirements are also included in the provided `environment.yml` file,
which can be used with [conda](https://docs.conda.io/en/latest/) to install the
requirements into a `conda` environment.

## Installation

It is reccomended to install the requirements for the included scripts with `conda`:

```
$ conda env create -f environment.yml
$ conda activate polar_stereo_tools
```

## Usage

### nsidc0001

The `nsidc0001` directory contains two scripts for converting
[nsidc0001](https://nsidc.org/data/nsidc-0001) netCDF data to binary files, one
written in `python` and the other as a `bash` shell script.

Both scripts take the path to an NSIDC-0001 netCDF file as an argument and
produce binary files corresponding to data from each passive microwave channel
(e.g., `n85h`, `n91v`) contained in the netCDF file.

Both scripts produce outputs in the directory from which the program was invoked.

#### Python script

Requires `netcdf4` python library.


```
$ python nsidc0001/nc2bin_nsidc0001.py /path/to/existing/netcdf/NSIDC0001_TB_PS_N12.5km_20080101_v6.0.nc
  Wrote: tb_f13_20080101_v6_n85h.bin
  Wrote: tb_f13_20080101_v6_n85v.bin
  Wrote: tb_f17_20080101_v6_n91h.bin
  Wrote: tb_f17_20080101_v6_n91v.bin
```

#### Bash script

Requires `nco` package.

```
$ ./nsidc0001/nc2bin_nsidc0001.sh /path/to/existing/netcdf/NSIDC0001_TB_PS_N12.5km_20080101_v6.0.nc
$ ls -l *.bin
-rw-rw-r-- 1 <user> <group> 1089536 Aug 11 16:28 tb_f13_20080101_v6_n85h.bin
-rw-rw-r-- 1 <user> <group> 1089536 Aug 11 16:28 tb_f13_20080101_v6_n85v.bin
-rw-rw-r-- 1 <user> <group> 1089536 Aug 11 16:28 tb_f17_20080101_v6_n91h.bin
-rw-rw-r-- 1 <user> <group> 1089536 Aug 11 16:28 tb_f17_20080101_v6_n91v.bin

```

## License

See [LICENSE](LICENSE).

## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).

## Credit

This software was developed by the National Snow and Ice Data Center with
funding from multiple sources.
