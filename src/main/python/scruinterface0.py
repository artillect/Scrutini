# Interface 0 (Text, Command Line) Instructions
import scrudb
from scruclasses import *
import datetime
from pathlib import Path
import os
import csv


def verify():
    # a generic pop up to verify a choice, such as in the case of deletion
    # returns: 1 if the user chooses yes, 0 otherwise
    entry = input("Are you sure? (y/N) ")

    if ((entry == 'Y') or (entry == 'y') or (entry == 'yes') or (entry == 'Yes')):
        return 1
    else:
        return 0


def form_new_judge(comp_id):
    # A form to create a new judge
    # param: comp_id (expected int) <-- indicates which competition to add the judge to
    # returns: Judge (object of type Judge)
    firstName = ''
    while (firstName == ''):
        firstName = input('First name: ')
    lastName = ''
    while (lastName == ''):
        lastName = input('Last name: ')
    judge = Judge(0, firstName, lastName, comp_id)
    judge = scrudb.insert_judge(judge)
    return judge


def form_edit_judge(judge):
    # A form to change the name of a judge
    # param: judge (type Judge)
    # returns: Judge (object of type Judge)
    #judge = scrudb.retrieve_judge(int(id))
    print('Current first name: %s' % judge.firstName)
    firstName = input('New first name: ')
    if (firstName != ''):
        judge.firstName = firstName
    print('Current last name: %s' % judge.lastName)
    lastName = input('New last name: ')
    if (lastName != ''):
        judge.lastName = lastName
    judge = scrudb.update_judge(judge)
    return judge


def menu_judges(comp_id):
    # a menu to allow the user to view/add/choose judges for a competition
    # param: comp_id (expected int)
    loop = 1
    while loop > 0:
        judges = scrudb.retrieve_judges_by_competition(comp_id)
        judges_list = [0, 0]
        for judge in judges:
            #judge = Judge(row[0],row[1],row[2],row[3])
            #id, firstName, lastName, competition = row
            print('( %2d ) %s %s' %
                  (judge.id, judge.firstName, judge.lastName))
            judges_list.append(judge.id)
        print('(  N ) New Judge')
        print('(  X ) Exit')
        entry = input()
        if ((entry == 'N') or (entry == 'n')):
            form_new_judge(comp_id)
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry.isdigit()):
            if ((int(entry) in judges_list) and (int(entry) != 0)):
                menu_judge(int(entry))
            else:
                print('Judge not found.')
        else:
            print('Please choose an option.')


def select_judge(comp_id):
    # allows the user to select a judge
    # param: comp_id (expected int)
    #returns: Judge
    loop = 1
    while loop > 0:
        judges = scrudb.retrieve_judges_by_competition(comp_id)
        judges_list = [0, 0]
        for judge in judges:
            #judge = Judge(row[0],row[1],row[2],row[3])
            #id, firstName, lastName, competition = row
            print('( %2d ) %s %s' %
                  (judge.id, judge.firstName, judge.lastName))
            judges_list.append(judge.id)
        print('(  N ) New Judge')
        entry = input()
        if ((entry == 'N') or (entry == 'n')):
            return form_new_judge(comp_id)
        elif (entry.isdigit()):
            if ((int(entry) in judges_list) and (int(entry) != 0)):
                return scrudb.retrieve_judge(int(entry))
            else:
                print('Judge not found.')
        else:
            print('Please choose an option.')


def menu_judge(id):
    # a menu to allow user to edit/delete a judge
    # param: id (expected int, but other numerical representation that can be converted with int() is okay)
    loop = 1
    while (loop > 0):
        judge = scrudb.retrieve_judge(int(id))
        print('Judge: ( %2d ) %s %s' %
              (judge.id, judge.firstName, judge.lastName))
        print("What do you want to do?")
        print("( 1 ) Edit Judge details")
        print("( D ) Delete Judge")
        print("( X ) Exit")
        entry = input()
        if ((entry == 'D') or (entry == 'd')):
            new_verify = verify()
            if (new_verify == 1):
                print("Removing judge")
                scrudb.rm_judge(int(id))
                loop = 0
            else:
                print("Okay, action canceled.")
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry == '1'):
            judge = form_edit_judge(judge)


def select_dancer_by_competition(comp_id):
    # allows the user to choose a dancer or make a new one
    #returns: Dancer
    loop = 1
    starting_record = 0
    previous_starting_records = [0]
    while (loop > 0):
        print("Choose a competitor:")
        dancers = scrudb.retrieve_dancers_by_competition(comp_id)
        dancers_list = [0]
        total_records = 0
        last_record = 0
        listed_records = 0
        for dancer in dancers:
            #dancer = Dancer(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18])
            #id, firstName, lastName, scotDanceNum, street, city, state, zipCode, birthdate, age, registeredDate, number, phonenum, email, teacher, teacherEmail, dancerCat, dancerGroup, competition
            total_records += 1
            last_record = dancer.id
            if ((dancer.id > starting_record) and (len(dancers_list) <= 10)):
                dancers_list.append(dancer.id)
                listed_records += 1
                print('(%2d) %-15s %-15s (%3s) | %s, %s' % ((len(dancers_list)-1),
                                                            dancer.firstName, dancer.lastName, dancer.number, dancer.city, dancer.state))
        if ((listed_records < total_records) and (starting_record > 0)):
            print('( P) Previous entries')
        if ((listed_records < total_records) and (last_record > dancers_list[-1])):
            print('( M) Show More entries')
        print('( N) New Competitor')
        print('( X) Exit')
        entry = input()
        if (((entry == 'M') or (entry == 'm')) and (listed_records < total_records) and (last_record > dancers_list[-1])):
            previous_starting_records.append(starting_record)
            starting_record = dancers_list[-1]
        elif (((entry == 'P') or (entry == 'p')) and (listed_records < total_records) and (starting_record > 0)):
            starting_record = previous_starting_records.pop()
        elif ((entry == 'N') or (entry == 'n')):
            return form_new_dancer(comp_id)
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry.isdigit()):
            if ((int(entry) <= len(dancers_list)) and (int(entry) > 0)):
                #dancer = scrudb.retrieve_dancer(dancers_list[int(entry)])
                menu_dancer(dancers_list[int(entry)])
            else:
                print('Competitor not found.')
        else:
            print('Please choose an option.')


