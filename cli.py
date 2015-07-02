#!/usr/bin/python
import argparse
import daytrace

#This variable is temporary, a config file will replace these at a later date.
output_file = "/home/eandrews/Notes/general/mytime.json"
daytracer = daytrace.daytrace()

def tcreate(args):
    enter_time = daytracer.create_entry(args.category, args.message, args.duration, args.ticket)
    punch_timecard = daytracer.log_entry(enter_time, output_file)
    print(punch_timecard)
    
def ttotal(args):
    print(daytracer.time_total(args.timecard_file))

def tsearch(args):
    sresults = daytracer.search(args.timecard_file, args.category, args.ticket, args.day)
    formatted = daytracer.formatted(sresults)
    for entry in formatted:
        print(entry)
    print(daytracer.tally(sresults))

parser = argparse.ArgumentParser(description='enters and queries time entries.')
subparsers = parser.add_subparsers()

parser_create = subparsers.add_parser("create")
parser_create.add_argument("category", help="The category to assign the time entry to. String expected.", type=str)
parser_create.add_argument("message", help="A brief description of the work done. String expected.", type=str)
parser_create.add_argument("duration", help="The amount of time worked in hours", type=float)
parser_create.add_argument("ticket", nargs='?', help="The ticket name/number the work is associated with.", type=str, default=None)
parser_create.set_defaults(func=tcreate)

parser_total = subparsers.add_parser("total")
parser_total.add_argument("timecard_file", nargs='?', help="Path to the timecard json file.", default=output_file)
parser_total.set_defaults(func=ttotal)

parser_search = subparsers.add_parser("search")
parser_search.add_argument("timecard_file", nargs='?', help="Path to the timecard json file.", default=output_file)
parser_search.add_argument("-c", "--category", nargs='?', help="Show entries with the following category", default=None)
parser_search.add_argument("-t", "--ticket", nargs='?', help="Show entries related to a ticket.", default=None)
parser_search.add_argument("-d", "--day", nargs='?', help="Show entries for a given day.", default=None)
parser_search.set_defaults(func=tsearch)

args = parser.parse_args()
args.func(args)
