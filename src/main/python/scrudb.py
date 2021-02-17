#""" Scrutini Database Functions """
import sqlite3
import os
from scruclasses import *
import csv

db_filename = 'scrutini.db'
schema_filename = 'scrutinischema.sql'
app_version = 0.01
schema_version = 0.01
dbconn = None


def retrieve_settings(whichSettings):
    # retrieve settings from DB
    # param: whichSettings <-- Expects 'current' atm, hoping to apply 'last' for undo
    #returns: Settings (name, version, schema, interface, lastComp)
    conn = return_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name, version, schema, interface, lastComp, orderPlaces FROM settings WHERE name = \"%s\"' % whichSettings)
    row = cursor.fetchone()
    settings = Settings(row[0], row[1], row[2], row[3], row[4], row[5])
    #settings = Settings(row)
    return settings


def close_connection():
    conn = return_connection()
    conn.close()


def return_connection():
    global dbconn
    # return a link to the active connection to the DB. if none, open one
    if dbconn != None:
        return dbconn
    else:
        print("Connecting to DB...")
        dbconn = create_connection(db_filename)
        return dbconn


def retrieve_competitionTypes():
    conn = return_connection()
    cursor = conn.cursor()
    cursor.execute(
        'select id, name, abbrev, isChampionship, protected from competitionTypes')
    competitionTypes = cursor.fetchall()
    competitionTypes_collection = []
    if (competitionTypes != None):
        for row in competitionTypes:
            compType = CompetitionType(row[0], row[1], row[2], row[3], row[4])
            competitionTypes_collection.append(compType)
        return competitionTypes_collection
    else:
        return None


