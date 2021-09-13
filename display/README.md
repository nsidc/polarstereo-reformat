![NSIDC logo](../images/NSIDC_DAAC_2018_smv2.jpg)

# disp_ssmi_ice_xa.pro

IDL program for creating animations of sea ice concentrations from SSM/I Polar
Grids.

Supported data products are [NSIDC-0051](https://nsidc.org/data/nsidc-0051), ,
[NSIDC-0079](https://nsidc.org/data/nsidc-0079), and
[NSIDC-0009](https://nsidc.org/data/nsidc-0009).

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
IDL> .RUN disp_ssmi_ice_xa.pro
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
% Compiled module: NASATEAM_COLORBAR.
% Compiled module: BOOTSTRAP_COLORBAR.
% Compiled module: LABEL_NASATEAM_COLORBAR.
% Compiled module: LABEL_BOOTSTRAP_COLORBAR.
% Compiled module: MAKE_COLOR_BAR.
% Compiled module: CREATE_NASATEAM_COLORS.
% Compiled module: CREATE_BOOTSTRAP_COLORS.
% Compiled module: CREATE_TITLE.
% Compiled module: GET_IMAGE_SIZE.
% Compiled module: ANIMATE.
% Compiled module: DISP_SSMI_ICE_XA.
```


Once `disp_ssmi_ice_xa.pro` has been compiled, run the `DISP_SSMI_ICE_XA`
procedure and follow the prompts to select and read data from files on disk and
create an animation. In the following example, a directory containing NASA Team
(`nt`) binary files from [NSIDC-0051](https://nsidc.org/data/nsidc-0051) read
and turned into an animation:

```
IDL> DISP_SSMI_ICE_XA
Enter the processing type (1 = SSM/I)
                          (2 = ESMR)
: 1
Enter the time resolution (1 = daily)
                          (2 = monthly)
: 1
Enter start and end dates for animation (yyyymmdd, e.g., 19950610).
Start Date: 20200101
End Date: 20201231
Enter the hemisphere (1 = northern)
                     (2 = southern)
: 1
Enter the full name of the directory that the sea ice files are in.
(Note: directory name is case-sensitive.)
: /path/to/data/on/disk/
Enter the satellite number (e.g., 7, 8, 11, 13, or 17)
: 17
Enter the algorithm (1 = NASATeam)
                    (2 = Bootstrap)
: 1
You selected the NASATeam algorithm
% Compiled module: XINTERANIMATE.
% Compiled module: XREGISTERED.
% Compiled module: CW_ANIMATE.
% Compiled module: CW_BGROUP.
% Compiled module: COLORMAP_APPLICABLE.
```

## License

See [LICENSE](../LICENSE).


## Code of Conduct

See [Code of Conduct](../CODE_OF_CONDUCT.md).


## Credit

This software was developed by the NASA National Snow and Ice Data Center
Distributed Active Archive Center.
