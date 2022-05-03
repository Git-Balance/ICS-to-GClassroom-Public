from __future__ import print_function

import os.path
from datetime import date
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
        'https://www.googleapis.com/auth/classroom.coursework.me',
        'https://www.googleapis.com/auth/classroom.coursework.students',
        'https://www.googleapis.com/auth/classroom.topics.readonly']
fileLocation = '~/Documents/Scripts/ICS-to-GClassroom/API'


def getTopics(course_id, token, service):
    topics = []
    page_token = None
    while True:
        response = service.courses().topics().list(
            pageToken=page_token,
            pageSize=30,
            courseId='461974219150').execute()
        topics.extend(response.get('topic', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    if not topics:
        print('No topics found.')
    else:
        print('Topics:')
        for topic in topics:
            print('{0} ({1})'.format(topic['name'], topic['topicId']))

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'API/credentials.json', SCOPES)
            print(flow)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API
        results = service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])

        if not courses:
            print('No courses found.')
            return
        # Prints the names of the first 10 courses.
        print('Courses:')
        for course in courses:
            print(course['name'])

    except HttpError as error:
        print('An error occurred: %s' % error)

    today = str(datetime.now())
    getTopics('461974219150', 'token.json', service)


if __name__ == '__main__':
    main()
