#!/usr/bin/python
import argparse
import daytrace

#This variable is temporary, a config file will replace these at a later date.
output_file = "/home/eandrews/Notes/general/mytime.json"

parser = argparse.ArgumentParser(description='enters and queries time entries.')
parser.add_argument("category", nargs='?', help="The category to assign the time entry to. String expected.", type=str, default=None)
parser.add_argument("message", nargs='?', help="A brief description of the work done. String expected.", type=str, default=None)
parser.add_argument("duration", nargs='?', help="The amount of time worked in hours", type=float)
parser.add_argument("ticket", nargs='?', help="The ticket name/number the work is associated with.", type=str, default=None)
parser.add_argument("-q", "--query", help="queries the time card and adds up the total", action="store_true")

args = parser.parse_args()

daytracer = daytrace.daytrace()

if args.query is True:
    print(daytracer.time_total(output_file))
    
else:
    enter_time = daytracer.create_entry(args.category, args.message, args.duration, args.ticket)
    punch_timecard = daytracer.log_entry(enter_time, output_file)
    print(punch_timecard)
