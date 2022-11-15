![NSIDC logo](/images/NSIDC_logo_2018_poster-1.png)

# Polar Stereographic Reformatting

Python scripts for reformatting specific NSIDC SMMR-SSM/I-SSMIS data products in polar stereographic projections from NetCDF to binary.

## Level of Support

<b>This repository is fully supported by NSIDC.</b> If you discover any problems or
bugs, please submit an Issue. If you would like to contribute to this
repository, you may fork the repository and submit a pull request.

See the [LICENSE](LICENSE) for details on permissions and warranties. Please
contact nsidc@nsidc.org for more information.

## Requirements

The python scripts in this repository require:
* [`python`](https://www.python.org/downloads/) >=v3.9,<4.0
* [`netcdf4`](https://unidata.github.io/netcdf4-python/) python library

These requirements are also included in the provided `environment.yml` file,
which can be used with [conda](https://docs.conda.io/en/latest/) to install the
requirements into a `conda` environment.


## Installation

The requirements for the included scripts can be installed with `conda`:

```
$ conda env create -f environment.yml
$ conda activate ps_nc2bin
```

## Usage

### NSIDC Brightness Temperature Data Sets (nsidc0001 and nsidc0080)

The nc2bin_tb.py `python` script converts [DMSP SSM/I-SSMIS Daily Polar Gridded Brightness Temperatures, Version 6](https://nsidc.org/data/nsidc-0001) and [Near-Real-Time DMSP SSM/I-SSMIS Daily Polar Gridded Brightness Temperatures, Version 2](https://nsidc.org/data/nsidc-0080) NetCDF data to the original binary format used in earlier versions.

The script takes the path to an NetCDF file as an argument and produces binary files corresponding to data from each passive microwave channel (e.g., `n19h`, `s91v`) contained in the NetCDF file.

Each script produces outputs in a directory provided as the second command-line argument or in the directory `./extracted_bins` if no directory name is provided.

#### Python script

Requires `netcdf4` python library.

```
$ python nc2bin_tb.py /path/to/existing/netcdf/NSIDC0001_TB_PS_N12.5km_20080101_v6.0.nc
  Wrote: extracted_bins/tb_f13_20080101_v6_n85h.bin
  Wrote: extracted_bins/tb_f13_20080101_v6_n85v.bin
  Wrote: extracted_bins/tb_f17_20080101_v6_n91h.bin
  Wrote: extracted_bins/tb_f17_20080101_v6_n91v.bin

$ python nc2bin_tb.py /path/to/existing/netcdf/NSIDC0080_TB_PS_S12.5km_20080101_v6.0.nc legacy_tbs
  Wrote: legacy_tbs/tb_f16_20220130_nrt_s19h.bin
  Wrote: legacy_tbs/tb_f16_20220130_nrt_s19v.bin
  Wrote: legacy_tbs/tb_f16_20220130_nrt_s22v.bin
  Wrote: legacy_tbs/tb_f16_20220130_nrt_s37h.bin
  Wrote: legacy_tbs/tb_f16_20220130_nrt_s37v.bin
  Wrote: legacy_tbs/tb_f17_20220130_nrt_s19h.bin
  Wrote: legacy_tbs/tb_f17_20220130_nrt_s19v.bin
  Wrote: legacy_tbs/tb_f17_20220130_nrt_s22v.bin
  Wrote: legacy_tbs/tb_f17_20220130_nrt_s37h.bin
  Wrote: legacy_tbs/tb_f17_20220130_nrt_s37v.bin
  Wrote: legacy_tbs/tb_f18_20220130_nrt_s19h.bin
  Wrote: legacy_tbs/tb_f18_20220130_nrt_s19v.bin
  Wrote: legacy_tbs/tb_f18_20220130_nrt_s22v.bin
  Wrote: legacy_tbs/tb_f18_20220130_nrt_s37h.bin
  Wrote: legacy_tbs/tb_f18_20220130_nrt_s37v.bin
```

### NSIDC Sea Ice Concentration Data Sets (nsidc0051, nsidc0081)

The nc2bin_siconc.py `python` script converts [Sea Ice Concentrations from Nimbus-7 SMMR and DMSP SSM/I-SSMIS Passive Microwave Data, Verson 2](https://nsidc.org/data/nsidc-0051) and [Near-Real-Time DMSP
SSMIS Daily Polar Gridded Sea Ice Concentrations, Version
2](https://nsidc.org/data/nsidc-0081) NetCDF data to the original binary format
from earlier versions.

The script takes the path to a NetCDF file as an argument and produces binary
files corresponding to sea ice concentration estimates from DMSP satellite
(e.g., `f16`, `f17`, `f18`) contained in the NetCDF file.

The script produces outputs in the directory from which the program was invoked.

##### Script usage

Requires `netcdf4` python library.

```
$ python nc2bin_siconc.py /path/to/existing/netcdf/NSIDC0081_SEAICE_PS_N25km_20211101_v2.0.nc 
  Wrote: ./nt_20211101_f16_nrt_n.bin
  Wrote: ./nt_20211101_f17_nrt_n.bin
  Wrote: ./nt_20211101_f18_nrt_n.bin
$ python nc2bin_siconc.py /path/to/existing/netcdf/NSIDC0081_SEAICE_PS_S25km_20211101_v2.0.nc 
  Wrote: ./nt_20211101_f16_nrt_s.bin
  Wrote: ./nt_20211101_f17_nrt_s.bin
  Wrote: ./nt_20211101_f18_nrt_s.bin

$ python nc2bin_siconc.py /path/to/existing/netcdf/NSIDC0051_SEAICE_PS_N25km_19900301_v2.0.nc 
  Wrote: ./nt_19900301_f08_v1.1_n.bin
$ python nc2bin_siconc.py /path/to/existing/netcdf/NSIDC0051_SEAICE_PS_S25km_20201101_v2.0.nc 
  Wrote: ./nt_20201101_f17_v1.1_s.bin
```

## License

See [LICENSE](LICENSE), unless otherwise stated in the README file with each subdirectory.

## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).

## Credit

Credit is provided in the README file within each subdirectory.
