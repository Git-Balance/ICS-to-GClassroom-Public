#!/usr/bin/python3

import os
import re
from datetime import date
import datetime

from utils import Debug, Classroom

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

debug = Debug()

# NTS: Delete useless comments like "print('|||||||')"

def main():
    # Get path to the directory containing all the ICS files

    folder = input("Enter folder name:\n")

    cwd = os.getcwd()
    path = os.path.join(cwd, folder)

    print(cwd)
    print(path)

    # For each file in folder, create a item in eventDict and for each line in
    # file, see if one of the filters is in the line. Add each line that passes
    # through the filter to a list that is the value for the item.
    eventDict = {}

    for file in os.listdir(path):
        f = os.path.join(path, file)
        filename = file.replace('.ics', '')
        if os.path.exists(f):
            fileNumber = 0

            with open(f) as icsFile:

                eventDict[filename] = []

                lines = icsFile.readlines()
                print("start")
                for line in lines:
                    # print("|||||||||||||||||||||||||")
                    fileNumber += 1

                    filters = [
                        'SUMMARY',
                        'CREATED',
                        'DTSTAMP',
                        'DTSTART',
                        'DTEND'
                    ]

                    for filter in filters:
                        # print("\\\\\\\\\\\\\\\\\\\\\\")
                        if filter in line:
                            # print(line.replace("\n",""))
                            eventDict[filename].append(line.replace("\n",""))

                if len(eventDict[filename]) != 5:
                    print("List is not correct length, proceed with caution: " + str(len(eventDict[filename])))
    # https://www.geeksforgeeks.org/python-accessing-items-in-lists-within-dictionary/
    # NTS: Make it so this only triggers during testing

    deleteList = []

    # For each event in eventDict, print the lines inside of the event list and
    # ask if the user wants to keep the event. If yes, keep the event. If no,
    # add the event to a list. If quit, stop asking the user to keep the events.

    for key, event in eventDict.items():
        #print(key, event)
        print(key)

        for attribute in event:
            print(" " + attribute)

        loop = True
        exitLoop = False
        while loop == True:
            askEvent = input("Do you want to keep the values? (y/n): \n")
            print("")

            if askEvent == "y":
                print("Kept")
                loop = False
            elif askEvent == "n":
                deleteList.append(key)
                print(deleteList)
                print("Going to be deleted")
                loop = False
            elif askEvent == "q":
                loop = False
                exitLoop = True
            else:
                print("Unknown input, please enter (y/n/q)")
        print("")

        if exitLoop == True:
            break

    # Use the list that has all the events that the user wants to delete from
    # earlier to remove events from eventDict that the user doesn't want.

    # NTS: delete prints used for testing
    debug.printDictKeys(eventDict)
    for deleted in deleteList:
        print("")
        print(deleted)
        del eventDict[deleted]
        print("")
    debug.printDictKeys(eventDict)

    # Start of the Google Classroom side of the code

    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
            'https://www.googleapis.com/auth/classroom.coursework.me',
            'https://www.googleapis.com/auth/classroom.coursework.students',
            'https://www.googleapis.com/auth/classroom.topics.readonly']

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        raise ValueError("No token, run quickstart or something")

    courseID = '461974219150'
    topicID = "483403222156"
    service = build('classroom', 'v1', credentials=creds)
    print(type(service)) # DD

    classroom = Classroom(courseID, service, topicID)

    currentDate = datetime.datetime.now()

    assignmentList = []



    # DD >> classroom.get_topics()
    for key, event in eventDict.items():
        print(key)
        title = key
        dueDay = 0
        dueMonth = 0
        dueYear = 0



        for attribute in event:
            if 'DTEND;VALUE=DATE:' in attribute:
                # https://pynative.com/python-regex-capturing-groups/
                print(attribute)
                date = re.search(r'([0-9]{4})([0-9]{2})([0-9]{2})', attribute)

                dueDay = int(date.group(3))
                dueMonth = int(date.group(2))
                dueYear = int(date.group(1))

        print("assignment day {}, current day {}".format(dueDay, currentDate.day))
        if dueMonth < currentDate.month:
            print("Month for {} is in the future")
            print("Event month: {}\nCurrent month: {}".format(dueMonth, currentDate.month))
            dueMonth = -1
        elif dueDay <= currentDate.day:
            print("Day for {} is in the future")
            print("Event day: {}\nCurrent day: {}".format(dueDay, currentDate.day))
            dueDay = -1
        classroom.create_coursework(
                                title,
                                dueDay,
                                dueMonth,
                                dueYear,
                                topicID)


if __name__ == '__main__':
    main()
