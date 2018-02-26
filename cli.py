#!python
import argparse
import ConfigParser
import daytrace
import os
import sys
import json

daytracer = daytrace.daytrace()
###############################################################################
# ___ Functions Below ___ #
###############################################################################

# Creates a time card entry 
def tcreate(args):
    if not os.path.isfile(output_file):
        with open(output_file, 'wb') as json_create:
            json_create.write('{}')

    #The next few lines pull out all the keys in the config file and assemble
    #them into an array to pass to the fuzzy matching method.
    categories = []
    for (item_key, item_value) in config.items('Categories'):
        categories.append(item_key)
    match_category = daytracer.fuzzy_match(args.category, categories)
    enter_time = daytracer.create_entry(match_category, args.message,
            args.duration, args.ticket)
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

def tupload(args):
    platform = config.get('Remote', 'platform')
    server = config.get('Remote', 'server')
    user = config.get('Remote', 'user')
    password = config.get('Remote', 'pass')
    token = config.get('Remote', 'token')
    with open(args.timecard_file, 'r') as jfile:
        time_card = json.load(jfile)

    auth = daytracer.auth_upload(platform, server, user, password, token)

    # First checks if the value has been uploaded already, if so, pass it.
    # Otherwise it checks to see if a ticket is set, if it is, upload the entry
    # to the ticket. Otherwise, upload the entry to the ticket associated with
    # the category.
    for key, value in time_card.iteritems():
        # Using .get method to return None if key is not present, rather than
        # erroring
        if value.get('uploaded') == True:
            print('blocked upload, already done')
            continue

        elif value['ticket'] == None:
            category = value['category']
            # Fetches the ticket assigned to the category in the config.cfg file
            ticket = config.get('Categories', category)
            upload_results = daytracer.upload(platform, server,
                value['message'], value['duration'], ticket, user,
                password, token)
        else:
            upload_results = daytracer.upload(platform, server,
                value['message'], value['duration'], value['ticket'], user,
                password, token)

        # Writes back to time entry to indicated it has been uploaded
        if upload_results == True:
            print('upload results triggered and uploaded written to databag')
            value['uploaded'] = True
            time_entry = { key: value }
            daytracer.log_entry(time_entry, output_file)




    return True

# This function parses the config. If it doesn't exist, it creates a Scaffold
# config with defaults
def config_fetch(config_path):
    config = ConfigParser.RawConfigParser()
    if not os.path.isfile(config_path):
        config.add_section('DayTracer')
        config.set('DayTracer', 'timecard_location', "%s/mytime.json" % (os.path.dirname(os.path.realpath(__file__))))
        config.add_section('Categories')
        config.set('Categories', 'admin', 'url/action')
        config.set('Categories', 'development', 'url/action')
        config.set('Categories', 'operations', 'url/action')
        #Configure a bare config file to use. Add/change categories to use when logging time.
        with open(config_path, 'wb') as configfile:
            config.write(configfile)
        print("Created config file %s, please update and re-run the desired command" % (config_path))
        sys.exit(1)

    return config


###############################################################################
# ^^^ Functions Above ^^^ #
###############################################################################

#Reads the config and assigns it to the output_file variable to determine where
#the timecard is to be placed.
config_file = "%s/config.cfg" % (os.path.dirname(os.path.realpath(__file__)))
config = config_fetch(config_file)
config.read(config_file)
output_file = config.get('DayTracer', 'timecard_location')
# This checks if the platform is defined as jira, if it is, import needed
# library
#if config.get('Remote', 'platform') == 'jira':
#    from jira import JIRA


parser = argparse.ArgumentParser(description='Enters and queries time logs. Time entries must match categories defined in config.cfg.')
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

parser_search = subparsers.add_parser("upload")
parser_search.add_argument("timecard_file", nargs='?', help="Path to the timecard json file.", default=output_file)
parser_search.set_defaults(func=tupload)

args = parser.parse_args()
# below calls the function defined by the set_defaults method of the argparser
# class parser_search.set_defaults(func="") line
args.func(args)