def select_dancer_by_dancerGroup(dancerGroup_id):
    # allows the user to choose a dancer or make a new one
    #returns: Dancer
    loop = 1
    starting_record = 0
    previous_starting_records = [0]
    while (loop > 0):
        print("Choose a competitor:")
        dancers = scrudb.retrieve_dancers_by_dancerGroup(dancerGroup_id)
        dancers_list = [0]
        total_records = 0
        last_record = 0
        listed_records = 0
        dancers_list = [0]
        for row in dancers:
            if (row != None):
                dancer = row
                total_records += 1
                last_record = int(dancer.id)
                if ((dancer.id > starting_record) and (len(dancers_list) <= 10)):
                    dancers_list.append(dancer.id)
                    # dancers_numbers_list.append(int(dancer.number))
                    listed_records += 1
                    print('(%2d) %-15s %-15s (%3s) | %s, %s' % ((len(dancers_list)-1),
                                                                dancer.firstName, dancer.lastName, dancer.number, dancer.city, dancer.state))
        if ((listed_records < total_records) and (starting_record > 0)):
            print('( P) Previous entries')
        if ((listed_records < total_records) and (last_record > dancers_list[-1])):
            print('( M) Show More entries')
        print('( N) New Competitor')
        print('( X) Exit')
        entry = input()
        if (((entry == 'M') or (entry == 'm')) and (listed_records < total_records) and (last_record > dancers_list[-1])):
            previous_starting_records.append(starting_record)
            starting_record = dancers_list[-1]
        elif (((entry == 'P') or (entry == 'p')) and (listed_records < total_records) and (starting_record > 0)):
            starting_record = previous_starting_records.pop()
        elif ((entry == 'N') or (entry == 'n')):
            return form_new_dancer_by_dancerGroup(dancerGroup_id)
            #print('New Dancer')
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry.isdigit()):
            if ((int(entry) <= len(dancers_list)) and (int(entry) > 0)):
                #dancer = scrudb.retrieve_dancer(dancers_list[int(entry)])
                menu_dancer(dancers_list[int(entry)])
            else:
                print('Competitor not found.')
        else:
            print('Please choose an option.')


def select_event(comp_id):
    # allows the user to choose an event
    #returns: event
    loop = 1
    starting_record = 0
    previous_starting_records = [0]
    while (loop > 0):
        print("Choose an event:")
        events = scrudb.retrieve_events_by_competition(comp_id)
        events_list = [0]
        total_records = 0
        last_record = 0
        listed_records = 0
        events_list = [0]
        for event in events:
            if (event != None):
                # print(row)
                #event = Event(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                total_records += 1
                last_record = int(event.id)
                if ((event.id > starting_record) and (len(events_list) <= 10)):
                    events_list.append(event.id)
                    listed_records += 1
                    print('(%2d) %s' % ((len(events_list)-1), event.name))
        if ((listed_records < total_records) and (starting_record > 0)):
            print('( P) Previous entries')
        if ((listed_records < total_records) and (last_record > events_list[-1])):
            print('( M) Show More entries')
        #print ('( N) New Competitor')
        print('( X) Exit')
        entry = input()
        if (((entry == 'M') or (entry == 'm')) and (listed_records < total_records) and (last_record > events_list[-1])):
            previous_starting_records.append(starting_record)
            starting_record = events_list[-1]
        elif (((entry == 'P') or (entry == 'p')) and (listed_records < total_records) and (starting_record > 0)):
            starting_record = previous_starting_records.pop()
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry.isdigit()):
            if ((int(entry) <= len(events_list)) and (int(entry) > 0)):
                return scrudb.retrieve_event(events_list[int(entry)])
            else:
                print('Event not found.')
        else:
            print('Please choose an option.')


def enter_scores_for_event(event_id):
    event = scrudb.retrieve_event(event_id)
    print('Event: %s' % event.name)
    if (scrudb.exists_scores_for_event(event_id)):
        print('These scores were already entered.')
        view_results_for_event(event_id)
        entry = input('Overwrite? (y/N) ')
        if ((entry == 'Y') or (entry == 'y') or (entry == 'yes') or (entry == 'Yes')):
            scrudb.rm_scores_by_event(event_id)
            enter_scores_for_event(event_id)
        else:
            print('Ok.')
    else:
        dancers = scrudb.retrieve_dancers_by_dancerGroup_ordered_by_number(
            event.dancerGroup)
        scores = {}
        if (dancers != None):
            for dancer in dancers:
                if (dancer != None):
                    entry = get_input_as_float(
                        ('Dancer %s' % dancer.number), 0)
                    print(entry)  # should store the score
                    scores[('%d' % dancer.id)] = entry
            for dancer_id in scores:
                dancer = scrudb.retrieve_dancer(int(dancer_id))
                print('%s: %f' % (dancer.lastName, scores[dancer_id]))
                score = Score(0, dancer.id, event_id, 0,
                              event.competition, scores[dancer_id])
                score = scrudb.insert_score(score)
                #id, dancer, event, judge, competition, score


def get_score_value(score):
    return score.score


def view_results_for_event(event_id):
    event = scrudb.retrieve_event(event_id)
    print('Event: %s' % event.name)
    scores = scrudb.retrieve_scores_by_event(event.id)
    scores.sort(key=get_score_value, reverse=True)
    place = 1
    for score in scores:
        dancer = scrudb.retrieve_dancer(score.dancer)
        print('%d - (%s) %s %s - %s, %s: %f' % (place, dancer.number,
                                                dancer.firstName, dancer.lastName, dancer.city, dancer.state, score.score))
        place += 1


def view_results_for_dancerGroup(dancerGroup_id):
    dancerGroup = scrudb.retrieve_dancerGroup(dancerGroup_id)
    print('Competitor Group: %s' % dancerGroup.name)
    events = scrudb.retrieve_events_by_dancerGroup(dancerGroup_id)
    dancer_scores = {}
    dancers = scrudb.retrieve_dancers_by_dancerGroup(dancerGroup_id)
    for dancer in dancers:
        dancer_id = ('%d' % dancer.id)
        dancer_scores[dancer_id] = 0
    for event in events:
        #event = Event(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        #id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp
        # view_results_for_event(event.id)
        print('Event: %s' % event.name)
        scores = scrudb.retrieve_scores_by_event(event.id)
        scores.sort(key=get_score_value, reverse=True)
        place = 1
        last_score = 0.0
        while (place <= event.numPlaces):
            for score in scores:
                if (score.score > 0.0):
                    dancer = scrudb.retrieve_dancer(score.dancer)
                    print('%d - (%s) %s %s - %s, %s: %f' % (place, dancer.number,
                                                            dancer.firstName, dancer.lastName, dancer.city, dancer.state, score.score))
                    dancer_id = ('%d' % dancer.id)
                    # if (score.score == last_score):
                    #    place -= 1
                    if (event.countsForOverall == 1):
                        if ((place == 1) and (score.score != 0.0)):
                            dancer_scores[dancer_id] += 137
                        elif ((place == 2) and (score.score != 0.0)):
                            dancer_scores[dancer_id] += 91
                        elif ((place == 3) and (score.score != 0.0)):
                            dancer_scores[dancer_id] += 71
                        elif ((place == 4) and (score.score != 0.0)):
                            dancer_scores[dancer_id] += 53
                        elif ((place == 5) and (score.score != 0.0)):
                            dancer_scores[dancer_id] += 37
                        elif ((place == 6) and (score.score != 0.0)):
                            dancer_scores[dancer_id] += 23
                place += 1
                last_score = score.score
            place = event.numPlaces + 1
        print('')
        # print(dancer_scores)
    # print(dancer_scores)
    dancer_scores_sorted = sorted(
        dancer_scores.items(), key=lambda x: x[1], reverse=True)
    place = 1
    # print(dancer_scores_sorted)
    last_score = 0.0
    print('Overall results for group %s' % dancerGroup.name)
    for k, v in dancer_scores_sorted:
        if ((v == last_score) and (v != 0.0)):
            place -= 1
        elif (v == 0.0):
            place = 0
        dancer = scrudb.retrieve_dancer(int(k))
        print('%d - (%s) %s %s - %s, %s (Points: %f)' % (place, dancer.number,
                                                         dancer.firstName, dancer.lastName, dancer.city, dancer.state, v))
        place += 1


