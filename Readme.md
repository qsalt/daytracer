#Purpose

Library to take time entry data and write output it as json. It should handle accepting the day, time, duration, note/message, and category.

daytrace -m may -D 25 -t 1230-1300 -d 30m -m "worked on the foo project." -c "foo_issue 25"

Options:
    * -y: Year. If omitted this should be calculated based on system time.
    * -m: Month. If omitted this should be calculated based on system time.
    * -D: Day. If omitted this should be calculated based on system time.
    * -t: Time of day. If omitted this should be calculated based on system time.
    * -d: Duration of time worked.
    * -m: Message/note about the work done.
    * -c: Category/issue related to the work done.

Sample json output:

```
{
    "entry1": {
        "year": 2015,
        "month": "june",
        "weekday": "monday",
        "day": 17,
        "time": 1415,
        "duration": "2h",
        "message": "Worked on the foo project."
        "category": "Foobar 1234"
    },
    "entry2": {
        "year": 2015,
        "month": "june",
        "weekday": "monday",
        "day": 17,
        "time": 1615,
        "duration": "0.5h",
        "message": "Worked on the foo project."
        "category": "Foobar 1234"
    }

}
```
