import datetime
import json
#from datetime import datetime

class daytrace:

    def __init__(self):
        #Assigns an instance variable for the time
        self.date_time = datetime.datetime.today()
################################################################################
################################################################################
    def create_entry(self, category, message, duration, output=None, year=None, month=None, day=None, hour=None, minute=None):
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

        # Creating the entry_key variable just to make naming the dictionary keys easier. Also appended dentries to the dictionary opposed to declaring them all at once for readability purposes.
        self.entry_key = self.date_time.strftime('%Y%m%d%M%S')
        time_entry = { self.entry_key: {}}
        time_entry[self.entry_key]['category'] = category
        time_entry[self.entry_key]['message'] = message
        time_entry[self.entry_key]['duration'] = duration
        time_entry[self.entry_key]['year'] = year
        time_entry[self.entry_key]['month'] = month
        time_entry[self.entry_key]['day'] = day
        time_entry[self.entry_key]['hour'] = hour
        time_entry[self.entry_key]['minute'] = minute
        entry_json = json.dumps(time_entry, sort_keys=True, indent=4)

        return time_entry
################################################################################
################################################################################
    def log_entry(self, entry_json, json_path=None):
        if json_path is None:
            json_path="./my_time.json"

        #Opens the json file of time entries as a python file obj. Converts the json file obj to a python dictionary.
        with open(json_path, 'r') as jfile:
            time_card = json.load(jfile)

        #Updates the python dictionary and appends the entry to the dictionary. Converts the dictionary back to json and overwrites the existing file.
        time_card.update(entry_json)
        with open(json_path, 'w') as jfile:
            json.dump(time_card, jfile, sort_keys=True, indent=4)
        return True
################################################################################
################################################################################
    def time_total(self, begin, end, json_path=None):
        if json_path is None:
            json_path = './my_time.json'

        #Opens the json file of time entries as a python file obj. Converts the json file obj to a python dictionary.
        with open(json_path, 'r') as jfile:
            time_card = json.load(jfile)
        time_total=0
#        print(time_card)
#        print(time_card['201506281138']['duration'])
        for key, value in time_card.iteritems():
            time_total = time_total + value['duration']

        return time_total
################################################################################


###############
### Methods ###
###############
#Time_entry(year, month, day, time, duration, message, category) 
###Writes output as json file as described in readme
###Increments entries
###Assumes date if blank
#Edit_entry
###Allows adding or modifying information on an existing time entry
#Sort_time
###Sorts and returns time entry based on search.
###Return time entries for the year
#####For month
#####For week
#####For day
#####For category
###Return total time worked for day
#####For week
#####For month