def menu_scrutineer(comp_id):
    loop = 1
    while (loop > 0):
        print('(1) Enter scores')
        print('(2) View results by event')
        print('(3) View results by competitor group')
        print('(X) Exit')
        entry = input()
        if ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry == '1'):
            event = select_event(comp_id)
            if (event != None):
                enter_scores_for_event(event.id)
        elif (entry == '2'):
            event = select_event(comp_id)
            if (event != None):
                view_results_for_event(event.id)
        elif (entry == '3'):
            dancerGroup = select_dancerGroup(comp_id)
            if (dancerGroup != None):
                view_results_for_dancerGroup(dancerGroup.id)


def menu_dancer(id):
    # a menu to allow user to edit/delete a dancer
    # param: id (expected int, but other numerical representation that can be converted with int() is okay)
    loop = 1
    while (loop > 0):
        dancer = scrudb.retrieve_dancer(int(id))
        dancerGroups = scrudb.retrieve_dancerGroups_by_dancer(int(id))
        print('Competitor: (%3s) %-15s %-15s | %s, %s' % (dancer.number,
                                                          dancer.firstName, dancer.lastName, dancer.city, dancer.state))
        if (len(dancerGroups) > 0):
            print('Competitor groups:')
            for row in dancerGroups:
                if (row != None):
                    dancerCat = scrudb.retrieve_dancerCat(row.dancerCat)
                    if (row.ageMax == 99):
                        age_string = ('%d+' % row.ageMin)
                    else:
                        age_string = ('%d-%d' % (row.ageMin, row.ageMax))
                    print('(%-3s) %25s | %s %s' %
                          (row.abbrev, row.name, dancerCat.abbrev, age_string))
        print("What do you want to do?")
        print("( 1 ) Edit Competitor details")
        print("( 2 ) Assign to Group")
        print("( 3 ) Remove from Group")
        print("( D ) Delete Competitor")
        print("( X ) Exit")
        entry = input()
        if ((entry == 'D') or (entry == 'd')):
            new_verify = verify()
            if (new_verify == 1):
                print("Removing competitor")
                scrudb.rm_dancer(int(id))
                loop = 0
            else:
                print("Okay, action canceled.")
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry == '1'):
            dancer = form_edit_dancer(dancer)
        elif (entry == '2'):
            dancerGroup = select_dancerGroup(dancer.competition)
            scrudb.insert_dancerGroupJoin(dancer.id, dancerGroup.id)
            #event = menu_events_by_dancerGroup(dancerGroup.id)
        elif (entry == '3'):
            dancerGroup = select_dancerGroup_by_dancer(dancer.id)
            if (dancerGroup != None):
                scrudb.rm_dancerGroupJoin_by_dancer_and_dancerGroup(
                    dancer.id, dancerGroup.id)


def select_dancerGroup_by_dancer(dancer_id):
    loop = 1
    while (loop > 0):
        dancer = scrudb.retrieve_dancer(dancer_id)
        dancerGroups = scrudb.retrieve_dancerGroups_by_dancer(dancer_id)
        dancerGroups_list = [0]
        print('Competitor: (%3s) %-15s %-15s | %s, %s' % (dancer.number,
                                                          dancer.firstName, dancer.lastName, dancer.city, dancer.state))
        if (dancerGroups != None):
            if (len(dancerGroups) > 0):
                for row in dancerGroups:
                    if (row != None):
                        dancerGroup = row
                        dancerGroups_list.append(dancerGroup.id)
                        dancerCat = scrudb.retrieve_dancerCat(
                            dancerGroup.dancerCat)
                        if (dancerGroup.ageMax == 99):
                            age_string = ('%d+' % dancerGroup.ageMin)
                        else:
                            age_string = (
                                '%d-%d' % (dancerGroup.ageMin, dancerGroup.ageMax))
                        print('(%2d) %25s (%-3s) | %s %s' % ((len(dancerGroups_list)-1),
                                                             dancerGroup.name, dancerGroup.abbrev, dancerCat.abbrev, age_string))
                    else:
                        # this doesn't print!
                        print('Competitor is in no groups')
            else:
                print('Competitor is in no groups')  # this does
        else:
            print('Competitor is in no groups')  # neither does this!
        print('(X) Exit')
        entry = input()
        if ((entry == 'X') or (entry == 'x')):
            return None
        elif (entry.isdigit()):
            if ((int(entry) <= len(dancerGroups_list)) and (int(entry) > 0)):
                return scrudb.retrieve_dancerGroup(dancerGroups_list[int(entry)])
            else:
                print('Competitor not found.')
        else:
            print('Please choose an option.')


def get_input_as_int(prompt, required):
    entry = 't'
    while (entry.isdigit() == False):
        entry = input('%s: ' % prompt)
        if ((required == 0) and (entry.isdigit() == False)):
            entry = '0'
    return int(entry)


def get_input_as_float(prompt, required):
    entry = 't'
    while (is_float(entry) == False):
        entry = input('%s: ' % prompt)
        if ((required == 0) and (is_float(entry) == False)):
            entry = '0'
    return float(entry)


def is_float(string):
    try:
        val = float(string)
        return True
    except ValueError:
        return False


def get_edit(key, original):
    print('Current %s: %s' % (key, original))
    entry = input('New %s (hit Enter to keep \"%s\"): ' % (key, original))
    if (entry != ''):
        return entry
    else:
        return original


def get_edit_as_int(key, original):
    print('Current %s: %d' % (key, original))
    entry = input('New %s (hit Enter to keep %d): ' % (key, original))
    if (entry.isdigit()):
        return int(entry)
    else:
        return original


def form_edit_dancer(dancer):
    # a form to edit a dancer
    # param: dancer (object of type Dancer)
    # returns: dancer (object of type Dancer)
    dancer.firstName = get_edit('First Name', dancer.firstName)
    dancer.lastName = get_edit('Last Name', dancer.lastName)
    dancer.number = get_edit('Competitor Number', dancer.number)
    dancer.scotDanceNum = get_edit('ScotDance Number', dancer.scotDanceNum)
    dancer.street = get_edit('Street Address', dancer.street)
    dancer.city = get_edit('City', dancer.city)
    dancer.state = get_edit('State/Province', dancer.state)
    dancer.zipCode = get_edit('Zip/Postal Code', dancer.zipCode)
    print('Current birthdate: %s' % dancer.birthdate)
    dancer_birthdate = select_date('New Birthdate', 1)
    if (dancer_birthdate != ''):
        dancer.birthdate = dancer_birthdate
    dancer.age = get_edit_as_int('Age', dancer.age)
    print('Current registration date: %s' % dancer.registeredDate)
    dancer_entryReceived = select_date('New registration date', 1)
    if (dancer_entryReceived != ''):
        dancer.registeredDate = dancer_entryReceived
    dancer.phonenum = get_edit('Phone Number', dancer.phonenum)
    dancer.email = get_edit('Email', dancer.email)
    dancer.teacher = get_edit('Teacher\'s Name', dancer.teacher)
    dancer.teacherEmail = get_edit('Teacher\'s Email', dancer.teacherEmail)
    dancerCat = scrudb.retrieve_dancerCat(dancer.dancerCat)
    print('Current Category: %s' % dancerCat.name)
    entry = input("Do you want to change %s %s\'s category? (y/N) ")
    if ((entry == 'y') or (entry == 'Y') or (entry == 'yes') or (entry == 'Yes')):
        dancerCat = select_dancerCat()
        dancer.dancerCat = dancerCat.id
    return scrudb.update_dancer(dancer)


