from flask import session
from datetime import datetime, timedelta
import time
import random
import math


def setUserSession(user):
    session['id'] = user.id
    session['username'] = user.username
    session['name'] = user.name
    session['surname'] = user.surname
    session['isadmin'] = user.isadmin
    session['mockpassword'] = user.mockpassword


def deleteSession():
    session['id'] = None
    session['username'] = None
    session['name'] = None
    session['surname'] = None
    session['isadmin'] = None
    session['mockpassword'] = None


def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


def turkishTimeNow():
    utc = datetime.utcnow()
    return utc2local(utc)


def numberDateTimeNowUtc():
    current_milli_time = int(round(time.time() * 1000))
    return current_milli_time


def pythonDateTime(htmldatetime):
    pydatetime = datetime.strptime(htmldatetime, '%Y-%m-%dT%H:%M')
    '''date_processing = htmldatetime.replace('T', '-').replace(':', '-').split('-')
    date_processing = [int(v) for v in date_processing]
    pydatetime = datetime(*date_processing)'''
    return pydatetime


def htmldateTime(pythondatetime):
    htmldatetime = pythondatetime.strftime('%Y-%m-%dT%H:%M')
    return htmldatetime


def randomDate(start, end):
    """
    Return a random datetime between given datetimes

    :param start: The start datetime
    :type start: datetime
    :param end: The end datetime
    :type end: datetime
    :return: The random datetime between start and end
    :rtype: datetime
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random.seed(time.perf_counter_ns())
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def time_me(*arg):
    if len(arg) != 0:
        elapsedTime = time.time() - arg[0]
        # print(elapsedTime);
        hours = math.floor(elapsedTime / (60*60))
        elapsedTime = elapsedTime - hours * (60*60)
        minutes = math.floor(elapsedTime / 60)
        elapsedTime = elapsedTime - minutes * (60)
        seconds = math.floor(elapsedTime)
        elapsedTime = elapsedTime - seconds
        ms = elapsedTime * 1000
        if(hours != 0):
            print("%d hours %d minutes %d seconds" % (hours, minutes, seconds))
        elif(minutes != 0):
            print("%d minutes %d seconds" % (minutes, seconds))
        else:
            print("%d seconds %f ms" % (seconds, ms))
    else:
        # print ('does not exist. here you go.');
        return time.time()
