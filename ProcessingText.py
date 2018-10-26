# This is for processing the given text files from cornell movie dialogues corpus to get just
# the line numbers
#
# get_lines() will get the line numbers from each conversation in the movie_conversations text document
#
# make_new_con() will take each new list of conversations and break down each array larger than 2 into statements and
# responses. For example, if a conversation has statements 1, 2, 3 it will be broken down into
# 2 new arrays 1, 2 and 2, 3
#
# get_text() will take the lines from the lineText file and produce an array for each line with the
# first elements being the line number denoted with L at the beginning and the second element will be
# the text for the line
#
# sort_statements() will take all of the line numbers and corresponding texts and write a file with the lines in
# file containing the movies lines in increasing order based on the LXXXX identifier
#
# set_statements() replaces all of the identifier numbers in newCoversations with the corresponding
# textual line
#
# keyfunc(x) this is just a simple function to help with the sorting
#
# binarySearch(array, start, end, state_val) is a simple function that performs a binary search to find the
# textual line for each corresponding identifier in each pair in the newConversations
#

import re


def get_lines():

    txt = open('conversations')
    new = open('processTest', 'w')

    key = '+++$+++'

    for line in txt.readlines():

        oldLine = str(line)
        newLine = oldLine.split(key)
        new.write(newLine[(len(newLine) - 1)])

    new.close()
    txt.close()


def make_new_con():

    lines = open('lineNumbers')
    new = open('processText2', 'w')

    for line in lines.readlines():

        line = line.split(',')

        if len(line) == 2:

            newConvo = [re.sub('[] [\n]', '', line[0]), re.sub('[] [\n]', '', line[1])]
            new.write(str(newConvo) + '\n')

        else:

            for i in range(len(line) - 1):

                newConvo = [re.sub('[] [\n]', '', line[i]), re.sub('[] [\n]', '', line[i+1])]
                # print(newConvo)
                new.write(str(newConvo) + '\n')

    lines.close()
    new.close()


def get_text():

    txt = open('lineText', encoding='utf8')
    new = open('processText3', 'w')

    key = '+++$+++'

    for line in txt.readlines():

        # print(line)
        line = line.split(key)
        formedText = [re.sub('[\n ""]', '', line[0]), re.sub('[\n""]', '', line[len(line) - 1])]
        new.write(str(formedText) + '\n')

    txt.close()
    new.close()


def sort_statements():

    sortedState = open('sortedStatements', 'w')
    statements = open('statements')

    linesToSort = []

    for lines in statements.readlines():

        lines = lines.split(',')
        state = re.sub('[][ ""]', '', lines[0])
        respon = re.sub('[][""\n]', '', lines[1])

        linesToSort.append([state, respon])

    linesToSort.sort(key=keyfunc)

    for group in linesToSort:

        sortedState.write(str(group) + '\n')

    sortedState.close()


def set_statements():

    sortedState = open('sortedStatements')
    convos = open('newConversations')
    processed = open('processTest4', 'w')

    textLinesArray = []

    for group in sortedState.readlines():

        group = group.split(',')
        key = group[0][4:len(group[0]) - 2]
        line = group[1][4:len(group[1]) - 3]

        textLinesArray.append([key, line])

    for lines in convos.readlines():

        lines = lines.split(',')
        state = int(lines[0][4:len(lines[0]) - 2])
        respon = int(lines[1][4:len(lines[1]) - 4])

        result_state = binarySearch(textLinesArray, 0, len(textLinesArray), state)
        result_respon = binarySearch(textLinesArray, 0, len(textLinesArray), respon)

        if result_state[0] == " ":

            result_state = result_state[1:len(result_state)]

        if result_state[len(result_state) - 1] == "'":

            result_state = result_state[0:len(result_state) - 1]

        if result_respon[len(result_respon) - 1] == "'":

            result_respon = result_respon[0:len(result_respon) - 1]

        # newLines = []

        # newLines.insert(0, result_state)
        # newLines.insert(1, result_respon)

        processed.write(result_state + " / " + result_respon + '\n')

    sortedState.close()
    convos.close()
    processed.close()


def keyfunc(x):

    return int(x[0][2:len(x[0]) - 1])


def binarySearch(array, start, end, state_val):

    mid = int((start + end) / 2)

    if int(state_val) == int(array[mid][0]):

        return array[mid][1]

    elif int(state_val) > int(array[mid][0]):

        return binarySearch(array, mid, end, state_val)

    elif int(state_val) < int(array[mid][0]):

        return binarySearch(array, start, mid, state_val)


# get_lines()
# make_new_con()
# get_text()
# sort_statements()
set_statements()
