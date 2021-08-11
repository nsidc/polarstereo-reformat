Polar Stereographic Reading, Reformatting, and Visualizing
---

Scripts for working with NSIDC data in polar stereographic projections.

# nsidc0001

## Python script

Requires `netcdf4` python library.

Usage:


```
$ python nsidc0001/nc2bin_nsidc0001.py /path/to/existing/netcdf/NSIDC0001_TB_PS_N12.5km_20080101_v6.0.nc
  Wrote: tb_f13_20080101_v6_n85h.bin
  Wrote: tb_f13_20080101_v6_n85v.bin
  Wrote: tb_f17_20080101_v6_n91h.bin
  Wrote: tb_f17_20080101_v6_n91v.bin
```

Produces output files to the directory in which the program was invoked from.

## Bash script

Requires `nco` package.

Usage:

```
$ ./nsidc0001/nc2bin_nsidc0001.sh /path/to/existing/netcdf/NSIDC0001_TB_PS_N12.5km_20080101_v6.0.nc
```

Produces binary files for each channel in the netcdf file to the directory from
which the script is run. In the above case,

```
tb_f13_20080101_v6_n85h.bin
tb_f13_20080101_v6_n85v.bin
tb_f17_20080101_v6_n91h.bin
tb_f17_20080101_v6_n91v.bin
```
