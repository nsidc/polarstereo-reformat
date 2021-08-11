#!/bin/bash

# nc2bin_nsidc0001.sh

# Simple script to extract any binary files from a netCDF file

fn_nc=$1

if [ -z "$fn_nc" ]; then
  echo "Usage: nc2bin_nsidc0001.sh <NSIDC0001_netCDF_filename>"
  echo "  e.g.:"
  echo "    ./nc2bin_nsidc0001.sh ./NSIDC0001_TB_PS_N12.5km_20071231_v6.0.nc" 
else
  echo " "
  echo "Extracting binary files from:"
  echo "  $fn_nc"
fi

# This simply executes a brute force approach to attempt to extract all
# possible TB fields from this file

[[ ${fn_nc} == *"_N25km_"* ]] && hemres=nhlo
[[ ${fn_nc} == *"_N12.5km_"* ]] && hemres=nhhi
[[ ${fn_nc} == *"_S25km_"* ]] && hemres=shlo
[[ ${fn_nc} == *"_S12.5km_"* ]] && hemres=shhi

echo "  hemres: ${hemres}"

base_fn=$(basename "$fn_nc")

echo "  base_fn: ${base_fn}"

# Determine date from filename
file_dstr=$(basename "$fn_nc" | sed -n "s/^.*_\([[:digit:]]\{8,8\}\)_.*$/\1/p")
echo "  file date string: ${file_dstr}"

# Set which sat and chan to search for
declare -a satlist=(f08 f11 f13 f17 f18)
if [[ $hemres == *"lo" ]]; then
  declare -a chanlist=(19h 19v 22v 37h 37v)
elif [[ $hemres == *"hi" ]]; then
  declare -a chanlist=(85h 85v 91h 91v)
fi

hem=${hemres:0:1}

# Determine version string from filename
# NOTE: Only major version number is used
file_vstr=$(basename "$fn_nc" | sed -n "s/^.*_\(v[[:digit:]]\{1,1\}\).*$/\1/p")
echo "  file version string: ${file_vstr}"

# Set a dummy filename.  This is needed by ncks, but is deleted later.
dummy_fn=ncdummyfile.nc

# Run through all possible combinations of sat and chan
echo "  hem: $hem"
echo " "

for sat in "${satlist[@]}"; do
  #echo "Checking for sat: $sat"
  echo "Checking for sat: $sat  channels: ${chanlist[*]}"
  #echo "  chanlist: ${chanlist[*]}"
  capsat=$(echo "$sat" | tr "[:lower:]" "[:upper:]")
  for chan in "${chanlist[@]}"; do
    #echo "    $chan"
    capchan=$(echo "$chan" | tr "[:lower:]" "[:upper:]")

    ofn=tb_${sat}_${file_dstr}_${file_vstr}_${hem}${chan}.bin
    #echo "    $ofn"

    TBvarname=TB_${capsat}_${capchan}

    # Attempt to extract, ignoring error
    stdout_str=$(ncks -C -O -v "$TBvarname" -b "$ofn" "$fn_nc" "$dummy_fn" 2>&1)

    if [ -z "$stdout_str" ]; then
      # Empty ncks string, therefore the command ran without error
      echo "    $ofn"
    fi

  done
done
  
# Remove the dummy netcdf file created by 'ncks'
rm "$dummy_fn"