def form_new_dancer_by_dancerGroup(dancerGroup_id):
    # a form to create a new dancer within a dancerGroup
    # returns: dancer (object of type Dancer)
    dancer_firstName = ''
    while (dancer_firstName == ''):
        dancer_firstName = input('*First Name: ')
    dancer_lastName = ''
    while (dancer_lastName == ''):
        dancer_lastName = input('*Last Name: ')
    dancer_number = ''
    while (dancer_number == ''):
        dancer_number = input('*Competitor Number: ')
    dancer_scotDanceNum = input('ScotDance Number: ')
    dancer_street = input('Street Address: ')
    dancer_city = input('City: ')
    dancer_state = input('State/Province: ')
    dancer_zipCode = input('Zip/Postal Code: ')
    dancer_birthdate = select_date('Birthdate', 1)
    dancer_age_input = input('Age (as of competition): ')
    if (dancer_age_input.isdigit()):
        dancer_age = int(dancer_age_input)
    else:
        dancer_age = 0
    dancer_entryReceived = select_date('Date entry received', 1)
    dancer_phone = input('Phone Number: ')
    dancer_email = input('Email: ')
    dancer_teacher = input('Teacher\'s Name: ')
    dancer_teacherEmail = input('Teacher\'s Email: ')
    dancer_cat = select_dancerCat()
    dancerCat = dancer_cat.id
    dancerGroup = scrudb.retrieve_dancerGroup(dancerGroup_id)
    comp_id = dancerGroup.competition
    #id, firstName, lastName, scotDanceNum, street, city, state, zipCode, birthdate, age, registeredDate, number, phonenum, email, teacher, teacherEmail, dancerCat, dancerGroup, competition
    dancer = Dancer(0, dancer_firstName, dancer_lastName, dancer_scotDanceNum, dancer_street, dancer_city, dancer_state, dancer_zipCode, dancer_birthdate, int(
        dancer_age), dancer_entryReceived, dancer_number, dancer_phone, dancer_email, dancer_teacher, dancer_teacherEmail, dancerCat, 0, comp_id)
    dancer = scrudb.insert_dancer(dancer)
    print('Adding dancer to group %s...' % dancerGroup.name)
    scrudb.insert_dancerGroupJoin(dancer.id, dancerGroup.id)
    entry = 'Y'
    while ((entry == 'Y') or (entry == 'y') or (entry == 'yes') or (entry == 'Yes')):
        entry = input('Would you like to add competitor %s %s to any other groups? (y/N) ' %
                      (dancer.firstName, dancer.lastName))
        if ((entry == 'Y') or (entry == 'y') or (entry == 'yes') or (entry == 'Yes')):
            dancerGroup = select_dancerGroup(comp_id)
            scrudb.insert_dancerGroupJoin(dancer.id, dancerGroup.id)
    return dancer


def form_new_dancer(comp_id):
    # a form to create a new dancer within a competition
    # returns: dancer (object of type Dancer)
    dancer_firstName = ''
    while (dancer_firstName == ''):
        dancer_firstName = input('*First Name: ')
    dancer_lastName = ''
    while (dancer_lastName == ''):
        dancer_lastName = input('*Last Name: ')
    dancer_number = ''
    while (dancer_number == ''):
        dancer_number = input('*Competitor Number: ')
    dancer_scotDanceNum = input('ScotDance Number: ')
    dancer_street = input('Street Address: ')
    dancer_city = input('City: ')
    dancer_state = input('State/Province: ')
    dancer_zipCode = input('Zip/Postal Code: ')
    dancer_birthdate = select_date('Birthdate', 1)
    dancer_age_input = input('Age (as of competition): ')
    if (dancer_age_input.isdigit()):
        dancer_age = int(dancer_age_input)
    else:
        dancer_age = 0
    dancer_entryReceived = select_date('Date entry received', 1)
    dancer_phone = input('Phone Number: ')
    dancer_email = input('Email: ')
    dancer_teacher = input('Teacher\'s Name: ')
    dancer_teacherEmail = input('Teacher\'s Email: ')
    dancer_cat = select_dancerCat()
    dancerCat = dancer_cat.id
    #dancerGroup = scrudb.retrieve_dancerGroup(dancerGroup_id)
    #comp_id = dancerGroup.competition
    #id, firstName, lastName, scotDanceNum, street, city, state, zipCode, birthdate, age, registeredDate, number, phonenum, email, teacher, teacherEmail, dancerCat, dancerGroup, competition
    dancer = Dancer(0, dancer_firstName, dancer_lastName, dancer_scotDanceNum, dancer_street, dancer_city, dancer_state, dancer_zipCode, dancer_birthdate, int(
        dancer_age), dancer_entryReceived, dancer_number, dancer_phone, dancer_email, dancer_teacher, dancer_teacherEmail, dancerCat, 0, comp_id)
    dancer = scrudb.insert_dancer(dancer)
    #print('Adding dancer to group %s...' % dancerGroup.name)
    # scrudb.insert_dancerGroupJoin(dancer.id,dancerGroup.id)
    entry = 'Y'
    while ((entry == 'Y') or (entry == 'y') or (entry == 'yes') or (entry == 'Yes')):
        entry = input('Would you like to add competitor %s %s to any groups? (y/N) ' %
                      (dancer.firstName, dancer.lastName))
        if ((entry == 'Y') or (entry == 'y') or (entry == 'yes') or (entry == 'Yes')):
            dancerGroup = select_dancerGroup(comp_id)
            scrudb.insert_dancerGroupJoin(dancer.id, dancerGroup.id)
    return dancer


