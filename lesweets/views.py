import json

from django.http import HttpResponse
from django.shortcuts import render

def mathlibs(request):
    return render(request, 'mathlibs.html', { 'activities': ACTIVITIES, "page": "Math Libs" })

def jeopardy(request):
    return render(request, 'mathlibs.html', { 'activities': ACTIVITIES })

def tictactoe(request):
    return render(request, 'mathlibs.html', { 'activities': ACTIVITIES })

def aroundtheworld(request):
    return render(request, 'mathlibs.html', { 'activities': ACTIVITIES })

def bingo(request):
    return render(request, 'mathlibs.html', { 'activities': ACTIVITIES })


CARDS_PER_ROW = 3
ACTIVITIES = [
    {
        "name": "Math Libs",
        "slug": "math-libs",
        "view": mathlibs,
        "thumbnail": "",
        "description": "Select word problems for students to create their own stories by filling in the blanks. Students can share their stories and have each other solve their problems.",
        "annotation": {
            "time": "20min",
            "skills": ["Critical Thinking", "Creativity"],
            "level": "K-6",
            "subjects": ["Math"],
        },
    },
    {
        "name": "Jeopardy",
        "slug": "jeopardy",
        "view": jeopardy,
        "thumbnail": "",
        "description": "Fill out a jeopardy board with categories from your lessons to help your students review information. Students will participate in teams or individually to try to get the most points.",
        "annotation": {
            "time": "60min",
            "skills": ["Collaboration", "Review"],
            "level": "K-12",
            "subjects": ["Any Subject"]
        },
    },
    {
        "name": "Tic-Tac-Toe",
        "slug": "tic-tac-toe",
        "view": tictactoe,
        "thumbnail": "",
        "description": "Fill a tic-tac-toe board with problems. Pair your students and have them mark 'X' or 'O' every time they alternate in solving the problems. The first player to get three in a row wins.",
        "annotation": {
            "time": "60min",
            "skills": ["Collaboration"],
            "level": "K-12",
            "subjects": ["Collaboration"],
        },
    },
    {
        "name": "I have… Who has….?",
        "slug": "around-the-world",
        "view": aroundtheworld,
        "thumbnail": "",
        "description": "The teacher randomly passes out cards (in this case, randomly assigns a digital card to each student). Each card has written on it both a question to ask out loud, as well as the answer to another card’s question",
        "annotation": {
            "time": "20min",
            "skills": ["Collaboration"],
            "level": "K-3",
            "subjects": ["Any Subject"],
        },
    },
    {
        "name": "Bingo",
        "slug": "bingo",
        "view": bingo,
        "thumbnail": "",
        "description": "Create squares with questions for students to fill out. These squares will be auto-shuffled for each student. When a student has filled out the card, he or she wins",
        "annotation": {
            "time": "45min",
            "skills": ["Review"],
            "level": "K-3",
            "subjects": ["Any Subject"],
        },
    },
]


# The teacher randomly passes out cards (in this case, randomly assigns a digital card to each student). Each card has written on it both a question to ask out loud, as well as the answer to another card’s question. For example, there may be a set of Math cards with double digit addition problems. One card may say, “I have 36. Who has the sum of 19 + 4?” and someone else’s card will read “I have 23. Who has the sum of 12 + 5?” etc.

# The teacher picks one person to start the activity by reading the question out loud on their card, and then the person who has the corresponding answer reads their card by saying “I have….” and then proceeds by reading the new question on the card.

# This can be done with other subjects as well, but is typically successful with Math problems because the group can work together to solve if someone gets stuck.




def index(request):
    return render(request, 'menu.html', {
        'activities': [ ACTIVITIES[i:i+3] for i in range(0, len(ACTIVITIES), CARDS_PER_ROW) ],
        'colsize': int(round(12 / CARDS_PER_ROW))
    })
