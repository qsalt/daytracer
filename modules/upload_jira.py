from jira import JIRA
import datetime
#server = 'https://curiositycake.atlassian.net'
#user = ''
#password = ''


#print(jira.search_issues('assignee = currentUser()'))

class TimeUpload:
    def __init__(self):
        self.auth_type = 'basic'

    def auth(self, server, user, password):
        ### NOTE: Add a try catch here when uploading. This would be to catch
        #if the auth fails
        server = "https://%s" % (server)
        print("Authenticating to %s" % (server))
        self.jira = JIRA(server, basic_auth=(user,password))
        return self

    def upload(self, message, duration, ticket, datetime_obj):
        ### NOTE: Add a try catch here when uploading. This would be to catch
        #if the ticket does not exist
        duration = "%sh" % (duration)
        self.jira.add_worklog(issue=ticket, timeSpent=duration,
                comment=message,
                started=datetime_obj)
#                started=datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.000%z"))
        print("Adding worklog to ticket  %s" % (ticket))
        return True