def select_competition():
    # allows the user to choose a competition or make a new one
    #returns: Competition
    loop = 1
    starting_record = 0
    previous_starting_records = [0]
    while (loop > 0):
        print("Choose a competition:")
        competitions = scrudb.retrieve_competitions()
        competitions_list = [0]
        total_records = 0
        last_record = 0
        listed_records = 0
        for comp in competitions:
            #comp = Competition(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            #id, name, description, eventDate, deadline, location, competitionType, isChampionship
            format_str = '%m/%d/%y'
            otherformat_str = '%Y-%m-%d %H:%M:%S'
            compDate = (datetime.datetime.strftime(datetime.datetime.strptime(
                ('%s' % comp.eventDate), otherformat_str).date(), format_str))
            total_records += 1
            last_record = comp.id
            if ((comp.id > starting_record) and (len(competitions_list) <= 10)):
                competitions_list.append(comp.id)
                listed_records += 1
                print('(%2d) %-25s (%8s) | %s' %
                      ((len(competitions_list)-1), comp.name, compDate, comp.location))
        if ((listed_records < total_records) and (starting_record > 0)):
            print('( P) Previous entries')
        if ((listed_records < total_records) and (last_record > competitions_list[-1])):
            print('( M) Show More entries')
        print('( N) New Competition')
        #print ('(  X ) Exit')
        entry = input()
        if (((entry == 'M') or (entry == 'm')) and (listed_records < total_records) and (last_record > competitions_list[-1])):
            previous_starting_records.append(starting_record)
            starting_record = competitions_list[-1]
        elif (((entry == 'P') or (entry == 'p')) and (listed_records < total_records) and (starting_record > 0)):
            starting_record = previous_starting_records.pop()
        elif ((entry == 'N') or (entry == 'n')):
            return form_new_competition()
        # elif ((entry == 'X') or (entry == 'x')):
        #    loop = 0
        elif (entry.isdigit()):
            if ((int(entry) <= len(competitions_list)) and (int(entry) > 0)):
                return scrudb.retrieve_competition(competitions_list[int(entry)])
            else:
                print('Competition not found.')
        else:
            print('Please choose an option.')


def select_dancerCat():
    # allows the user to choose a category or make a new one
    #returns: DancerCat
    loop = 1
    while (loop > 0):
        print("Choose a category:")
        dancerCats = scrudb.retrieve_dancerCats()
        dancerCats_list = [0, 0]
        for dancerCat in dancerCats:
            #dancerCat = DancerCat(row[0],row[1],row[2],row[3])
            #id, name, abbrev, protected
            print('( %2d ) %-25s (%3s)' %
                  (dancerCat.id, dancerCat.name, dancerCat.abbrev))
            dancerCats_list.append(dancerCat.id)
        entry = input()
        if (entry.isdigit()):
            if ((int(entry) in dancerCats_list) and (int(entry) != 0)):
                return scrudb.retrieve_dancerCat(int(entry))
            else:
                print('Category not found.')
        else:
            print('Please choose an option.')


def select_dancerGroup(comp_id):
    # a menu to allow the user to select a dancerGroup
    # param: comp_id (expected int)
    #returns: DancerGroup
    loop = 1
    while loop > 0:
        dancerGroups = scrudb.retrieve_dancerGroups_by_competition(comp_id)
        dancerGroups_list = [0, 0]
        for dancerGroup in dancerGroups:
            #dancerGroup = DancerGroup(row[0],row[1],row[2],row[3], row[4], row[5], row[6])
            #id, name, abbrev, ageMin, ageMax, dancerCat, competition = row
            dancerCat = scrudb.retrieve_dancerCat(dancerGroup.dancerCat)
            print('( %2d ) %-25s |%-3s| %s %d-%d' % (dancerGroup.id, dancerGroup.name,
                                                     dancerGroup.abbrev, dancerCat.abbrev, dancerGroup.ageMin, dancerGroup.ageMax))
            dancerGroups_list.append(dancerGroup.id)
        #print ('(  N ) New Competitor Group')
        #print ('(  X ) Exit')
        entry = input()
        if ((entry == 'N') or (entry == 'n')):
            return form_new_dancerGroup(comp_id)
        elif (entry.isdigit()):
            if ((int(entry) in dancerGroups_list) and (int(entry) != 0)):
                return scrudb.retrieve_dancerGroup(int(entry))
            else:
                print('Dancer Group not found.')
        else:
            print('Please choose an option.')


def menu_dancerGroup(id):
    # a menu to allow user to edit/delete a dancerGroup
    # param: id (expected int, but other numerical representation that can be converted with int() is okay)
    loop = 1
    while (loop > 0):
        dancerGroup = scrudb.retrieve_dancerGroup(int(id))
        dancerCat = scrudb.retrieve_dancerCat(dancerGroup.dancerCat)
        print('Competitor Group: ( %2s ) %-25s | %s %d-%d' % (dancerGroup.abbrev,
                                                              dancerGroup.name, dancerCat.abbrev, dancerGroup.ageMin, dancerGroup.ageMax))
        print("What do you want to do?")
        print("(1) Edit Group details")
        print("(2) Select Dances")
        print("(3) Add/Edit/View Competitors")
        print("(D) Delete Group")
        print("(X) Exit")
        entry = input()
        if ((entry == 'D') or (entry == 'd')):
            new_verify = verify()
            if (new_verify == 1):
                print("Removing group")
                scrudb.rm_danceGroup(int(id))
                loop = 0
            else:
                print("Okay, action canceled.")
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry == '1'):
            dancerGroup = form_edit_dancerGroup(dancerGroup)
        elif (entry == '2'):
            event = menu_events_by_dancerGroup(dancerGroup.id)
        elif (entry == '3'):
            dancer = select_dancer_by_dancerGroup(dancerGroup.id)


def menu_dancerGroups(comp_id):
    # a menu to allow the user to view/add/edit dancerGroups for a competition
    # param: comp_id (expected int)
    loop = 1
    while loop > 0:
        dancerGroups = scrudb.retrieve_dancerGroups_by_competition(comp_id)
        dancerGroups_list = [0, 0]
        for dancerGroup in dancerGroups:
            #dancerGroup = DancerGroup(row[0],row[1],row[2],row[3], row[4], row[5], row[6])
            #id, name, abbrev, ageMin, ageMax, dancerCat, competition = row
            dancerCat = scrudb.retrieve_dancerCat(dancerGroup.dancerCat)
            if (dancerGroup.ageMax == 99):
                dancerAge_string = ('%d+' % dancerGroup.ageMin)
            else:
                dancerAge_string = ('%d-%d' %
                                    (dancerGroup.ageMin, dancerGroup.ageMax))
            print('( %2d ) %-25s |%-3s| %s %s' % (dancerGroup.id, dancerGroup.name,
                                                  dancerGroup.abbrev, dancerCat.abbrev, dancerAge_string))
            dancerGroups_list.append(dancerGroup.id)
        print('(  N ) New Competitor Group')
        print('(  X ) Exit')
        entry = input()
        if ((entry == 'N') or (entry == 'n')):
            dancerGroup = form_new_dancerGroup(comp_id)
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry.isdigit()):
            if ((int(entry) in dancerGroups_list) and (int(entry) != 0)):
                dancerGroup = menu_dancerGroup(int(entry))
            else:
                print('Dancer Group not found.')
        else:
            print('Please choose an option.')


