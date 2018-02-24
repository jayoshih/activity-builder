import io
import json
import os
import tempfile

from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from lesweets.html_writer import HTMLWriter
from urllib.parse import parse_qsl

def mathlibs(request):
    with open(os.path.join(settings.DATA_URL, "mathlibs.json"), "rb") as mathlib_data:
        return render(request, "mathlibs.html", {
            "activities": ACTIVITIES,
            "page": "Math Libs",
            "stories": json.load(mathlib_data)
        })

def create_mathlib(request, category_id, story_id):
    with open(os.path.join(settings.DATA_URL, "mathlibs.json"), "rb") as mathlib_data:
        data = json.load(mathlib_data)
        category_data = next(c for c in data["categories"] if c["id"] == category_id)
        story_data = next(s for s in category_data["stories"] if s["id"] == story_id)

        # Get list of numbers to use in formula
        numbers = [n for n in story_data["items"] if n.get("operator")]

        return create_zip(
            "{}-{}.zip".format(category_id, story_id),
            'activities/mathlibs_template.html',
            {"story": story_data, "formula": numbers}
        )

def jeopardy(request):
    NUM_ROWS = int(request.GET.get('rows', None) or 5)
    NUM_COLUMNS = int(request.GET.get('cols', None) or 6)
    POINT_INCREMENT = 100

    grid = []
    points = 0
    for row in range(0, NUM_ROWS):
        points += POINT_INCREMENT
        grid.append({
            "num": row,
            "points": points,
            "columns": range(0, NUM_COLUMNS),
        })

    return render(request, 'jeopardy.html', {
        "activities": ACTIVITIES,
        "page": "Jeopardy",
        "grid": grid,
        "categories": range(1, NUM_COLUMNS + 1), # Start at category 1 rather than 0
        "numrows": NUM_ROWS,
        "numcols": NUM_COLUMNS,
    })

def create_jeopardy(request):
    params = parse_qsl(request.body)

    # Parse query params
    rows = {}
    categories = {}

    for k, v in params:
        keys = k.decode('utf-8').split("-")
        value = v.decode('utf-8')

        # Parse categories
        if keys[0] == "c":
            colnum = int(keys[1]) - 1
            categories.update({ str(colnum) :  value })
        elif keys[0] == "p" or keys[0] == "q" or keys[0] == "a":
            rownum = keys[1]
            row = rows.get(rownum) or {}

            # Process points
            if keys[0].startswith("p"):
                row.update({ "points": int(value) })

            # Process questions and answers
            else:
                colnum = keys[2]
                columns = row.get("columns") or {}
                column = columns.get(colnum) or {}
                column.update({ keys[0]: value, "num": colnum })
                columns.update({ colnum : column })
                row.update({ "columns" : columns })
            rows.update({ rownum: row })

    game = {
        "categories": [categories[k] for k in sorted(categories)],
        "rows": [{
            "num": k,
            "points": rows[k]["points"],
            "columns": [rows[k]["columns"][col] for col in sorted(rows[k]["columns"])]
        } for k in sorted(rows)]
    }

    return create_zip("jeopardy.zip", 'activities/jeopardy_template.html', game)

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



def get_file_path(path):
    return os.path.sep.join([settings.BASE_DIR, "lesweets"] + path.lstrip("/").split("/"))

# Write the value of our buffer to the response
def create_zip(zip_name, html, context):
    # Create a buffer to write the zipfile into
    zip_buffer = io.BytesIO()

    with HTMLWriter(zip_buffer) as writer:
        html  = render_to_string(html, context)

        soup = BeautifulSoup(html, "html.parser")
        # Add links to zip
        for link in soup.find_all('link'):
            download_path = get_file_path(link["href"])
            link["href"] = writer.write_file(download_path)

        # Add scripts to zip
        for script in soup.find_all('script'):
            download_path = get_file_path(script["src"])
            script["src"] = writer.write_file(download_path)

        writer.write_index_contents(soup.renderContents())

        writer.zf.printdir()

    # Create the HttpResponse object with the appropriate HTML header.
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(zip_name)

    return response
