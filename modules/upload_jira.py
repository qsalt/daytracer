from jira import JIRA
#server = 'https://curiositycake.atlassian.net'
#user = ''
#password = ''


#print(jira.search_issues('assignee = currentUser()'))

class TimeUpload:
    def __init__(self):
        self.auth_type = 'basic'

#    def auth_type(self):
#        return 'basic'

    def auth(self, server, user, password):
        print('authenticating ===NOW===')
        return self
        #self.jira = JIRA(server, basic_auth=(user,password))

    def upload(self, message, duration, ticket):
        #self.jira.add_worklog(issue=ticket, timeSpent=duration, comment=message)
        print('Trying to upload some ====stuff====')