def form_new_dancerGroup(comp_id):
    # A form to create a new dancerGroup
    # param: comp_id (expected int) <-- indicates which competition to add the group to
    # returns: DancerGroup (object of type DancerGroup)
    name = ''
    while (name == ''):
        name = input('Name: ')
    lastName = ''
    abbrev = input('Abbreviation: ')
    dancerCat = select_dancerCat()
    if (dancerCat.abbrev == 'P'):
        ageMin = '4'
        ageMax = '6'
    else:
        ageMin = 't'
        while (ageMin.isdigit() == False):
            ageMin = input('Min. Age: ')
            if (ageMin == ''):
                ageMin = '7'
        ageMax = 't'
        while (ageMax.isdigit() == False):
            ageMax = input('Max. Age: ')
            if (ageMax == ''):
                ageMax = '99'
    dancerGroup = DancerGroup(0, name, abbrev, int(
        ageMin), int(ageMax), dancerCat.id, comp_id)
    dancerGroup = scrudb.insert_dancerGroup(dancerGroup)
    return dancerGroup


def form_edit_dancerGroup(dancerGroup):
    # A form to change the details of a dancerGroup
    # param: dancerGroup (type DancerGroup)
    # returns: DancerGroup (object of type DancerGroup)
    print('Current name: %s' % dancerGroup.name)
    name = input('New name: ')
    if (name != ''):
        dancerGroup.name = name
    print('Current abbreviation: %s' % dancerGroup.abbrev)
    abbrev = input('New abbreviation: ')
    if (abbrev != ''):
        dancerGroup.abbrev = abbrev
    # option to select new DancerCat
    print('Current Min. Age: %d' % dancerGroup.ageMin)
    ageMin = input('New Min. Age: ')
    if ((ageMin != '') and (ageMin.isdigit())):
        dancerGroup.ageMin = int(ageMin)
    print('Current Max. Age: %d' % dancerGroup.ageMax)
    ageMax = input('New Max. Age: ')
    if ((ageMax != '') and (ageMax.isdigit())):
        dancerGroup.ageMax = int(ageMax)
    dancerGroup = scrudb.update_dancerGroup(dancerGroup)
    return dancerGroup


def menu_main():
    # the main menu of the program, user adds/chooses a competition to work with
    loop = 1
    comp = None
    while (loop > 0):
        settings = scrudb.retrieve_settings('current')
        competitions = scrudb.retrieve_competitions()
        competitions_list = [0, 0]
        for comp in competitions:
            #comp = Competition(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            #id, name, description, eventDate, deadline, location, competitionType, isChampionship
            #print ('( %2d ) %-25s (%10s) | %s' % (comp.id, comp.name, comp.eventDate, comp.location))
            competitions_list.append(comp.id)
        if ((settings.lastComp in competitions_list) and (settings.lastComp != 0)):
            comp = scrudb.retrieve_competition(settings.lastComp)
        else:
            comp = select_competition()
            settings.lastComp = comp.id
            scrudb.set_settings(settings)
        format_str = '%m/%d/%y'
        otherformat_str = '%Y-%m-%d %H:%M:%S'
        compDate = (datetime.datetime.strftime(datetime.datetime.strptime(
            ('%s' % comp.eventDate), otherformat_str).date(), format_str))
        print('Competition: %-25s (%8s) | %s' %
              (comp.name, compDate, comp.location))
        print('(1) Scrutineer Competition')
        print('(2) Change competitions')
        print('(3) Edit competition details')
        print('(4) Add/Edit Competitors')
        print('(5) Add/Edit judges')
        print('(6) Define Competitor Groups')
        print('(7) Import CSV')
        print('(D) Delete competition')
        print('(X) Exit')
        entry = input()
        if ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif ((entry == 'D') or (entry == 'd')):
            new_verify = verify()
            if (new_verify == 1):
                print("Removing competition")
                scrudb.rm_competition(int(comp.id))
            else:
                print("Okay, action canceled.")
        elif (entry == '1'):
            menu_scrutineer(comp.id)
        elif (entry == '2'):
            comp = select_competition()
            settings.lastComp = comp.id
            scrudb.set_settings(settings)
        elif (entry == '3'):
            comp = form_edit_competition(comp)
        elif (entry == '4'):
            dancer = select_dancer_by_competition(comp.id)
        elif (entry == '5'):
            menu_judges(comp.id)
        elif (entry == '6'):
            menu_dancerGroups(comp.id)
        elif (entry == '7'):
            csv_filename = select_csv_file()
            process_csv_file(csv_filename, comp.id)
        else:
            print('Please choose an option.')


def process_csv_file(csv_filename, comp_id):
    if os.path.exists(csv_filename):
        reader = scrudb.retrieve_csv_keys(csv_filename)
        if (reader != None):
            key_firstName = select_column(reader, 'First Name')
            key_lastName = select_column(reader, 'Last Name')
            key_street = select_column(reader, 'Street Address')
            key_city = select_column(reader, 'City')
            key_state = select_column(reader, 'State/Province')
            key_zipCode = select_column(reader, 'Zip/Postal Code')
            key_phone = select_column(reader, 'Phone Number')
            key_email = select_column(reader, 'Email')
            key_scotDanceNum = select_column(reader, 'ScotDance Number')
            key_birthdate = select_column(reader, 'Birthdate')
            key_age = select_column(reader, 'Age')
            key_teacher = select_column(reader, 'Teacher')
            key_teacherEmail = select_column(reader, 'Teacher Email')
            key_entryReceived = select_column(
                reader, 'Date Entry was Received')
            key_number = select_column(reader, 'Competitor Number')
            key_grp1 = select_column(reader, 'Primary Competitor Group')
            key_grp2 = select_column(reader, 'Secondary Competitor Group')
            key_grp3 = select_column(reader, 'Tertiary Competitor Group')
            #dict_reader = retrieve_csv_dict(csv_filename)
            with open(csv_filename, newline='') as csvfile:
                dict_reader = csv.DictReader(csvfile)
                for row in dict_reader:
                    # print(row)
                    #print('%s %s - %s, %s - %s |%s|%s|%s' % (row[key_firstName], row[key_lastName], row[key_city], row[key_state], row[key_number], row[key_grp1], row[key_grp2], row[key_grp3]))
                    dancer_firstName = row[key_firstName]
                    dancer_lastName = row[key_lastName]
                    dancer_number = row[key_number]

                    if (key_street != None):
                        dancer_street = row[key_street]
                    else:
                        dancer_street = ''
                    if (key_city != None):
                        dancer_city = row[key_city]
                    else:
                        dancer_city = ''
                    if (key_state != None):
                        dancer_state = row[key_state]
                    else:
                        dancer_state = ''
                    if (key_zipCode != None):
                        dancer_zipCode = row[key_zipCode]
                    else:
                        dancer_zipCode = ''
                    if (key_phone != None):
                        dancer_phone = row[key_phone]
                    else:
                        dancer_phone = ''
                    if (key_email != None):
                        dancer_email = row[key_email]
                    else:
                        dancer_email = ''
                    if (key_scotDanceNum != None):
                        dancer_scotDanceNum = row[key_scotDanceNum]
                    else:
                        dancer_scotDanceNum = ''
                    if (key_birthdate != None):
                        dancer_birthdate = row[key_birthdate]
                    else:
                        dancer_birthdate = ''
                    if (key_age != None):
                        if (row[key_age].isdigit()):
                            dancer_age = int(row[key_age])
                        else:
                            dancer_age = 0
                    else:
                        dancer_age = 0
                    if (key_teacher != None):
                        dancer_teacher = row[key_teacher]
                    else:
                        dancer_teacher = ''
                    if (key_teacherEmail != None):
                        dancer_teacherEmail = row[key_teacherEmail]
                    else:
                        dancer_teacherEmail = ''
                    if (key_entryReceived != None):
                        dancer_entryReceived = row[key_entryReceived]
                    else:
                        dancer_entryReceived = ''
                    if (key_grp1 != None):
                        dancer_grp1 = row[key_grp1]
                    else:
                        dancer_grp1 = ''
                    if (key_grp2 != None):
                        dancer_grp2 = row[key_grp2]
                    else:
                        dancer_grp2 = ''
                    if (key_grp3 != None):
                        dancer_grp3 = row[key_grp3]
                    else:
                        dancer_grp3 = ''
                    dancerGroup_1 = scrudb.retrieve_dancerGroup_by_abbrev(
                        dancer_grp1)
                    dancerGroup_2 = scrudb.retrieve_dancerGroup_by_abbrev(
                        dancer_grp2)
                    dancerGroup_3 = scrudb.retrieve_dancerGroup_by_abbrev(
                        dancer_grp3)
                    #id, firstName, lastName, scotDanceNum, street, city, state, zipCode, birthdate, age, registeredDate, number, phonenum, email, teacher, teacherEmail, dancerCat, dancerGroup, competition
                    dancer = Dancer(0, dancer_firstName, dancer_lastName, dancer_scotDanceNum, dancer_street, dancer_city, dancer_state, dancer_zipCode, dancer_birthdate,
                                    dancer_age, dancer_entryReceived, dancer_number, dancer_phone, dancer_email, dancer_teacher, dancer_teacherEmail, 0, 0, comp_id)
                    dancer = scrudb.insert_dancer(dancer)
                    if (dancerGroup_1 != None):
                        scrudb.insert_dancerGroupJoin(
                            dancer.id, dancerGroup_1.id)
                    if (dancerGroup_2 != None):
                        scrudb.insert_dancerGroupJoin(
                            dancer.id, dancerGroup_2.id)
                    if (dancerGroup_3 != None):
                        scrudb.insert_dancerGroupJoin(
                            dancer.id, dancerGroup_3.id)
                    # print(dancer)
    else:
        print('File not found.')


