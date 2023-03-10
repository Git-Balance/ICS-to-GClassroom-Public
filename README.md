# ICS-to-GClassroom
Take ICS files and make Google Classroom assignments based off of them

Input the name of the folder containing the ICS files. For each file inside the folder, ask the user if they want to keep the assignment or not. After the user entered an input for every file, make an event with only the data of the files the user wanted to keep. Then, create assignments for every event. If the event is in the past, make the assignment without a due date. 

This project was created during independent study. It was made as a way of transfering items from an app a teacher forced me to use to Google Classroom, which was my primary todolist at the time. At the time, I would transfer then ICS file to my PC, run the script to a google account that wasn't my school one, so my todolists weren't the same, and had to constantly swap between acounts. Nowadays, I use Emacs' todomode on my phone using termux for my todolist.

If I were to redo this assignment, which I probably wouldn't since I use an actual todolist nowadays, I would have made a cleaner menu for selecting which items to add to Google Classroom, and would have learned how to write documentation according to a coding standard. The menu specifically could have been done with a library like simple-term-menu or console-menu. I would also have kept better track of time, so I wouldn't have to make a commit one minute before the bell rings.
