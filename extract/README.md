![NSIDC logo](../images/NSIDC_DAAC_2018_smv2.jpg)

# extract

IDL procedures for extracting data from binary files.

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

### extract.pro

IDL program that allows you to open a brightness temperature grid file and read
it into an array, making it available for further manipulation in IDL or to
write to hard disc. After the program has read the user-indicated time range, an
array is returned with a 2-byte integer array of brightness temperatures
expressed in tenths of a kelvin (0.1 K). For example, a value of 2358 translates
to 235.8 K.

To use `extract.pro`, start an IDL repl (`idl`):

```
$ idl
IDL Version 8.3 (linux x86_64 m64). (c) 2013, Exelis Visual Information Solutions, Inc.
Installation number: xxx-xxxx.
Licensed for use by: University of Colorado - Boulder (MAIN)

IDL>
```

Next, compile `extract.pro` with the `.RUN` command:

```
$ idl
IDL> .RUN extract.pro
% Compiled module: REVERSE_STRING_FIND.
% Compiled module: GET_SATELLITE.
% Compiled module: GET_PROCESSING_TYPE.
% Compiled module: GET_DATES.
% Compiled module: GET_CHANNEL.
% Compiled module: GET_HEMISPHERE.
% Compiled module: GET_DIR.
% Compiled module: DATE_INCREMENT.
% Compiled module: GET_TB_FILE_LIST.
% Compiled module: READ_DATA_FILE.
% Compiled module: GET_IMAGE_SIZE.
% Compiled module: EXTRACT.
```

Finally, use the `EXTRACT` procedure to read data into an array (`data`). The
user will be prompted to provide information on which files to pull data
from. Once complete, `data` will be populated with values from files found in
the user-supplied data directory:

```
IDL> EXTRACT, data
Enter start and end dates (yyyymmdd, e.g., 19950610).
Start Date: 20210101
End Date: 20210909
Enter the satellite number (e.g., 8, 11, 13, or 17)
: 17
Enter the channel to be extracted
 1   2   3   4   5   6   7
--- --- --- --- --- --- ---
19V 19H 22V 37V 37H 91V 91H
Enter position of parameter (1-7)
: 5
Enter the hemisphere (1 = northern)
                     (2 = southern)
: 1
Enter the full name of the directory that the Tb files are in.
(Note: must correctly use upper and lower case letters.)
: /path/to/data/on/disk/
IDL> size(data)
           2         304         448           2      136192
```

### extract_ice.pro

TODO

## License

See [LICENSE](../LICENSE).


## Code of Conduct

See [Code of Conduct](../CODE_OF_CONDUCT.md).


## Credit

This software was developed by the NASA National Snow and Ice Data Center
Distributed Active Archive Center.
