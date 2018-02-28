## Purpose

Library to take time entry data and output it as json to a file. It should handle accepting the, duration, note/message/descriptoion, category, and ticket.

## ToDo:
* Provide a means to edit logged issues beyond vim.
* Provide alternate output for searches.
* Link into jira's API for work log entries.

### Usage Example
```
daytrace create "awesome category" "I made great progress on that awesome project." 2.5 "issue-awesome123"
```

### Arguments & Sub Args:
* create: Used to create time entries.
    * category: The category the time falls under. ie. support, admin time, maintenance, etc. String expected
    * description: A brief description of the work done. String expected.
    * duration: The time worked in hours. Float expected
    * ticket (optional): The ticket or issue associated with the work log. String expected.
* total: Used to output the total time worked.
* search: Used to find logs for a specific category, day, or ticket.
    * -c, --category: Find all entries in the given category. Fuzzy matching used. String expecte.
    * -d, --day: Find all entries on a given day. Int expected.
    * -t, --ticket: Find all entries associated with a specific ticket. Fuzzy matching used. String expected.
* edit: Used to edit previous entries. If no search criteria provided edits last entry. (Not available/Work in progress)
    * Single & Bulk edit: find one or multiple issues and edit a given key value pair.
    * Edit last: If no filter is provided edit key value pairs of latlest entry.

### Remote module extension
This tool stores ticket system modules in ./lib/platform to handle the
uploading of time entries to different tracking systems. The requirements for
modules are they have a upload method, and when initialized, the class contains
a self.auth variable, which stores the kind of authentication system required
(basic auth, token, oauth).

### Config file
This script looks for a config.cfg file in the directory of the git repo. If it does not exist, a default config file is generated. This config is used to set where your mytime.json file will be saved, and what categories you want to track your time in.

Sample config:

```
[DayTracer]
timecard_location = mytime.json

[Categories]
admin = url/action
development = url/action
operations = url/action

[Remote]
platform = jira
server = curiositycake.atlassian.net
user = USERNAME
pass = PASSWORD
token = TOKEN
```

### Sample Output:

```
{
    "20150630081700": {
        "year": 2015,
        "month": "06",
        "day": 17,
        "hour": 16,
        "minute":15,
        "duration": 2,
        "message": "Worked on the foo project.",
        "category": "Foobar 1234",
        "ticket": "issue-2348"
    },
    "20150701075825": {
        "year": 2015,
        "month": "06",
        "day": 17,
        "hour": 16,
        "minute":15,
        "duration": 0.5,
        "message": "Worked on the foo project.",
        "category": "Foobar 1234",
        "ticket": null
    }

}
```

### Bugs
* Bug found in jira library. PR for fix created here: https://github.com/pycontribs/jira/pull/514
