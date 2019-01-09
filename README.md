# iski-tracker-export-tcx
Export-Script for iSki Tracker as.tcx

Thanks to vicziani for the script ----- https://gist.github.com/vicziani/2b099734e8847a26ef0e8ab8d76c33e0

Convert html saved from iSki tracker website to gpx format to import any application or service such QLandkarteGT, Endomondo, etc. 
Need to install the following packages: 

$ pip install pytz 
$ pip install tzlocal 

Usage: $ iski-convert.py 

Background: There is no export function on iSki tracker website, but the html source contains the date, coordinates, profile 
in different format. This script converts it to gpx that is a common GPS data format for software applications. 
The script use the locale timezone and convert the dates to UTC, because the GPS format defines date in Coordinated Universal Time (UTC) 
using ISO 8601 format. The Z at the end of the dates is the zone designator for the zero UTC offset.

I added the save to a file. The track is saved to a file 'out.gpx'