def select_column(reader, prompt):
    loop = 1
    while (loop > 0):
        print('Choose a column that holds values for \"%s\" (Enter for none):' % prompt)
        x = 0
        for item in reader:
            print('(%3d) %s' % (x, item))
            x += 1
        entry = input('Enter the number of the column (hit Enter for none): ')
        if (entry == ''):
            return None
        elif (entry.isdigit()):
            if ((int(entry) >= 0) and (int(entry) < x)):
                return reader[int(entry)]
            else:
                print('Please choose from available columns.')
        else:
            print('Please enter a number.')


def form_edit_event(event):
    dancerGroup = scrudb.retrieve_dancerGroup(event.dancerGroup)
    dance = scrudb.retrieve_dance(event.dance)
    print('Current dance: %s' % dance.name)
    entry = input('Change dance? (y/N) ')
    if ((entry == 'Y') or (entry == 'y') or (entry == 'yes') or (entry == 'Yes')):
        dance = select_dance()  # this really should be a picker
    name = ('%s - %s' % (dancerGroup.name, dance.name))
    numPlaces = 't'
    while (numPlaces.isdigit() == False):
        numPlaces = input('How many places will be awarded? ')
    entry = input("Will this event earn a stamp for group %s? (Y/n) " %
                  dancerGroup.name)
    if ((entry == 'N') or (entry == 'n') or (entry == 'no') or (entry == 'No')):
        earnsStamp = 0
    else:
        earnsStamp = 1
    entry = input(
        "Will this event count toward the overall trophy for group %s? (Y/n)" % dancerGroup.name)
    if ((entry == 'N') or (entry == 'n') or (entry == 'no') or (entry == 'No')):
        countsForOverall = 0
    else:
        countsForOverall = 1
    #id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp
    event = scrudb.update_event(event)
    return event


def form_new_event_by_dancerGroup(dancerGroup_id):
    # A form to create a new event
    # param: dancerGroup_id (expected int) <-- indicates which dancerGroup to add the event to
    # returns: event (object of type Event)
    #name = input('Name the event: ')
    #abbrev = input('If you want to, give a 3 letter abbreviation: ')
    dancerGroup = scrudb.retrieve_dancerGroup(int(dancerGroup_id))
    dance = select_dance()  # this really should be a picker
    name = ('%s - %s' % (dancerGroup.name, dance.name))
    numPlaces = 't'
    while (numPlaces.isdigit() == False):
        numPlaces = input('How many places will be awarded? ')
    entry = input("Will this event earn a stamp for group %s? (Y/n)" %
                  dancerGroup.name)
    if ((entry == 'N') or (entry == 'n') or (entry == 'no') or (entry == 'No')):
        earnsStamp = 0
    else:
        earnsStamp = 1
    entry = input(
        "Will this event count toward the overall trophy for group %s? (Y/n)" % dancerGroup.name)
    if ((entry == 'N') or (entry == 'n') or (entry == 'no') or (entry == 'No')):
        countsForOverall = 0
    else:
        countsForOverall = 1
    #id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp
    event = Event(0, name, dancerGroup.id, dance.id, dancerGroup.competition,
                  countsForOverall, int(numPlaces), earnsStamp)
    event = scrudb.insert_event(event)
    return event


def menu_events(comp_id):
    # a menu to add/edit events
    loop = 1
    while (loop > 0):
        print("Choose an event:")
        events = scrudb.retrieve_events_by_competition(comp_id)
        events_list = [0, 0]
        for event in events:
            #event = Event(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            #id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp
            dance = scrudb.retrieve_dance(event.dance)
            print('( %2d ) %s' % (event.id, event.name))
            events_list.append(event.id)
        print('(  N ) New Event')
        print('(  X ) Exit')
        entry = input()
        if ((entry == 'N') or (entry == 'n')):
            form_new_event(comp_id)
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry.isdigit()):
            if ((int(entry) in events_list) and (int(entry) != 0)):
                menu_event(int(entry))
            else:
                print('Event not found.')
        else:
            print('Please choose an option.')


def menu_events_by_dancerGroup(dancerGroup_id):
    # a menu to add/edit events
    loop = 1
    while (loop > 0):
        print("Choose an event:")
        events = scrudb.retrieve_events_by_dancerGroup(dancerGroup_id)
        events_list = [0, 0]
        for event in events:
            #event = Event(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            #id, name, dancerGroup, dance, competition,countsForOverall, numplaces, earnsStamp
            #dance = scrudb.retrieve_dance(event.dance)
            print('( %2d ) %s' % (event.id, event.name))
            events_list.append(event.id)
        print('(  N ) New Event')
        print('(  X ) Exit')
        entry = input()
        if ((entry == 'N') or (entry == 'n')):
            event = form_new_event_by_dancerGroup(dancerGroup_id)
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry.isdigit()):
            if ((int(entry) in events_list) and (int(entry) != 0)):
                event = menu_event(int(entry))
            else:
                print('Event not found.')
        else:
            print('Please choose an option.')


