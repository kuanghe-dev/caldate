# Calculate Dates

## This tool can
- calculate the difference in days between two dates;
- apply an offset to a certain date.

## Usage
    # Calculate the difference in days between 'date1' and 'date2'
    caldate [-q] date1 date2

    # Calculate the date of 'date1' +/- number of days
    caldate [-q] date1 [+|-]num

    NOTE: Dates should be 'today' or in the form of m/d, mm/dd (both assuming
          current year), m/d/yy, mm/dd/yy, m/d/yyyy or mm/dd/yyyy.

## Option
    -q      quiet mode (output as little as possible)

## Examples
    $ caldate 08/20/2005 06/22/10
    08/20/2005 to 06/22/2010: 1767 day(s)

    $ caldate 2/1 28            # Assuming current year is 2013
    02/01/2013 + 28 day(s): 03/01/2013

    $ caldate today 12/25       # Assuming today is Feb 4, 2013
    02/04/2013 to 12/25/2013: 324 day(s)
    
## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
