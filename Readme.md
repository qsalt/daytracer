## Purpose

Library to take time entry data and output it as json to a file. It should handle accepting the, duration, note/message/descriptoion, category, and ticket.

daytrace create "awesome category" "I made great progress on that awesome project." 2.5 "issue-awesome123"

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

Sample json output:

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