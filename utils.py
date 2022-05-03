#!/usr/bin/python3

dict1 = {"Test1":1, "Test2":2, "Test3":3}

class Debug:
    def printDictKeys(self, dict):
        for key in dict:
            print('({0})'.format(key))

class Classroom:
    def __init__(self, course, service, token):
        self.course = course
        self.service = service # build('classroom', 'v1', credentials=creds)
        self.token = token
        print(self.service) # DD
        print(type(self.service)) # DD
    def create_coursework(self,
                        title,
                        due_day,
                        due_month,
                        due_year,
                        topic_id):
        # Start service with self.service
        # Note: finding the values of due variables is not this script's
        # job. Do that in __main__ or another function
        # Make dictionary called coursework for coursework (duh)
        #
        # For title, make it the title variable
        # For dueDate:
        #    day = due_day
        #    month = due_month
        #    year = due_year
        # For dueTime, make it at 10:30pm
        # For topic, make it topic_id
        #
        # If due_day or due_month is equal to -1, don't make a duedate
        #
        # Use service.courses() to make assignment


        service = self.service

        coursework = {
            'title': title,
            'description': '''Made using the ICS-to-GClassroom script I made''',
            'materials': [
                # Leave blank, unless it breaks the code
            ],
            'workType': 'ASSIGNMENT',
            'state': 'PUBLISHED',
            "dueDate": { # Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following: * A full date, with non-zero year, month, and day values. * A month and day, with a zero year (for example, an anniversary). * A year on its own, with a zero month and a zero day. * A year and month, with a zero day (for example, a credit card expiration date). Related types: * google.type.TimeOfDay * google.type.DateTime * google.protobuf.Timestamp # Optional date, in UTC, that submissions for this course work are due. This must be specified if `due_time` is specified.
                "day": due_day, # Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.
                "month": due_month, # Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day.
                "year": due_year, # Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.
            },
            "dueTime": { # Represents a time of day. The date and time zone are either not significant or are specified elsewhere. An API may choose to allow leap seconds. Related types are google.type.Date and `google.protobuf.Timestamp`. # Optional time of day, in UTC, that submissions for this course work are due. This must be specified if `due_date` is specified.
                "hours": 23, # Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time.
                "minutes": 0, # Minutes of hour of day. Must be from 0 to 59.
                "nanos": 0, # Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.
                "seconds": 0, # Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds.
            },
            'topicId': topic_id,
        }

        # print("{} day {} month".format(due_day, due_month))

        if due_day == -1 or due_month == -1:
            print("Creating assignment ({}) without a due date".format(title))
            del coursework["dueDate"]
            del coursework["dueTime"]

        coursework = service.courses().courseWork().create(
            courseId=self.course, body=coursework).execute()
        print('Assignment created with ID {%s}' % coursework.get('id'))
        print('Assignment name is (' + title + ')')


    def get_topics(self):
        # Just code copied from google's api page for google classroom, but
        # edited to work with Classroom class
        # Link: https://developers.google.com/classroom/guides/manage-topics

        course_id = self.course
        service = self.service

        topics = []
        page_token = None
        while True:
            response = service.courses().topics().list(
                pageToken=page_token,
                pageSize=30,
                courseId=course_id).execute()
            topics.extend(response.get('topic', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                print("No token found")
                break
        if not topics:
            print('No topics found.')
        else:
            print('Topics:')
            for topic in topics:
                print('{0} ({1})'.format(topic['name'], topic['topicId']))




if __name__ == "__main__":
    # This is just for debugging
    debug = Debug()
    debug.printDictKeys(dict1)