def retrieve_competitionType(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, abbrev, isChampionship, protected from competitionTypes where id = %d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    compType = CompetitionType(row[0], row[1], row[2], row[3], row[4])
    return compType


def retrieve_categories():
    conn = return_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select id, name, abbrev from dancerCats
        """)
    categories = cursor.fetchall()
    dancerCat_collection = []
    if (categories != None):
        for row in categories:
            category = DancerCat(row[0], row[1], row[2])
            dancerCat_collection.append(category)
        return dancerCat_collection
    else:
        return None


def update_competition(comp):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('update competitions set name = \"%s\", description = \"%s\", eventDate = \"%s\", deadline = \"%s\", location = \"%s\", competitionType = %d, isChampionship = %d where id =%d' % (
        comp.name, comp.description, comp.eventDate, comp.deadline, comp.location, comp.competitionType, comp.isChampionship, comp.id))
    cursor.execute(sql)
    conn.commit()
    return comp


def insert_competition(comp):
    conn = return_connection()
    cursor = conn.cursor()
    #print('Inserting: %s - %s -- %s, %s -- %s' % (comp.name, comp.description, comp.eventDate, comp.deadline, comp.location))
    sql = 'insert into competitions default values'
    cursor.execute(sql)
    comp.id = cursor.lastrowid
    comp = update_competition(comp)
    return comp


def rm_competition(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from competitions where id = %d' % int(id))
    cursor.execute(sql)
    rm_judges_by_competition(id)
    rm_dancerGroups_by_competition(id)
    rm_dancers_by_competition(id)
    rm_events_by_competition(id)
    conn.commit()


def retrieve_competitions():
    conn = return_connection()
    cursor = conn.cursor()
    cursor.execute(
        'select id, name, description, eventDate, deadline, location, competitionType, isChampionship from competitions')
    competitions_collection = []
    competitions = cursor.fetchall()
    if (competitions != None):
        for row in competitions:
            comp = Competition(row[0], row[1], row[2],
                               row[3], row[4], row[5], row[6], row[7])
            competitions_collection.append(comp)
        return competitions_collection
    else:
        return None


def retrieve_competition(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, description, eventDate, deadline, location, competitionType, isChampionship from competitions where id = %d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    comp = Competition(row[0], row[1], row[2], row[3],
                       row[4], row[5], row[6], row[7])
    return comp


def update_judge(judge):
    conn = return_connection()
    cursor = conn.cursor()
    #print('Update Judge %s %s %d' % (judge.firstName, judge.lastName, judge.id))
    sql2 = ('update judges set firstName = \"%s\", lastName = \"%s\", competition = %d where id =%d' % (
        judge.firstName, judge.lastName, judge.competition, judge.id))
    cursor.execute(sql2)
    conn.commit()
    return judge


def insert_judge(judge):
    # Add a new Judge object to the DB
    conn = return_connection()
    cursor = conn.cursor()
    #print('Inserting: %s %s' % (judge.firstName, judge.lastName))
    sql = 'insert into judges default values'
    cursor.execute(sql)
    judge.id = cursor.lastrowid
    judge = update_judge(judge)
    return judge


def rm_judge(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from judges where id = %d' % int(id))
    cursor.execute(sql)
    conn.commit()


def rm_judges_by_competition(comp_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from judges where competition = %d' % int(comp_id))
    cursor.execute(sql)
    conn.commit()


def retrieve_judges_by_competition(comp_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, firstName, lastName, competition from judges where competition = %d' % int(comp_id))
    cursor.execute(sql)
    judges = cursor.fetchall()
    judges_collection = []
    if (judges != None):
        for row in judges:
            judge = Judge(row[0], row[1], row[2], row[3])
            judges_collection.append(judge)
            #print('Found judge',row[0],row[1],row[2],'in competition',row[3])
        return judges_collection
    else:
        return None


def retrieve_judge(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, firstName, lastName, competition from judges where id = %d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    judge = Judge(row[0], row[1], row[2], row[3])
    return judge


def update_dancerGroup(dancerGroup):
    conn = return_connection()
    cursor = conn.cursor()
    sql2 = ('update dancerGroups set name = \"%s\", abbrev = \"%s\", ageMin = %d, ageMax = %d, dancerCat = %d, competition = %d where id =%d' % (
        dancerGroup.name, dancerGroup.abbrev, dancerGroup.ageMin, dancerGroup.ageMax, dancerGroup.dancerCat, dancerGroup.competition, dancerGroup.id))
    cursor.execute(sql2)
    conn.commit()
    return dancerGroup


def insert_dancerGroup(dancerGroup):
    # Add a new DancerGroup object to the DB
    conn = return_connection()
    cursor = conn.cursor()
    sql = 'insert into dancerGroups default values'
    cursor.execute(sql)
    dancerGroup.id = cursor.lastrowid
    dancerGroup = update_dancerGroup(dancerGroup)
    return dancerGroup


def rm_dancerGroupJoin_by_dancer_and_dancerGroup(dancer_id, dancerGroup_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from dancerGroupJoin where (dancer = %d and dancerGroup = %d)' % (
        int(dancer_id), int(dancerGroup_id)))
    cursor.execute(sql)
    conn.commit()


def rm_dancerGroupJoin_by_dancer(dancer_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from dancerGroupJoin where dancer = %d' % int(dancer_id))
    cursor.execute(sql)
    conn.commit()


def rm_dancerGroupJoin_by_dancerGroup(dancerGroup_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from dancerGroupJoin where dancerGroup = %d' %
           int(dancerGroup_id))
    cursor.execute(sql)
    conn.commit()


def rm_dancerGroup(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from dancerGroups where id = %d' % int(id))
    cursor.execute(sql)
    rm_dancerGroupJoin_by_dancerGroup(id)
    conn.commit()


def rm_dancerGroups_by_competition(comp_id):
    dancerGroups = retrieve_dancerGroups_by_competition(comp_id)
    for dancerGroup in dancerGroups:
        rm_dancerGroup(dancerGroup.id)


def retrieve_dancerGroups_by_competition(comp_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, abbrev, ageMin, ageMax, dancerCat, competition from dancerGroups where competition = %d' % int(comp_id))
    cursor.execute(sql)
    dancerGroups = cursor.fetchall()
    dancerGroups_collection = []
    if (dancerGroups != None):
        for row in dancerGroups:
            dancerGroup = DancerGroup(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            dancerGroups_collection.append(dancerGroup)
        return dancerGroups_collection
    else:
        return None


def retrieve_dancerGroup(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, abbrev, ageMin, ageMax, dancerCat, competition from dancerGroups where id = %d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    if (row != None):
        dancerGroup = DancerGroup(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    else:
        dancerGroup = None
    return dancerGroup


def retrieve_dancerGroup_by_abbrev(abbrev):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, abbrev, ageMin, ageMax, dancerCat, competition from dancerGroups where abbrev = \"%s\"' % abbrev)
    cursor.execute(sql)
    row = cursor.fetchone()
    dancerGroup = None
    if(row != None):
        dancerGroup = DancerGroup(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    return dancerGroup


def retrieve_dancerGroups_by_dancer(dancer_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select dancer, dancerGroup from dancerGroupJoin where dancer = %d' % dancer_id)
    cursor.execute(sql)
    dancerGroups = cursor.fetchall()
    dancerGroups_collection = []
    if (dancerGroups != None):
        #print('retrieve_dancerGroups_by_dancer: if (dancerGroups != None): %s' % dancerGroups)
        if (len(dancerGroups) > 0):
            for row in dancerGroups:
                if (row != None):
                    dancerGroup = retrieve_dancerGroup(row[1])
                    dancerGroups_collection.append(dancerGroup)
        return dancerGroups_collection
    else:
        #print('retrieve_dancerGroups_by_dancer: else')
        return None


def create_connection(db_file):
    # create a database connection to the SQLite database specified by db_file
    # param db_file: database filename
    # return: Connection object or None
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_schema():
    # Loads the schema from scratch
    conn = return_connection()
    print('Creating schema')
    with open(schema_filename, 'rt') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()


def new_settings(settings):
    # Set a new settings set
    # param: settings (type Settings)
    conn = return_connection()
    sql = ('INSERT INTO settings(name, version, schema, interface, lastComp, orderPlaces) VALUES(\"%s\",%f,%f,%d,%d,%d)' % (
        settings.name, settings.version, settings.schema, settings.interface, settings.lastComp, settings.orderOfPlacings))
    #sql = ('update settings set name = \"%s\", version = %f, schema = %f, interface = %d, lastComp = %d where name = \"%s\"' % (settings.name, settings.version, settings.schema, settings.interface, settings.lastComp, settings.name))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def set_settings(settings):
    # Set the settings
    # param: settings (type Settings)
    conn = return_connection()
    #sql = ('INSERT INTO settings(name, version, schema, interface, lastComp) VALUES(\"%s\",%f,%f,%d,%d)' % (settings.name, settings.version, settings.schema, settings.interface, settings.lastComp))
    sql = ('update settings set name = \"%s\", version = %f, schema = %f, interface = %d, lastComp = %d, orderPlaces=%d where name = \"%s\"' % (
        settings.name, settings.version, settings.schema, settings.interface, settings.lastComp, settings.orderOfPlacings, settings.name))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def update_dancer(dancer):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('update dancers set firstName = \"%s\", lastName = \"%s\", scotDanceNum = \"%s\", street  = \"%s\", city = \"%s\", state = \"%s\", zip = \"%s\", birthdate = \"%s\", age = %d, registeredDate = \"%s\", number = \"%s\", phonenum = \"%s\", email = \"%s\", teacher = \"%s\", teacherEmail = \"%s\", dancerCat = %d, dancerGroup = %d, competition = %d where id = %d' % (
        dancer.firstName, dancer.lastName, dancer.scotDanceNum, dancer.street, dancer.city, dancer.state, dancer.zipCode, dancer.birthdate, dancer.age, dancer.registeredDate, dancer.number, dancer.phonenum, dancer.email, dancer.teacher, dancer.teacherEmail, dancer.dancerCat, dancer.dancerGroup, dancer.competition, dancer.id))
    cursor.execute(sql)
    conn.commit()
    return dancer


def insert_dancer(dancer):
    conn = return_connection()
    sql = ('insert into dancers default values')
    cur = conn.cursor()
    cur.execute(sql)
    dancer.id = cur.lastrowid
    dancer = update_dancer(dancer)
    return dancer


def find_dancer_number(dancer):
    return dancer.number


def retrieve_dancers_by_dancerGroup_ordered_by_number(dancerGroup_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select dancer, dancerGroup from dancerGroupJoin where dancerGroup = %d' %
           dancerGroup_id)
    cursor.execute(sql)
    dancers = cursor.fetchall()
    dancers_collection = []
    dancers = list(filter(None, dancers))
    for row in dancers:
        dancer = retrieve_dancer(row[0])
        # print(row)
        # if dancer != None:
        #    print('%d - %s' % (dancer.id, dancer.number))
        # print(retrieve_dancer(row[0]))
        dancers_collection.append(dancer)
    dancers_collection = list(filter(None, dancers_collection))
    if (dancers_collection != None):
        try:
            dancers_collection.sort(key=find_dancer_number)
        except:
            return None
    return dancers_collection


def retrieve_dancers_by_dancerGroup(dancerGroup_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select dancer, dancerGroup from dancerGroupJoin where dancerGroup = %d' %
           dancerGroup_id)
    cursor.execute(sql)
    dancers = cursor.fetchall()
    dancers_collection = []
    dancers = list(filter(None, dancers))
    for row in dancers:
        if (row != None):
            dancer = retrieve_dancer(row[0])
            dancers_collection.append(dancer)
    dancers_collection = list(filter(None, dancers_collection))
    return dancers_collection


def retrieve_dancers_by_competition(comp_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, firstName, lastName, scotDanceNum, street, city, state, zip, birthdate, age, registeredDate, number, phonenum, email, teacher, teacherEmail, dancerCat, dancerGroup, competition from dancers where competition = %d' % comp_id)
    cursor.execute(sql)
    dancers = cursor.fetchall()
    dancers_collection = []
    for row in dancers:
        dancer = Dancer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                        row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18])
        dancers_collection.append(dancer)
    dancers_collection = list(filter(None, dancers_collection))
    return dancers_collection


def retrieve_dancer(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, firstName, lastName, scotDanceNum, street, city, state, zip, birthdate, age, registeredDate, number, phonenum, email, teacher, teacherEmail, dancerCat, dancerGroup, competition from dancers where id = %d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    if (row != None):
        dancer = Dancer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                        row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18])
        return dancer
    else:
        return None


def rm_dancers_by_competition(comp_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from dancers where competition = %d' % comp_id)
    cursor.execute(sql)
    conn.commit()


def rm_dancer(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from dancers where id = %d' % int(id))
    cursor.execute(sql)
    rm_dancerGroupJoin_by_dancer(id)
    conn.commit()


def insert_dancerGroupJoin(dancer_id, dancerGroup_id):
    conn = return_connection()
    cursor = conn.cursor()
    check = retrieve_dancerGroups_by_dancer(dancer_id)
    if (check != None):
        for dancerGroup in check:
            if (dancerGroup.id == dancerGroup_id):
                #print('Competitor is already in group %s' % dancerGroup.name)
                return
    sql = ('insert into dancerGroupJoin (dancer, dancerGroup) values(%d,%d)' %
           (dancer_id, dancerGroup_id))
    cursor.execute(sql)
    conn.commit()


def update_dance(dance):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('update dances set name = \"%s\" where id = %d' %
           (dance.name, dance.id))
    cursor.execute(sql)
    conn.commit()
    return dance


def insert_dance(dance):
    conn = return_connection()
    sql = ('insert into dances default values')
    cur = conn.cursor()
    cur.execute(sql)
    dance.id = cur.lastrowid
    dance = update_dance(dance)
    return dance


def retrieve_dances():
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name from dances')
    cursor.execute(sql)
    return cursor.fetchall()


def retrieve_dance(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name from dances where id = %d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    dance = Dance(row[0], row[1])
    return dance


def retrieve_score(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, dancer, event, judge, competition, score from scores where id = %d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    score = Score(row[0], row[1], row[2], row[3], row[4], row[5])
    return score

def retrieve_score_by_event_and_dancer(event_id, dancer_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, dancer, event, judge, competition, score from scores where event = %d and dancer = %d' % (int(event_id), int(dancer_id)))
    cursor.execute(sql)
    row = cursor.fetchone()
    if row != None:
        score = Score(row[0], row[1], row[2], row[3], row[4], row[5])
        return score
    else:
        return None


def exists_scores_for_event(event_id):
    scores = retrieve_scores_by_event(event_id)
    if ((scores == []) or (scores == None)):
        return False
    else:
        return True


def update_score(score):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('update scores set dancer = %d, event = %d, judge = %d, competition = %d, score = %f where id = %d' % (
        score.dancer, score.event, score.judge, score.competition, score.score, score.id))
    cursor.execute(sql)
    conn.commit()
    return score


def insert_score(score):
    conn = return_connection()
    sql = ('insert into scores default values')
    cur = conn.cursor()
    cur.execute(sql)
    score.id = cur.lastrowid
    score = update_score(score)
    return score


def retrieve_scores_by_event(event_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, dancer, event, judge, competition, score from scores where event = %d' % event_id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    scores = []
    for row in rows:
        scores.append(Score(row[0], row[1], row[2], row[3], row[4], row[5]))
    return scores


def rm_scores_by_event(event_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from scores where event = %d' % event_id)
    cursor.execute(sql)
    conn.commit()

def rm_scores_by_event_and_judge(event_id, judge_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from scores where event = %d and judge = %d' % (event_id, judge_id))
    cursor.execute(sql)
    conn.commit()


def retrieve_events_by_competition(comp_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp from events where competition=%d' % int(comp_id))
    cursor.execute(sql)
    events = cursor.fetchall()
    events_collection = []
    for row in events:
        event = Event(row[0], row[1], row[2], row[3],
                      row[4], row[5], row[6], row[7])
        events_collection.append(event)
    events_collection = list(filter(None, events_collection))
    return events_collection


def retrieve_events_by_dancerGroup(dancerGroup_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp from events where dancerGroup=%d' % int(dancerGroup_id))
    cursor.execute(sql)
    events = cursor.fetchall()
    events_collection = []
    for row in events:
        event = Event(row[0], row[1], row[2], row[3],
                      row[4], row[5], row[6], row[7])
        events_collection.append(event)
    events_collection = list(filter(None, events_collection))
    return events_collection


def retrieve_event(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp from events where id=%d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    event = Event(row[0], row[1], row[2], row[3],
                  row[4], row[5], row[6], row[7])
    return event


def rm_event(event_id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('delete from events where id = %d' % event_id)
    cursor.execute(sql)
    rm_scores_by_event(event_id)
    conn.commit()


def rm_events_by_competition(comp_id):
    events = retrieve_events_by_competition(comp_id)
    for event in events:
        rm_event(event.id)


def update_event(event):
    conn = return_connection()
    cursor = conn.cursor()
    #id, name, dancerGroup, dance, competition, countsForOverall, numPlaces, earnsStamp
    sql = ('update events set name = \"%s\", dancerGroup = %d, dance = %d, competition=%d, countsForOverall=%d,numPlaces=%d, earnsStamp=%d where id = %d' % (
        event.name, event.dancerGroup, event.dance, event.competition, event.countsForOverall, event.numPlaces, event.earnsStamp, event.id))
    cursor.execute(sql)
    conn.commit()
    return event


def insert_event(event):
    conn = return_connection()
    sql = ('insert into events default values')
    cur = conn.cursor()
    cur.execute(sql)
    event.id = cur.lastrowid
    event = update_event(event)
    return event


def update_competitionType(competitionType):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('update competitionTypes set name = \"%s\", abbrev = \"%s\", isChampionship = %d, protected = %d where id = %d' % (
        competitionType.name, competitionType.abbrev, competitionType.isChampionship, competitionType.isProtected, competitionType.id))
    cursor.execute(sql)
    conn.commit()
    return competitionType


def insert_competitionType(competitionType):
    conn = return_connection()
    sql = ('insert into competitionTypes default values')
    cur = conn.cursor()
    cur.execute(sql)
    competitionType.id = cur.lastrowid
    competitionType = update_competitionType(competitionType)
    return competitionType


def update_dancerCat(dancerCat):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('update dancerCats set name = \"%s\", abbrev = \"%s\", protected = %d where id =%d' % (
        dancerCat.name, dancerCat.abbrev, dancerCat.protected, dancerCat.id))
    cursor.execute(sql)
    conn.commit()
    return dancerCat


def insert_dancerCat(dancerCat):
    # add a new dancerCat object into the DB
    conn = return_connection()
    sql = 'INSERT INTO dancerCats default values'
    cur = conn.cursor()
    cur.execute(sql)
    dancerCat.id = cur.lastrowid
    dancerCat = update_dancerCat(dancerCat)
    return dancerCat

def rm_dancerCat(dancerCat_id):
    # add a new dancerCat object into the DB
    conn = return_connection()
    sql = ('delete from dancerCats where id = %d' % dancerCat_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def retrieve_dancerCats():
    conn = return_connection()
    cursor = conn.cursor()
    sql = 'select id, name, abbrev, protected from dancerCats'
    cursor.execute(sql)
    dancerCats = cursor.fetchall()
    dancerCats_collection = []
    for row in dancerCats:
        dancerCat = DancerCat(row[0], row[1], row[2], row[3])
        dancerCats_collection.append(dancerCat)
    dancerCats_collection = list(filter(None, dancerCats_collection))
    return dancerCats_collection


def retrieve_dancerCat(id):
    conn = return_connection()
    cursor = conn.cursor()
    sql = ('select id, name, abbrev, protected from dancerCats where id=%d' % int(id))
    cursor.execute(sql)
    row = cursor.fetchone()
    if (row != None):
        dancerCat = DancerCat(row[0], row[1], row[2], row[3])
        return dancerCat
    else:
        return None


def insert_initial_data():
    # preload the DB with some necessary data
    conn = return_connection()

    print('Inserting initial data')
    catBlank = DancerCat(0, '', '', 1)
    catPrimary = DancerCat(0, 'Primary', 'P', 1)
    catBeginner = DancerCat(0, 'Beginner', 'B', 1)
    catNovice = DancerCat(0, 'Novice', 'N', 1)
    catIntermediate = DancerCat(0, 'Intermediate', 'I', 1)
    catPremier = DancerCat(0, 'Premier', 'X', 1)
    catChoreo = DancerCat(0, 'Choreography', 'C', 1)
    catSpecial = DancerCat(0, 'Special Award', 'S', 1)

    dancerCat = insert_dancerCat(catBlank)
    dancerCat = insert_dancerCat(catPrimary)
    dancerCat = insert_dancerCat(catBeginner)
    dancerCat = insert_dancerCat(catNovice)
    dancerCat = insert_dancerCat(catIntermediate)
    dancerCat = insert_dancerCat(catPremier)
    dancerCat = insert_dancerCat(catChoreo)
    dancerCat = insert_dancerCat(catSpecial)

    compType_regular = CompetitionType(0, 'Regular', 'Reg', 0, 1)
    compType_championship = CompetitionType(0, 'Championship', 'Champ', 1, 1)
    compType_premiership = CompetitionType(0, 'Premiership', 'Prem', 1, 1)

    compType = insert_competitionType(compType_regular)
    compType = insert_competitionType(compType_championship)
    compType = insert_competitionType(compType_premiership)

    defaultValues = Settings('current', app_version, schema_version, 0, 0, 1)
    new_settings(defaultValues)

    placeValues = []
    placeValues.append(PlaceValue(1,137))
    placeValues.append(PlaceValue(2,91))
    placeValues.append(PlaceValue(3,71))
    placeValues.append(PlaceValue(4,53))
    placeValues.append(PlaceValue(5,37))
    placeValues.append(PlaceValue(6,23))
    for placeValue in placeValues:
        insert_placeValue(placeValue)

    judge = Judge(0,'','',9999999999)
    insert_judge(judge)

    print('Loading dances...')
    dances = ['Dance/Award','Highland Fling', 'Sword Dance', 'Sean Triubhas', 'Reel',
                'Flora', 'Scottish Lilt', 'Jig', 'Sailor\'s Hornpipe',
                'Highland Laddie', 'Village Maid', 'Blue Bonnets', 'Earl of Erroll',
                'Scotch Measure', 'Barracks Johnnie', 'Pas de Basques',
                'Pas de Basques and High Cuts', 'Scholarship', 'Most Promising',
                'Special Award', 'Dancer of the Day', 'Choreography', 'Special/Trophy Fling',
                'Broadswords', 'Cake Walk', 'Reel Team']

    for i in dances:
        dance = Dance(0, i)
        # print(i)
        insert_dance(dance)

    conn.commit()

def retrieve_placeValue(place):
    conn = return_connection()
    sql = ('select place, points from placeValues where place=%d' % int(place))
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    if (row != None):
        placeValue = PlaceValue(row[0],row[1])
        return placeValue
    else:
        return None

def retrieve_placeValues():
    conn = return_connection()
    cursor = conn.cursor()
    sql = 'select place, points from placeValues'
    cursor.execute(sql)
    placeValues = cursor.fetchall()
    placeValues_collection = []
    for row in placeValues:
        placeValue = PlaceValue(row[0], row[1])
        placeValues_collection.append(placeValue)
    placeValues_collection = list(filter(None, placeValues_collection))
    return placeValues_collection

def insert_placeValue(placeValue):
    conn = return_connection()
    sql = ('insert into placeValues (place, points) values(%d,%d)' % (placeValue.place, placeValue.points))
    cur = conn.cursor()
    cur.execute(sql)
    return placeValue

def insert_placeValues_table():
    conn = return_connection()
    sql = ('create table if not exists placeValues (place integer primary key not null, points integer);')
    cur = conn.cursor()
    cur.execute(sql)

def retrieve_csv_dict(csv_filename):
    if os.path.exists(csv_filename):
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # for row in reader:
            #    print(row)
            return reader
    else:
        print('File not found.')
        return None


def retrieve_csv_keys(csv_filename):
    if os.path.exists(csv_filename):
        with open(csv_filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            # for row in reader:
            #    print(row)
            return next(reader)
    else:
        print('File not found.')
        return None


def check_db():
    # Check whether the DB is new, and create schema and load defaults if it is
    db_is_new = not os.path.exists(db_filename)

    if db_is_new:
        print('Need to create schema')
        create_schema()
        insert_initial_data()
    else:
        print('Database exists; check version')
        settings = retrieve_settings('current')
        if (settings.version == app_version):
            print("App Version %f is current version" % settings.version)
        elif (settings.version < app_version):
            print("Settings need updated to version %f" % app_version)
        else:
            print("App needs updated to version %f to use this data" %
                  settings.version)
        if (settings.schema == schema_version):
            print("Schema version %f is current version" % settings.schema)
        elif (settings.schema < schema_version):
            print("Schema version %f need updated to %f" %
                  (settings.schema, schema_version))
        else:
            print("App needs updated to schema version %f to use this data" %
                  settings.schema)