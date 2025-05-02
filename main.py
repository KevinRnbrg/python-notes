import time
from progress.bar import Bar

notes = []
title = "~ Notes ~"
compact = False

invalidInput = "Input cannot be read."

def initialize():
    with Bar('Loading...') as bar:
        for i in range(100):
            time.sleep(0.01)
            bar.next()
        bar.finish()
    printPerCharacter("Write 'help' for list of commands.")

def printPerCharacter(string):
    newString = ""
    for i in range (0, len(string)):
        newString += string[i]
        print(newString, end="\r")
        max_sleep = 0.02
        min_sleep = 0.002
        scaling_factor = 50
        calculated_sleep = min_sleep + ((max_sleep - min_sleep) / (1 + len(string) / scaling_factor))
        time.sleep(calculated_sleep)
    print("")

def displayNotes():
    def calculateDimensions():
        max_note_length = max((len(note) for note in notes), default=0)
        max_index_width = len(str(len(notes)))
        max_content_width = max(len(title), max_note_length + max_index_width + 3)
        columns = max_content_width + 2
        return max_index_width, max_content_width, columns

    def printHeader(columns):
        printPerCharacter("+" + "-" * columns + "+")
        printPerCharacter("| {:^{}} |".format(title, columns - 2))

    def printNoteRow(index, note, max_index_width, max_content_width):
        printPerCharacter("| {:>{}} | {:<{}} |".format(
            index, max_index_width, note, max_content_width - max_index_width - 3
        ))

    max_index_width, max_content_width, columns = calculateDimensions()

    if notes:
        printHeader(columns)
        printPerCharacter("+" + "-" * columns + "+")
        for index, note in enumerate(notes, start=1):
            printNoteRow(index, note, max_index_width, max_content_width)
            if compact:
                continue
            else:
                printPerCharacter("+" + "-" * columns + "+")
        if compact:
            printPerCharacter("+" + "-" * columns + "+")
    else:
        printHeader(columns)
        printPerCharacter("+" + "-" * columns + "+")

def commandHelp():
    commands = [
        "'list' - list notes",
        "'add <>' - add new note",
        "'delete <ID>' - delete note by ID",
        "'exit' - exit application",
        "'help' - list of usable commands",
        "'compact' - toggle compact list"
    ]
    for command in commands:
        printPerCharacter(command)

def commandAdd(note):
    if note.strip():
        notes.append(note)
        printPerCharacter(f"Added new note: {note}")
    else:
        printPerCharacter("Note cannot be empty")

def commandDelete(note_id):
    try:
        note_id = int(note_id) - 1
        if 0 <= note_id < len(notes):
            printPerCharacter(f"Deleted note: {notes.pop(note_id)}")
        else:
            printPerCharacter("Invalid note ID.")
    except (ValueError, IndexError):
        printPerCharacter("Invalid note ID.")

def showMenu():
    global compact
    while True:
        user_input = input()
        split_input = user_input.split(" ")
        match split_input[0]:
            case "list":
                displayNotes()
            case "add":
                commandAdd(' '.join(split_input[1:])) if len(split_input) > 1 else printPerCharacter(invalidInput)
            case "delete":
                commandDelete(split_input[1])
            case "exit":
                quit() if len(split_input) <= 1 else printPerCharacter(invalidInput)
            case "help":
                commandHelp() if len(split_input) <= 1 else printPerCharacter(invalidInput)
            case "compact":
                if len(split_input) > 1:
                    printPerCharacter(invalidInput)
                else:
                    compact = not compact
                    printPerCharacter(f"List compact: {compact}")
            case _:
                printPerCharacter("Command could not be recognized.")

def startup():
    printPerCharacter("Welcome to notes")
    showMenu()

initialize()
startup()