def menu_event(id):
    # a menu to allow user to edit/delete an event
    # param: id (expected int, but other numerical representation that can be converted with int() is okay)
    loop = 1
    while (loop > 0):
        event = scrudb.retrieve_event(int(id))
        dance = scrudb.retrieve_dance(int(event.dance))
        print('Event: %s | %s' % (event.name, dance.name))
        print("What do you want to do?")
        print("( 1 ) Edit event details")
        print("( D ) Delete event")
        print("( X ) Exit")
        entry = input()
        if ((entry == 'D') or (entry == 'd')):
            new_verify = verify()
            if (new_verify == 1):
                print("Removing event")
                scrudb.rm_event(int(id))
                loop = 0
            else:
                print("Okay, action canceled.")
        elif ((entry == 'X') or (entry == 'x')):
            loop = 0
        elif (entry == '1'):
            event = form_edit_event(event)


def select_dance():
    # a menu to choose which dance
    # return: (object of type Dance)
    loop = 1
    while (loop > 0):
        print("Choose a dance:")
        dances = scrudb.retrieve_dances()
        dances_list = [0, 0]
        for row in dances:
            dance = Dance(row[0], row[1])
            #id, name = row
            print('( %2d ) %s' % (dance.id, dance.name))
            dances_list.append(dance.id)
        entry = input()
        if (entry.isdigit()):
            if ((int(entry) in dances_list) and (int(entry) != 0)):
                return scrudb.retrieve_dance(int(entry))
            else:
                print('Dance not found.')
        else:
            print('Please choose an option.')


def select_csv_file():
    # a menu to find the CSV file
    # return: csv_filename
    path = '.'
    loop = 1
    print('Choose a file: ')
    while (loop > 0):
        #print ('(  0) .')
        entries = os.scandir(path)
        files = ['..']
        print('(  0) [..]')
        x = 1
        for entry in entries:
            if (os.path.isdir(entry)):
                print('(%3d) [%s]' % (x, entry.name))
                files.append(entry.name)
                x += 1
            elif (entry.name.endswith('.csv')):
                print('(%3d) %s' % (x, entry.name))
                files.append(entry.name)
                x += 1
        # print(files)
        number = input('Choose a number: ')
        if (number.isdigit()):
            num = int(number)
            if (num <= len(files)):  # and (num > 0)):
                if (os.path.isdir(files[num])):
                    os.chdir(files[num])
                    #path = files[num]
                elif(files[num].endswith('.csv')):
                    return files[num]
            else:
                print('Choose a file: ')


def select_competitionType():
    # a menu to choose type of competition
    # return: (object of type CompetitionType)
    loop = 1
    while (loop > 0):
        print("Choose type of competition:")
        compTypes = scrudb.retrieve_competitionTypes()
        compTypes_list = [0, 0]
        for compType in compTypes:
            #compType = CompetitionType(row[0],row[1],row[2],row[3],row[4])
            #id, name, abbrev, isChampionship, protected = row
            print('( %2d ) %s' % (compType.id, compType.name))
            compTypes_list.append(compType.id)
        entry = input()
        if (entry.isdigit()):
            if ((int(entry) in compTypes_list) and (int(entry) != 0)):
                return scrudb.retrieve_competitionType(int(entry))
            else:
                print('Competition Type not found.')
        else:
            print('Please choose an option.')


def form_new_competition():
    # a form to create a new competition
    # returns: comp (object of type Competition)
    name = ''
    while (name == ''):
        name = input('Name the competition: ')
    desc = input('Description: ')
    eventDate_date_obj = select_date('Date', 0)
    deadline_date_obj = select_date('Deadline', 1)
    location = input('Location: ')
    compType = select_competitionType()
    comp = Competition(0, name, desc, eventDate_date_obj, deadline_date_obj,
                       location, compType.id, compType.isChampionship)
    comp = scrudb.insert_competition(comp)
    if (compType.isChampionship == 1):
        judge_count = 0
        while (judge_count < 3):
            print(
                'Competitions of type %s require at least 3 judges. Please add 3 judges.' % compType.name)
            new_judge = select_judge(comp.id)
            judges = scrudb.retrieve_judges_by_competition(comp.id)
            judge_count = 0
            for row in judges:
                judge_count += 1
    return comp


def form_edit_competition(comp):
    # a form to change the details of a competition
    # param: id (expected int, but other numerical representation that can be converted with int() is okay)
    # returns: comp (object of type Competition)
    #comp = scrudb.retrieve_competition(int(id))
    print('Current name: %s' % comp.name)
    name = input('New name: ')
    if (name != ''):
        comp.name = name
    print('Current description: %s' % comp.description)
    description = input('New description: ')
    if (description != ''):
        comp.description = description
    format_str = '%m/%d/%y'
    #print('Current event date %s' % comp.eventDate)
    otherformat_str = '%Y-%m-%d %H:%M:%S'
    print('Current event date: %s' % datetime.datetime.strftime(
        datetime.datetime.strptime(('%s' % comp.eventDate), otherformat_str).date(), format_str))
    #print('Current event date: %s' % datetime.datetime.strftime(comp.eventDate, format_str))
    date = select_date('New date', 1)
    if (date != ''):
        comp.date = date
    if (comp.deadline == ''):
        print('Current deadline:')
    else:
        print('Current deadline: %s' % datetime.datetime.strftime(datetime.datetime.strptime(
            ('%s' % comp.deadline), otherformat_str).date(), format_str))
    deadline = select_date('New deadline', 1)
    if (deadline != ''):
        comp.deadline = deadline
    print('Current location: %s' % comp.location)
    location = input('New location: ')
    if (location != ''):
        comp.location = location
    comp = scrudb.update_competition(comp)
    return comp


def print_categories():
    # displays the categories
    categories = scrudb.retrieve_categories()
    print('\nCategories:')
    for category in categories:
        #id, name, abbrev = row
        print('%2d %-25s (%s)' % (category.id, category.name, category.abbrev))


def print_settings():
    # displays the current settings
    settings = scrudb.retrieve_settings('current')
    settings = scrudb.retrieve_settings('current')
    if (settings.interface > 0):
        settings.interface = 0
        scrudb.set_settings(settings)
    print('Settings details - Version: %f - Schema: %f - Interface: %d - Last Competition: %d' %
          (settings.version, settings.schema, settings.interface, settings.lastComp))


def select_date(prompt, allowBlank):
    # asks for a date using supplied prompt, validates input
    #param: prompt (string)
    #returns: date
    dateObj = ''  # None
    dateloop = 0
    format_str = '%m/%d/%y'  # The format
    while dateloop < 1:
        dateEntry = input('%s (MM/DD/YY): ' % prompt)
        try:
            dateObj = datetime.datetime.strptime(
                dateEntry, format_str)  # .date()
            #dateloop += 1
            return dateObj
        except:  # ValueError:
            if ((dateEntry == '') and (allowBlank == 1)):
                return dateEntry
            else:
                print('Invalid date format.')
    # return dateObj
