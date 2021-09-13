![NSIDC logo](../images/NSIDC_DAAC_2018_smv2.jpg)

# extract_ice.pro

IDL program for extracting sea ice concentrations from Polar Stereographic grid
files.

## Level of Support

<b>This directory is fully supported by the NSIDC DAAC</b>. If you discover any problems or
bugs, please submit an Issue. If you would like to contribute to this
repository, you may fork the repository and submit a pull request.

See the [LICENSE](../LICENSE) for details on permissions and warranties. Please
contact nsidc@nsidc.org for more information.


## Requirements

The procedures defined in this directory require the Interactive Data Language
(IDL), which requires a license to install and use.


## Installation

Please see
[this](https://www.l3harrisgeospatial.com/Support/Self-Help-Tools/Help-Articles/Help-Articles-Detail/ArtMID/10220/ArticleID/23920/Install-and-License-IDL-88)
documentation page for more information on how to install IDL on your system.


## Usage

First, start an IDL repl (`idl`):

```
$ idl
IDL Version 8.3 (linux x86_64 m64). (c) 2013, Exelis Visual Information Solutions, Inc.
Installation number: xxx-xxxx.
Licensed for use by: University of Colorado - Boulder (MAIN)

IDL>
```

Next, compile `extract_ice.pro` with the `.RUN` command:

```
$ idl
IDL> .RUN extract_ice.pro
% Compiled module: GET_PROCESSING_TYPE.
% Compiled module: GET_TIME_RESOLUTION.
% Compiled module: GET_DATES.
% Compiled module: GET_ALGORITHM.
% Compiled module: GET_HEMISPHERE.
% Compiled module: GET_DIR.
% Compiled module: GET_ESMR_THRESHOLD.
% Compiled module: GET_SATELLITE_NUMBER.
% Compiled module: DATE_INCREMENT.
% Compiled module: GET_ICE_FILE_LIST.
% Compiled module: GET_MONTHLY_FILE_LIST.
% Compiled module: GET_ESMR_FILE_LIST.
% Compiled module: GET_ESMR_MONTHLY_FILE_LIST.
% Compiled module: GET_ESMR_MEANS_FILE_LIST.
% Compiled module: READ_DATA_FILE.
% Compiled module: GET_IMAGE_SIZE.
% Compiled module: EXTRACT_ICE.
```


Once `extract_ice.pro` has been compiled, run the `EXTRACT_ICE` procedure and
follow the prompts to select and read data from files on disk into an array. In
the following example, a directory containing a NASA Team (`nt`) binary file
from [NSIDC-0051](https://nsidc.org/data/nsidc-0051) is loaded into a
`conc_data` array:

```
IDL> EXTRACT_ICE, conc_data
Enter the processing type (1 = SSM/I)
                          (2 = ESMR)
: 1
Enter the time resolution (1 = daily)
                          (2 = monthly)
: 1
Enter start and end dates (yyyymmdd, e.g., 19950610).
Start Date: 20200101
End Date: 20201231
Enter the hemisphere (1 = northern)
                     (2 = southern)
: 2
Enter the full name of the directory that the sea ice files are in.
(Note: directory names are case-sensitive.)
: /path/to/data/on/disk/
Enter the satellite number (e.g., 7, 8, 11, 13, or 17)
: 17
Enter the algorithm (1 = NASATeam)
                    (2 = Bootstrap)
: 1
You selected the NASATeam algorithm
/path/to/data/on/disk/nt_20201126_f17_v1.1_s.bin
IDL> n_elements(conc_data)
      104912
```

## License

See [LICENSE](../LICENSE).


## Code of Conduct

See [Code of Conduct](../CODE_OF_CONDUCT.md).


## Credit

This software was developed by the NASA National Snow and Ice Data Center
Distributed Active Archive Center.
