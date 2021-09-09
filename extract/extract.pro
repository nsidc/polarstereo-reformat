;===============================================================================
; extract.pro - IDL program for extracting a time series of SSM/I Polar
;               Grids brightness temperature data.
;
; Comments by dscott 09/10/2010
; This program works with Nimbus-5 ESMR Daily Polar Gridded Brightness Temperatures
; (http://nsidc.org/data/nsidc-0077.html) and DMSP SSM/I Daily Polar Gridded Brightness 
; Temperatures (http://nsidc.org/data/nsidc-0001.html) and Near-Real-Time DMSP SSM/I Daily 
; Polar Gridded Brightness Temperatures (http://nsidc.org/data/nsidc-0080.html).
;
;===============================================================================



;-------------------------------------------------------------------------------
; reverse_string_find - work around for IDL removing the function RSTRPOS and
;                       adding keywords to strpos between 5.2 and 5.3
;-------------------------------------------------------------------------------
function reverse_string_find,  line,  token
  ;; fix for RSI's brain dead changing of 5.2 -> 5.3 removal of RSTRPOS
  IF Float(!Version.Release) GT 5.2 THEN $
    loc = call_function("StrPos", line, token, /Reverse_Search) $
  ELSE $
    loc = call_function("RStrPos", line, token)
  return,  loc
end 


;-------------------------------------------------------------------------------
; get_satellite - gets user's choice of satellite (F8, F11, F13, or F17)
;
; Input:
;    none.
;
; Output:
;    none.
;
; Return Value:
;
;-------------------------------------------------------------------------------
function get_satellite

satellite_number = -1
while satellite_number ne 8 and satellite_number ne 11 and $
   satellite_number ne 13 and satellite_number ne 17 do begin
   print, 'Enter the satellite number (e.g., 8, 11, 13, or 17)'
   read, satellite_number
endwhile

return, satellite_number
end


;-------------------------------------------------------------------------------
; get_processing_type - gets user's choice of near real-time or batch.
;
; Input:
;     None.
;
; Output:
;     None.
;
; Return Values:
;     1: near real-time; 2: batch.
;-------------------------------------------------------------------------------
function get_processing_type

prod_type = 0
while (prod_type lt 1 or prod_type gt 2) do begin
    print, 'Enter the processing type (1 = near real-time)'
    print, '                          (2 = polar grids from hard drive)'
    read, prod_type
endwhile

return, prod_type
end


;-------------------------------------------------------------------------------
; get_dates gets the user's start and end dates.
;
; Input:
;     none.
;
; Output:
;     none.
;
; Return Value:
;     the start and end dates in yyyymmdd format.
;-------------------------------------------------------------------------------
function get_dates

dates = {start_date: 0L, $
         end_date: 0L}

i = 0L
print, 'Enter start and end dates (yyyymmdd, e.g., 19950610).'
read, i, PROMPT='Start Date: '
dates.start_date = i
read, i, PROMPT='End Date: '
dates.end_date = i

return, dates
end


;--------------------------------------------------------------------------------
; get_channel - gets user's choice of which channel.
;
; Input:
;     satellite_number - the satellite number (8, 11, 13, or 17).
;
; Output:
;     none.
;
; Return Value:
;     1 - 19GHz Vertical; 2 - 19GHz Horizontal; 3 - 22GHz Vertical;
;     4 - 37GHz Vertical; 5 - 37GHz Horizontal;
;     6 - 85/91GHz Vertical; 7 - 85/91GHz Horizontal
;--------------------------------------------------------------------------------
function get_channel, satellite_number

channel = 0

while (channel lt 1 or channel gt 7) do begin
    print,'Enter the channel to be extracted'
    print,' 1   2   3   4   5   6   7'
    print,'--- --- --- --- --- --- ---'
    if satellite_number eq 8 or satellite_number eq 11 or $
       satellite_number eq 13 then begin
       print,'19V 19H 22V 37V 37H 85V 85H'
    endif else if satellite_number eq 17 then begin
       print,'19V 19H 22V 37V 37H 91V 91H'
    endif
    print,'Enter position of parameter (1-7)'
    read, channel
endwhile

return, channel
end


;--------------------------------------------------------------------------------
; get_hemisphere - gets the user's choice of which hemisphere (northern or
;                  southern).
;
; Input:
;     none.
;
; Output:
;     none.
;
; Return Value:
;     1 - Northern Hemisphere; 2 - Southern Hemisphere
;-------------------------------------------------------------------------------
function get_hemisphere

hemisphere = 0

while (hemisphere lt 1 or hemisphere gt 2) do begin
    print, 'Enter the hemisphere (1 = northern)'
    print, '                     (2 = southern)'
    read, hemisphere
endwhile

return, hemisphere
end


;-------------------------------------------------------------------------------
; get_dir - gets the directory that the NRTSI brightness temperature files
;           are in.
;
; Input:
;     none.
;
; Output:
;     none.
;
; Return Value:
;     the directory name.
;-------------------------------------------------------------------------------
function get_dir

dir_name = ' '
print, 'Enter the full name of the directory that the Tb files are in.'
print, '(Note: must correctly use upper and lower case letters.)'
read, dir_name

return, dir_name
end


;--------------------------------------------------------------------------------
; date_increment - properly increments a date in yyyymmdd format (at least
;                  for the period 1901-2099).
;
; Input/Output:
;     the date in yyyymmdd format.
;
; Effect: changes the date.
;--------------------------------------------------------------------------------
pro date_increment, date

monthLength = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

year = date/10000
month = (date mod 10000)/100
day = date mod 100

day = day + 1
if (day gt monthLength[month-1] and (not((year mod 4) eq 0 and month eq 2 $
                                       and day eq 29))) then begin
    day = 1
    month = month + 1
    if (month eq 13) then begin
        month = 1
        year = year + 1
    endif
endif

date = year*10000 + month*100 + day

end


;--------------------------------------------------------------------------------
; get_Tb_file_list - returns a list of the Tb files for the given date
;                    range and hemisphere from the user-specified
;                    directory.
;
; Input:
;     start_date - the start of the date range in yyyymmdd format.
;     end_date - the end of the date range in yyyymmdd format.
;     channel - 1: 19GHz Vertical; 2: 19GHz Horizontal; 3: 22GHz Vertical;
;               4: 37GHz Vertical; 5: 37GHz Horizontal;
;               6: 85/91GHz Vertical; 7: 85/91GHz Horizontal
;     hemisphere - 1: northern hemisphere; 2: southern hemisphere.
;     dir_name - the name of the directory the sea ice concentration files
;                are in.
;
; Output:
;     none.
;
; Return Value:
;     a list of file names or -1 if there is an error.
;--------------------------------------------------------------------------------
function get_Tb_file_list, start_date, end_date, channel, hemisphere, $
                           dir_name, sat_no


if (start_date gt end_date or hemisphere lt 1 or hemisphere gt 2 or $
    strlen(dir_name) lt 1) then begin
    list_size = 0
    print, 'Not able to generate list of brightness temperature files.'
    goto, FINISH
endif

str_case = -1

if sat_no eq 8 or sat_no eq 11 or sat_no eq 13 then begin
   channel_name = ['19v', '19h', '22v', '37v', '37h', '85v', '85h']
endif else if sat_no eq 17 then begin
   channel_name = ['19v', '19h', '22v', '37v', '37h', '91v', '91h']
endif

hem_name = ['n', 's']

dir_name = dir_name + '/'

result = FINDFILE(dir_name + '*' + STRING(format='(i2.2)', sat_no) + '*' + $
                  hem_name[hemisphere-1] + channel_name[channel - 1] + '*', $
                  count=count)

;
; Loop thru the dates in the date range, construct the file names,
; and append them to the full directory name.
;
cur_date = start_date
list_size = 0
while (cur_date le end_date) do begin

    str_cur_date = STRING(format='(i6.6)', cur_date mod 1000000)
    for r=0,count-1 do begin
        ;
        ; Test to see if the file name contains the current date.
        ;
        if STRPOS(result[r], 'nrt') gt 0 then begin
           offset = 19
        endif else begin
           offset = 18
        endelse
        if STRPOS(result[r], str_cur_date) eq (strlen(result[r]) - offset) $
        then begin
            list_size = list_size + 1
            temp = MAKE_ARRAY(list_size, /STRING)
            if (list_size gt 1) then temp[0:list_size - 2] = file_list
            temp[list_size - 1] = result[r]
            file_list = temp
        endif
    endfor

    ;
    ; Go to the next day.
    ;
    date_increment, cur_date

endwhile

FINISH: if list_size eq 0 then return, ['-1'] else return, file_list
end


;-------------------------------------------------------------------------------
; read_data_file - gets the brightness temperatures from a data file.
;
; Input:
;     path - complete path name of data file.
;     xdim - the X dimension of the data grid.
;     ydim - the Y dimension of the data grid.
;
; Output:
;     status - flag indicating whether the file was succesfully read:
;              1 - was read; 0 - was not read.
;
; Return Value:
;     array containing the brightness temperatures or all zeros if there
;     is an error.
;-------------------------------------------------------------------------------
function read_data_file, path, xdim, ydim, status

status = 0

tmp = INTARR(xdim, ydim)

if (strlen(path) lt 10 or xdim lt 1 or ydim lt 1) then begin
    print, 'Not able to read file ', path
    goto, FINISH
endif

;
; First see if file exists.
;
result = FINDFILE(path, COUNT=count)

if count gt 0 then begin
    ;
    ; File DOES exist.
    ;
    if HDF_ISHDF(path) then begin
        ;
        ; NRTSI data stored in HDF files.
        ;
        DFSD_GETINFO,path,TYPE=type,DIMS=dims
        DFSD_GETDATA,path,tmp
        tmp = rotate(tmp, 7)
    endif else begin
        OPENR, lun, path, /GET_LUN, /SWAP_IF_BIG_ENDIAN
        READU, lun, tmp
        FREE_LUN, lun
    endelse
    status = 1
endif else begin
    ;
    ; File does NOT exist.
    ;
    print, 'File ', path, ' not found.'
    tmp(*,*) = 157
endelse

FINISH:
return, tmp

end


;--------------------------------------------------------------------------------
; get_image_size - returns the dimensions of a brightness temperature
;                  array.
;
; Input:
;     channel - 1: 19GHz Vertical; 2: 19GHz Horizontal; 3: 22GHz Vertical;
;               4: 37GHz Vertical; 5: 37GHz Horizontal;
;               6: 85/91GHz Vertical; 7: 85/91GHz Horizontal
;     hemisphere - 1: northern hemisphere; 2: southern hemisphere.
;
; Output:
;     xdim - the number of columns or -1 if there is an error.
;     ydim - the number of rows or -1 if there is an error.
;--------------------------------------------------------------------------------
pro get_image_size, channel, hemisphere, xdim, ydim

if (channel ge 1 and channel le 7 and hemisphere ge 1 and hemisphere le 2) $
  then begin
    if (hemisphere eq 1) then begin
        if (channel le 5) then begin
            xdim = 304
            ydim = 448
        endif else begin
            xdim = 608
            ydim = 896
        endelse
    endif else begin
        if (channel le 5) then begin
            xdim = 316
            ydim = 332
        endif else begin
            xdim = 632
            ydim = 664
        endelse
    endelse
endif else begin
    xdim = -1
    ydim = -1
endelse

end


;--------------------------------------------------------------------------------
; extract - extracts SSM/I Polar Grids brightness temperatures.
;
; Input:
;     none.
;
; Output:
;     array containing a time series of SSM/I brightness temperatures.
;--------------------------------------------------------------------------------
pro extract, tb


;
; Get user selections for date range, satellite channel, hemisphere, etc.
;
dates = get_dates()
sat_no = get_satellite()
channel = get_channel(sat_no)
hemisphere = get_hemisphere()

dir = get_dir()
files = get_Tb_file_list(dates.start_date, dates.end_date, $
                         channel, hemisphere, dir, sat_no)

if (n_elements(files) eq 1 and files(0) eq '-1') then begin
    print, 'No files for the period ', dates.start_date, ' to ', dates.end_date
endif else begin
    get_image_size, channel, hemisphere, xdim, ydim
    tb = INTARR(xdim, ydim, n_elements(files))
    for i=0,n_elements(files)-1 do begin
        tmp = read_data_file(files(i), xdim, ydim, status)
        if (status eq 1 and max(tmp) gt 0) then begin
            tb(*,*,i) = tmp
        endif else begin
            ;
            ; There was no file for that day, so fill in with missing.
            ;
            tb(*,*,i) = 157
        endelse
    endfor
endelse

end
