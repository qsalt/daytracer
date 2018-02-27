import datetime
import json
import difflib
import sys
import importlib
#from datetime import datetime

class daytrace:

    def __init__(self):
        #Assigns an instance variable for the time
        self.date_time = datetime.datetime.today()
################################################################################
################################################################################
    def create_entry(self, category, message, duration, ticket=None, year=None, month=None, day=None, hour=None, minute=None):
        # Checks if specific time was passed, if not, creates entry at the time
        # of creating the entry
        if year is None:
            year = int(self.date_time.strftime('%Y'))
        if month is None:
            month = int(self.date_time.strftime('%m'))
        if day is None:
            day = int(self.date_time.strftime('%d'))
        if hour is None:
            hour = int(self.date_time.strftime('%H'))
        if minute is None:
            minute = int(self.date_time.strftime('%M'))
        duration = float(duration)

        # Creating the entry_key variable just to make naming the dictionary
        # keys easier. Also appended dentries to the dictionary opposed to
        # declaring them all at once for readability purposes.
        self.entry_key = self.date_time.strftime('%Y%m%d%H%M%S')
        time_entry = { self.entry_key: {}}
        time_entry[self.entry_key]['category'] = category
        time_entry[self.entry_key]['message'] = message
        time_entry[self.entry_key]['duration'] = duration
        time_entry[self.entry_key]['ticket'] = ticket
        time_entry[self.entry_key]['year'] = year
        time_entry[self.entry_key]['month'] = month
        time_entry[self.entry_key]['day'] = day
        time_entry[self.entry_key]['hour'] = hour
        time_entry[self.entry_key]['minute'] = minute
        #entry_json = json.dumps(time_entry, sort_keys=True, indent=4)

        return time_entry
################################################################################
################################################################################
    def log_entry(self, entry_dict, json_path=None):
        if json_path is None:
            json_path="./my_time.json"

        #Opens the json file of time entries as a python file obj. Converts the
        #json file obj to a python dictionary.
        with open(json_path, 'r') as jfile:
            time_card = json.load(jfile)

        #Updates the python dictionary and appends the entry to the dictionary.
        #Converts the dictionary back to json and overwrites the existing file.
        time_card.update(entry_dict)
        with open(json_path, 'w') as jfile:
            json.dump(time_card, jfile, sort_keys=True, indent=4)
        return True
################################################################################
################################################################################
    def time_total(self, json_path=None):
        if json_path is None:
            json_path = './my_time.json'

        #Opens the json file of time entries as a python file obj. Converts the
        #json file obj to a python dictionary.
        with open(json_path, 'r') as jfile:
            time_card = json.load(jfile)
        time_total=0
#        print(time_card)
#        print(time_card['201506281138']['duration'])
        for key, value in time_card.iteritems():
            time_total = time_total + value['duration']

        return time_total
################################################################################
################################################################################
    def search(self, json_path=None, category=None, ticket=None, day=None):
        if json_path is None:
            json_path = './mytime.json'

        # Open the passed timecard json file
        with open(json_path, 'r') as jfile:
            time_card = json.load(jfile)

        def filter(item, item_category):
            filter_items = {}
            if item is not None:
                for key, value in time_card.iteritems():
                    if value[item_category] is None:
                        continue
                    elif type(value[item_category]) is int:
                        if int(item) is int(value[item_category]):
                            filter_items[key] = value
                    elif item.lower() in value[item_category].lower():
                        filter_items[key] = value
                        #print(filter_items)
                return filter_items
#            return None

        if category is not None:
            results = filter(category, 'category')
        if ticket is not None:
            results = filter(ticket, 'ticket')
        if day is not None:
            results = filter(day, 'day')
        if category is None and ticket is None and day is None:
            results = time_card

        return results
#        self.tally(results)
################################################################################
################################################################################
    def tally(self, time_dictionary):
        time_total = 0
        for key, value in time_dictionary.iteritems():
            time_total = time_total + value['duration']

        return time_total
################################################################################
################################################################################
    def formatted(self, time_dictionary):
        formatted_list = []
        for key, value in time_dictionary.iteritems():
            formatted_entry = '%s-%s, %s hour(s), CATEGORY: "%s" MESSAGE: "%s" TICKET: "%s"' % (value['month'], value['day'], value['duration'], value['category'], value['message'], value['ticket'])
            formatted_list.append(formatted_entry)
        return sorted(formatted_list)
################################################################################
################################################################################
    def fuzzy_match(self, item_str, category_list):
        #Category list is an array of values
        fuzzy_match = difflib.get_close_matches(item_str, category_list, 1, 0.7) 
        #This sees if the array is empty from the fuzzy match. If it is then no
        #matches were found and the program exits
        if not fuzzy_match:
            print('No category match, try again')
            sys.exit(1)
        #print(fuzzy_match)
        #return the matching category
        return fuzzy_match[0]
        #Compares the item_str to items in the category_list to see which is
        #the closest match. It returns the closest match.
################################################################################
################################################################################
    def auth_upload(self, ticket_platform, server, user=None, password=None,
            token=None):
        # Imports a module from ./lib/platform/ based on what ticket_platform is
        # passed as an argument. After instantiating the platform
        # module, code checks what kind of authentication that module uses, and
        # evokes the auth method needed for the given module. This
        # authentication child object is stored in the parent object to use
        # when uploading time entries to the service
        module = importlib.import_module("modules.%s" % (ticket_platform))
        self.uploader = module.TimeUpload()
        if self.uploader.auth_type == 'basic':
            self.uploader.auth(server, user, password)
        if self.uploader.auth_type == 'token':
            self.uploader.auth(server, user, token)
        return self

    def upload(self, ticket_platform, server, message, duration, ticket,
        user=None, password=None, token=None):

        # Upload results with the imported class from the auth method
        # NOTE: Should add a try catch here to not error if auth_upload is not
        # evoked first
        upload_results = self.uploader.upload(message, duration, ticket)
        return True

















