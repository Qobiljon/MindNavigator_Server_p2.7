# coding=utf-8
import json
import random
import time
import unicodecsv as csv
import calendar as cal
import datetime as dt

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response as Res
from MindNavigator_Server.models import User, Event, Intervention, InterventionManager, Evaluation, Survey
from django.db.models import Q

# region Constants
RES_SUCCESS = 0
RES_FAILURE = 1
RES_BAD_REQUEST = -1


# endregion


def is_user_valid(username, password):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        return user.password == password
    return False


def time_add(_time, _add):
    res = dt.datetime(
        year=int(_time / 1000000),
        month=int(_time / 10000) % 100,
        day=int(_time / 100) % 100,
        hour=int(_time % 100)
    )
    if _add >= 0:
        res += dt.timedelta(hours=int(_add / 60))
    else:
        res -= dt.timedelta(hours=int(-_add / 60))
    return int("%02d%02d%02d%02d" % (res.year % 100, res.month, res.day, res.hour))


def overlaps(username, start_time, end_time, except_id=None):
    if except_id is None:
        if Event.objects.filter(owner__username=username, startTime__range=(start_time, end_time - 1)).exists():
            return True
        elif Event.objects.filter(owner__username=username, endTime__range=(start_time + 1, end_time)).exists():
            return True
        elif Event.objects.filter(owner__username=username, startTime__lte=start_time, endTime__gte=end_time).exists():
            return True
    else:
        if Event.objects.filter(~Q(eventId=except_id), owner__username=username, startTime__range=(start_time, end_time - 1)).exists():
            return True
        elif Event.objects.filter(~Q(eventId=except_id), owner__username=username, endTime__range=(start_time + 1, end_time)).exists():
            return True
        elif Event.objects.filter(~Q(eventId=except_id), owner__username=username, startTime__lte=start_time, endTime__gte=end_time).exists():
            return True


def weekday(millis):
    temp = dt.datetime.fromtimestamp(millis / 1000.0)
    return cal.weekday(year=temp.year, month=temp.month, day=temp.day)


def add_timedelta(millis, timedelta):
    res = dt.datetime.fromtimestamp(millis / 1000.0) + timedelta
    return int(round(time.mktime(res.timetuple()) * 1000))


def to_time(millis):
    return dt.datetime.fromtimestamp(millis / 1000).strftime('%Y/%m/%d %H:%M')


@api_view(['POST'])
def handle_register(request):
    json_body = json.loads(request.body.decode('utf-8'))

    if 'username' in json_body and 'password' in json_body and 'name' in json_body:
        username = json_body['username']
        password = json_body['password']
        name = json_body['name']

        if User.objects.filter(username=username).exists():
            return Res(data={'result': RES_FAILURE})
        else:
            User.objects.create_user(username=username, password=password, name=name).save()
            Survey.objects.create_survey(user=User.objects.get(username=username)).save()
            return Res(data={'result': RES_SUCCESS})
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'either of username, password, or name was not passed as a POST argument!'})


@api_view(['POST'])
def handle_login(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})


@api_view(['POST'])
def handle_event_create(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and 'eventId' in json_body and 'title' in json_body and 'stressLevel' in json_body and 'startTime' in json_body and 'endTime' in json_body and 'intervention' in json_body \
            and 'interventionReminder' in json_body and 'stressType' in json_body and 'stressCause' in json_body and 'repeatId' in json_body and 'repeatTill' in json_body and 'repeatMode' in json_body and 'eventReminder' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) and not Event.objects.filter(eventId=json_body['eventId']).exists():
            if json_body['repeatMode'] is Event.NO_REPEAT:
                if not overlaps(username=json_body['username'], start_time=json_body['startTime'], end_time=json_body['endTime']):
                    # create a single event
                    Event.objects.create_event(
                        event_id=json_body['eventId'],
                        owner=User.objects.get(username=json_body['username']),
                        title=json_body['title'],
                        stress_level=json_body['stressLevel'],
                        start_time=json_body['startTime'],
                        end_time=json_body['endTime'],
                        intervention=json_body['intervention'],
                        interv_reminder=json_body['interventionReminder'],
                        stress_type=json_body['stressType'],
                        stress_cause=json_body['stressCause'],
                        repeat_mode=json_body['repeatMode'],
                        repeat_id=json_body['repeatId'],
                        event_reminder=json_body['eventReminder']
                    ).save()
                    return Res(data={'result': RES_SUCCESS})
                else:
                    return Res(data={'result': RES_FAILURE})
            elif json_body['repeatMode'] is Event.REPEAT_EVERYDAY:
                event_id = json_body['eventId']
                start_time = json_body['startTime']
                end_time = json_body['endTime']

                if end_time - start_time > 86400000:
                    return Res(data={'result': RES_FAILURE, 'reason': 'event length is longer than a day'})

                while start_time < json_body['repeatTill']:
                    if not overlaps(username=json_body['username'], start_time=start_time, end_time=end_time):
                        Event.objects.create_event(
                            event_id=event_id,
                            owner=User.objects.get(username=json_body['username']),
                            title=json_body['title'],
                            stress_level=json_body['stressLevel'],
                            start_time=start_time,
                            end_time=end_time,
                            intervention=json_body['intervention'],
                            interv_reminder=json_body['interventionReminder'],
                            stress_type=json_body['stressType'],
                            stress_cause=json_body['stressCause'],
                            repeat_mode=json_body['repeatMode'],
                            repeat_id=json_body['repeatId'],
                            event_reminder=json_body['eventReminder'],
                            repeat_till=json_body['repeatTill']
                        ).save()
                    start_time += 86400000
                    end_time += 86400000
                    event_id += 1

                return Res(data={'result': RES_SUCCESS})
            elif json_body['repeatMode'] is Event.REPEAT_WEEKLY:
                # create multiple events
                start = [
                    json_body['startTime'] if json_body['mon'] else None,
                    json_body['startTime'] if json_body['tue'] else None,
                    json_body['startTime'] if json_body['wed'] else None,
                    json_body['startTime'] if json_body['thu'] else None,
                    json_body['startTime'] if json_body['fri'] else None,
                    json_body['startTime'] if json_body['sat'] else None,
                    json_body['startTime'] if json_body['sun'] else None
                ]
                end = [
                    json_body['endTime'] if json_body['mon'] else None,
                    json_body['endTime'] if json_body['tue'] else None,
                    json_body['endTime'] if json_body['wed'] else None,
                    json_body['endTime'] if json_body['thu'] else None,
                    json_body['endTime'] if json_body['fri'] else None,
                    json_body['endTime'] if json_body['sat'] else None,
                    json_body['endTime'] if json_body['sun'] else None
                ]

                if json_body['endTime'] - json_body['startTime'] > 604800000:
                    return Res(data={'result': RES_FAILURE, 'reason': 'event length is longer than a week'})

                event_id = json_body['eventId']
                for x in range(7):
                    if start[x] is None:
                        continue
                    day_delta = (7 - (weekday(start[x]) - x)) % 7
                    start[x] = add_timedelta(start[x], dt.timedelta(days=day_delta))
                    end[x] = add_timedelta(end[x], dt.timedelta(days=day_delta))

                    while start[x] < json_body['repeatTill']:
                        if not overlaps(username=json_body['username'], start_time=start[x], end_time=end[x]):
                            Event.objects.create_event(
                                event_id=event_id,
                                owner=User.objects.get(username=json_body['username']),
                                title=json_body['title'],
                                stress_level=json_body['stressLevel'],
                                start_time=start[x],
                                end_time=end[x],
                                intervention=json_body['intervention'],
                                interv_reminder=json_body['interventionReminder'],
                                stress_type=json_body['stressType'],
                                stress_cause=json_body['stressCause'],
                                repeat_mode=json_body['repeatMode'],
                                repeat_id=json_body['repeatId'],
                                event_reminder=json_body['eventReminder'],
                                repeat_till=json_body['repeatTill']
                            ).save()
                        start[x] += 604800000
                        end[x] += 604800000
                        event_id += 1

                return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Some arguments are missing in the POST request!'})


@api_view(['POST'])
def handle_event_edit(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and 'eventId' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) and Event.objects.filter(
                owner__username=json_body['username'], eventId=json_body['eventId']).exists():
            event = Event.objects.get(eventId=json_body['eventId'])
            if 'stressLevel' in json_body:
                event.stressLevel = json_body['stressLevel']
            if 'realStressLevel' in json_body:
                event.repeatId = json_body['realStressLevel']
            if 'title' in json_body:
                event.title = json_body['title']
            if 'startTime' in json_body and 'endTime' in json_body and not overlaps(
                    username=json_body['username'], start_time=json_body['startTime'],
                    end_time=json_body['endTime'], except_id=event.eventId):
                event.startTime = json_body['startTime']
                event.endTime = json_body['endTime']
            if 'intervention' in json_body:
                event.intervention = json_body['intervention']
            if 'interventionReminder' in json_body:
                event.interventionReminder = json_body['interventionReminder']
            if 'stressType' in json_body:
                event.stressType = json_body['stressType']
            if 'stressCause' in json_body:
                event.stressCause = json_body['stressCause']
            if 'repeatMode' in json_body:
                event.repeatMode = json_body['repeatMode']
            if 'eventReminder' in json_body:
                event.eventReminder = json_body['eventReminder']
            if 'repeatId' in json_body:
                event.repeatId = json_body['repeatId']
            event.save()
            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'Username, password, or eventId was not passed as a POST argument!'})


@api_view(['POST'])
def handle_event_delete(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and ('eventId' in json_body or 'repeatId' in json_body):
        if is_user_valid(json_body['username'], json_body['password']):
            if 'eventId' in json_body and Event.objects.filter(owner__username=json_body['username'], eventId=json_body['eventId']).exists():
                Event.objects.get(eventId=json_body['eventId']).delete()
                return Res(data={'result': RES_SUCCESS})
            elif 'repeatId' in json_body and Event.objects.filter(owner__username=json_body['username'], repeatId=json_body['repeatId']).exists():
                array = []
                for event in Event.objects.filter(owner__username=json_body['username'], repeatId=json_body['repeatId']):
                    array.append(event.eventId)
                    event.delete()
                return Res(data={'result': RES_SUCCESS, 'deletedIds': array})
        all_events = []
        for event in Event.objects.filter(owner__username=json_body['username']):
            all_events.append(event.__json__())
        return Res(data={'result': RES_FAILURE, 'repeatId': json_body['repeatId'], 'allEvents': all_events})
    else:
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'Username, password, or event_id was not passed as a POST argument!'})


@api_view(['POST'])
def handle_events_fetch(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'],
                                                                             json_body['password']):
        user = User.objects.get(username=json_body['username'])
        _from = json_body['period_from']
        _till = json_body['period_till']
        result = {}
        done_ids = []
        array = []

        for event in Event.objects.filter(owner=user, startTime__range=(_from, _till - 1)):
            array.append(event.__json__())
            done_ids.append(event.eventId)
        for event in Event.objects.filter(owner=user, endTime__range=(_from + 1, _till)):
            if event.eventId not in done_ids:
                array.append(event.__json__())
                done_ids.append(event.eventId)
        for event in Event.objects.filter(owner=user, startTime__lte=_from, endTime__gte=_till):
            if event.eventId not in done_ids:
                array.append(event.__json__())

        result['result'] = RES_SUCCESS
        result['array'] = array
        return Res(data=result)
    return Res(data={'result': RES_BAD_REQUEST})


@api_view(['POST'])
def handle_intervention_create(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and 'interventionName' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) and not Intervention.objects.filter(
                name=json_body['interventionName']).exists():
            if not Intervention.objects.filter(name=json_body['interventionName'], privateUsername=None).exists():
                Intervention.objects.create_intervention(name=json_body['interventionName'],
                                                         intervention_type=InterventionManager.PEER,
                                                         private_username=json_body['username']).save()
            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'Username, password, or event_id was not passed as a POST argument!'})


@api_view(['POST'])
def handle_system_intervention_fetch(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            array = []
            for intervention in Intervention.objects.filter(interventionType=InterventionManager.SYSTEM):
                array.append(intervention.name)
            random.shuffle(array)
            return Res(data={'result': RES_SUCCESS, 'names': array})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username or password was not passed as a POST argument!'})


@api_view(['POST'])
def handle_peer_intervention_fetch(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            array = []
            for intervention in Intervention.objects.filter(interventionType=InterventionManager.PEER,
                                                            privateUsername=None):
                array.append(intervention.name)
            random.shuffle(array)
            return Res(data={'result': RES_SUCCESS, 'names': array})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'Username, password, or event_id was not passed as a POST argument!'})


@api_view(['POST'])
def handle_evaluation_submit(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and 'eventId' in json_body and 'interventionName' in json_body \
            and 'startTime' in json_body and 'endTime' in json_body and 'realStressLevel' in json_body \
            and 'realStressCause' in json_body and 'journal' in json_body and 'eventDone' in json_body \
            and 'interventionDone' in json_body and 'sharedIntervention' in json_body \
            and 'intervEffectiveness' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) \
                and Event.objects.filter(eventId=json_body['eventId'], owner__username=json_body['username']).exists():
            if Evaluation.objects.filter(event__owner__username=json_body['username'],
                                         event__eventId=json_body['eventId']).exists():
                Evaluation.objects.get(event__owner__username=json_body['username'],
                                       event__eventId=json_body['eventId']).delete()
            event = Event.objects.get(eventId=json_body['eventId'])
            event.realStressLevel = json_body['realStressLevel']
            event.save()

            Evaluation.objects.create_evaluation(
                event=event,
                intervention_name=json_body['interventionName'],
                start_time=json_body['startTime'],
                end_time=json_body['endTime'],
                real_stress_level=json_body['realStressLevel'],
                real_stress_cause=json_body['realStressCause'],
                journal=json_body['journal'],
                event_done=json_body['eventDone'],
                intervention_done=json_body['interventionDone'],
                shared_intervention=json_body['sharedIntervention'],
                interv_effectiveness=json_body['intervEffectiveness']
            ).save()
            event = Event.objects.get(eventId=json_body['eventId'])
            event.evaluated = True
            event.save()
            if json_body['sharedIntervention'] and not Intervention.objects.filter(name=json_body['interventionName'],
                                                                                   privateUsername=None).exists():
                interv = Intervention.objects.get(name=json_body['interventionName'])
                interv.privateUsername = None
                interv.save()
            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(
            data={'result': RES_BAD_REQUEST, 'reason': 'Some arguments are not present to complete this POST request!'})


@api_view(['POST'])
def handle_evaluation_fetch(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'eventId' in json_body:
        cursor = Evaluation.objects.filter(event__owner__username=json_body['username'],
                                           event__eventId=json_body['eventId'])
        if cursor.exists():
            return Res(data={'result': RES_SUCCESS,
                             'evaluation': Evaluation.objects.get(event__owner__username=json_body['username'],
                                                                  event__eventId=json_body['eventId']).__json__()})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(
            data={'result': RES_BAD_REQUEST, 'reason': 'Some arguments are not present to complete this POST request!'})


@api_view(['POST'])
def handle_survey_fetch(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            user = User.objects.get(username=json_body['username'])
            return Res(data={'result': RES_SUCCESS, 'surveys': Survey.objects.get(user=user).__json__()})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username or password was not passed as a POST argument!'})


@api_view(['POST'])
def handle_survey_submit(request):
    json_body = json.loads(request.body.decode('utf-8'))
    print(json_body)
    if 'username' in json_body and 'password' in json_body and 'survey1' in json_body and 'survey2' in json_body \
            and 'survey3' in json_body and 'survey4' in json_body and len(json_body['survey1']) == 10 and len(json_body['survey2']) == 16 \
            and len(json_body['survey3']) == 21 and len(json_body['survey4']) == 26:
        if is_user_valid(json_body['username'], json_body['password']):
            survey = Survey.objects.get(user__username=json_body['username'])

            survey.date = int(round(time.time() * 1000))

            survey.s1q1 = json_body['survey1'][0]
            survey.s1q2 = json_body['survey1'][1]
            survey.s1q3 = json_body['survey1'][2]
            survey.s1q4 = json_body['survey1'][3]
            survey.s1q5 = json_body['survey1'][4]
            survey.s1q6 = json_body['survey1'][5]
            survey.s1q7 = json_body['survey1'][6]
            survey.s1q8 = json_body['survey1'][7]
            survey.s1q9 = json_body['survey1'][8]
            survey.s1q10 = json_body['survey1'][9]

            survey.s2q1 = json_body['survey2'][0]
            survey.s2q2 = json_body['survey2'][1]
            survey.s2q3 = json_body['survey2'][2]
            survey.s2q4 = json_body['survey2'][3]
            survey.s2q5 = json_body['survey2'][4]
            survey.s2q6 = json_body['survey2'][5]
            survey.s2q7 = json_body['survey2'][6]
            survey.s2q8 = json_body['survey2'][7]
            survey.s2q9 = json_body['survey2'][8]
            survey.s2q10 = json_body['survey2'][9]
            survey.s2q11 = json_body['survey2'][10]
            survey.s2q12 = json_body['survey2'][11]
            survey.s2q13 = json_body['survey2'][12]
            survey.s2q14 = json_body['survey2'][13]
            survey.s2q15 = json_body['survey2'][14]
            survey.s2q16 = json_body['survey2'][15]

            survey.s3q1 = json_body['survey3'][0]
            survey.s3q2 = json_body['survey3'][1]
            survey.s3q3 = json_body['survey3'][2]
            survey.s3q4 = json_body['survey3'][3]
            survey.s3q5 = json_body['survey3'][4]
            survey.s3q6 = json_body['survey3'][5]
            survey.s3q7 = json_body['survey3'][6]
            survey.s3q8 = json_body['survey3'][7]
            survey.s3q9 = json_body['survey3'][8]
            survey.s3q10 = json_body['survey3'][9]
            survey.s3q11 = json_body['survey3'][10]
            survey.s3q12 = json_body['survey3'][11]
            survey.s3q13 = json_body['survey3'][12]
            survey.s3q14 = json_body['survey3'][13]
            survey.s3q15 = json_body['survey3'][14]
            survey.s3q16 = json_body['survey3'][15]
            survey.s3q17 = json_body['survey3'][16]
            survey.s3q18 = json_body['survey3'][17]
            survey.s3q19 = json_body['survey3'][18]
            survey.s3q20 = json_body['survey3'][19]
            survey.s3q21 = json_body['survey3'][20]

            survey.s4q1 = json_body['survey4'][0]
            survey.s4q2 = json_body['survey4'][1]
            survey.s4q3 = json_body['survey4'][2]
            survey.s4q4 = json_body['survey4'][3]
            survey.s4q5 = json_body['survey4'][4]
            survey.s4q6 = json_body['survey4'][5]
            survey.s4q7 = json_body['survey4'][6]
            survey.s4q8 = json_body['survey4'][7]
            survey.s4q9 = json_body['survey4'][8]
            survey.s4q10 = json_body['survey4'][9]
            survey.s4q11 = json_body['survey4'][10]
            survey.s4q12 = json_body['survey4'][11]
            survey.s4q13 = json_body['survey4'][12]
            survey.s4q14 = json_body['survey4'][13]
            survey.s4q15 = json_body['survey4'][14]
            survey.s4q16 = json_body['survey4'][15]
            survey.s4q17 = json_body['survey4'][16]
            survey.s4q18 = json_body['survey4'][17]
            survey.s4q19 = json_body['survey4'][18]
            survey.s4q20 = json_body['survey4'][19]
            survey.s4q21 = json_body['survey4'][20]
            survey.s4q22 = json_body['survey4'][21]
            survey.s4q23 = json_body['survey4'][22]
            survey.s4q24 = json_body['survey4'][23]
            survey.s4q25 = json_body['survey4'][24]
            survey.s4q26 = json_body['survey4'][25]

            survey.save()

            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username, password, or survey elements were not completely passed as a POST argument!'})


@api_view(['POST'])
def handle_log_fetch(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and json_body['username'] == u'qobiljon' and 'password' in json_body \
            and is_user_valid(json_body['username'], json_body['password']):
        with open('log.csv', 'w') as logfile:
            wr = csv.writer(logfile, quoting=csv.QUOTE_ALL)
            wr.writerow(['THIS \"DATA\" IS EXTRACTED FROM THE DATABASE OF THE MIND-FORECASTER SERVER'])
            wr.writerow(['EXTRACTION TIME %s' % dt.datetime.now().strftime(u"%I:%M%p ON %B %d, %Y")])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['1.', 'Events'])
            wr.writerow(['Event Id', 'Owner name', 'Owner username', 'Title', 'Expected Stress Level', 'Real Stress Level',
                         'Event Start Time', 'Event End Time', 'Intervention Title', 'Intervention Reminder', 'Expected Stress Type',
                         'Expected Stress Cause', 'Is Repeating Event', 'Event Reminder', 'Is Evaluated'])
            for event in Event.objects.all():
                wr.writerow([
                    event.eventId,
                    event.owner.email,
                    event.owner.username,
                    event.title,
                    event.stressLevel,
                    event.realStressLevel,
                    to_time(event.startTime),
                    to_time(event.endTime),
                    event.intervention,
                    event.interventionReminder,
                    event.stressType,
                    event.stressCause,
                    event.repeatMode is not Event.NO_REPEAT,
                    event.eventReminder,
                    event.evaluated
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['2.', 'Interventions Created By Peers'])
            wr.writerow(['Intervention Title', 'Intervention Type', 'Private Owner'])
            for intervention in Intervention.objects.filter(interventionType=InterventionManager.PEER):
                wr.writerow([
                    unicode(intervention.name),
                    unicode(intervention.interventionType),
                    'Publicly Shared Intervention' if intervention.privateUsername is None else unicode(intervention.privateUsername)
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['3.', 'Event Evaluations'])
            wr.writerow(['Event Id', 'Event Title', 'Event Start Time', 'Event End Time', 'Intervention Title', 'Intervention Was Applied',
                         'Intervention Effectiveness', 'Expected Stress Level', 'Real Stress Level',
                         'Expected Stress Cause', 'Real Stress Cause', 'Evaluation Journal'])
            for eval in Evaluation.objects.all():
                wr.writerow([
                    eval.event.eventId,
                    eval.event.title,
                    to_time(eval.startTime),
                    to_time(eval.endTime),
                    eval.interventionName,
                    eval.interventionDone,
                    eval.intervEffectiveness,
                    eval.event.stressLevel,
                    eval.realStressLevel,
                    eval.event.stressCause,
                    eval.realStressCause,
                    eval.journal
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['4.', 'Survey'])
            wr.writerow([
                'Name',
                'Username',
                'Filled Date',
                u'예상치 않게 생긴 일 때문에 속상한 적이 얼마나 자주 있었습니까',
                u'중요한 일을 조절할 수 없다고 느낀 적이 얼마나 자주 있었습니까',
                u'불안하고 스트레스받았다고 느낀 적이 얼마나 자주 있었습니까',
                u'개인적인 문제를 잘 처리할 수 있다고 자신감을 가진 적이 얼마나 자주 있었습니까',
                u'일이 내 뜻대로 진행되고 있다고 느낀 적이 얼마나 자주 있었습니까',
                u'자신이 해야 할 모든 일에 잘 대처할 수 없었던 적이 얼마나 자주 있었습니까',
                u'일상에서 짜증나는 것을 잘 조절할 수 있었던 적이 얼마나 자주 있었습니까',
                u'자신이 일을 잘 해냈다고 느낀 적이 얼마나 자주 있었습니까',
                u'자신의 능력으로는 어떻게 해 볼 수 없는 일 때문에 화가 난 적이 얼마나 자주 있었습니까',
                u'어려운 일이 너무 많아져서 극복할 수 없다고 느낀 적이 얼마나 자주 있었습니까',
                u'내가 무슨 일을 할 때 내 모든 관심을 쏟는다',
                u'나는 내가 좋아하지 않아도 필요한 일에는 집중한다',
                u'나는 목표를 달성할 때 내가 무엇을 해야하는지에 대해 잘 알고있다',
                u'나는 목표를 달성할 때 정기적으로 진행 상황을 추적한다',
                u'나는 무언가 열심히 일할 때 내 생각에 세심한 주의를 기울인다',
                u'나는 목표를 달성할 때 내가 나의 행동을 추적 할 수 있음을 안다',
                u'내 자신을 위해 중요한 목표를 설정할 때, 나는 보통 그것을 성취한다',
                u'나는 나에게 일어나는 대부분의 문제들에 대해 분명한 계획을 세울 수 있다',
                u'내가 성취 한 목표는 나에게 많은 의미가있다',
                u'나는 계획을 세우는 것이 중요하다고 생각한다',
                u'내 자신에 대한 기준이 분명하고, 이는 내가 어떻게 일을 하고있는지 판단 할 수있게 해준다',
                u'내가 무언가 진전이 있을때 나 자신을 축하한다',
                u'나는 나중에 나 자신을 즐겁게하기 위해 힘들게 한다',
                u'14 다른 사람들이 나를 칭찬하지 않을 때에도 나는 조용히 나를 칭찬한다',
                u'내가 옳은 일을 할 때, 나는 그 느낌을 즐기기 위해 시간을 들인다',
                u'나는 진전이있을 때 특별한 것을 나에게 준다',
                u'나는 내 삶을 어떻게 살아갈지에 대한 결정을 자유롭게 할 수 있습니다',
                u'나는 다른 사람들과 상호 작용하는 것을 매우 좋아합니다',
                u'종종, 나는 실력이 있다고 느끼지 않습니다',
                u'나는 내 인생에서 압박감을 느낍니다',
                u'내가 아는 사람들은 나에게 내가 하는 것을 잘하고있다고 말해줍니다',
                u'나는 내가 연락하는 사람들과 잘 지냅니다',
                u'나는 거의 내 자신에게 집중하고 많은 사회적 접촉이 없습니다',
                u'나는 내 생각과 의견을 자유롭게 표현할 수 있습니다',
                u'나는 정기적으로 상호 작용하는 사람들이 내 친구들이라고 생각합니다',
                u'나는 최근에 흥미로운 새로운 기술을 배울 수 있었습니다',
                u'나는 일상생활에서 내가 들은것은 자주 해야만 합니다',
                u'내 인생의 사람들은 나에 대해 관심이 있습니다',
                u'나는 요즘 내가 하는 일에서 성취감을 느낍니다',
                u'나와 매일 상호 작용하는 사람들은 나의 감정을 고려하는 경향이 있습니다',
                u'내 인생에서 나는 내가 얼마나 능력 있는지 보여줄 기회를 많이 얻지 못합니다',
                u'내가 가까이 지내는 사람들이 별로 없습니다',
                u'나는 일상 생활에서 온전히 내 자신이 될 수 있다고 느낍니다',
                u'정기적으로 교류하는 사람들은 나를 좋아하는 것처럼 보이지 않습니다',
                u'나는 종종 매우 유능하다고 느끼지 않는다',
                u'일상 생활에서 어떻게 해야할 지에 대해 스스로 결정할 기회는 별로 없습니다',
                u'사람들은 일반적으로 나에게 꽤 친절합니다.',
                u'우울해지는 것에서 벗어나기',
                u'자신에게 긍정적으로 말하기',
                u'변경할 수있는 항목과 변경할 수없는 항목을 정렬하기',
                u'친구 및 가족으로부터 감정적인 지지 얻기',
                u'나의 가장 어려운 문제에 대한 해결책을 찾기',
                u'혼란스러운 문제를 작은 부분으로 나누기',
                u'스트레스 받을 때 옵션을 열어두기',
                u'문제에 직면했을 때 행동 계획을 세우고 따르기',
                u'새로운 취미 또는 레크리에이션을 개발하기',
                u'불쾌한 생각을 잊어 버리기',
                u'부정적인 상황에서 좋은 점을 찾기',
                u'슬픈 감정에 머무르지 않기',
                u'격렬한 논쟁 중에 타인의 관점에서 바라보기',
                u'첫 번째 솔루션이 작동하지 않는 경우 문제에 대한 다른 솔루션 시도',
                u'불쾌한 생각으로 화가나는 것에서 벗어나기',
                u'새 친구 사귀기',
                u'필요한 것들을 도와 줄 친구 사귀기',
                u'낙심할 때 나에게 긍정적인 행동 하기',
                u'불쾌한 생각을 버리기',
                u'한 번에 한개의 문제 생각하기',
                u'즐거운 활동이나 장소를 시각화하기',
                u'외로움을 느끼지 않게하기',
                u'기도하거나 명상하기',
                u'지역 사회 단체로부터 감정적인 지지 얻기',
                u'기준을 세우고 내가 원하는 것을 위해 싸우기',
                u'압박감을 느낄 때 급하게 행동하는 충동 막기'
            ])
            for survey in Survey.objects.all():
                wr.writerow([
                    survey.user.email,
                    survey.user.username,
                    to_time(survey.date),
                    survey.s1q1, survey.s1q2, survey.s1q3, survey.s1q4, survey.s1q5, survey.s1q6, survey.s1q7, survey.s1q8, survey.s1q9, survey.s1q10, survey.s2q1, survey.s2q2, survey.s2q3, survey.s2q4, survey.s2q5, survey.s2q6, survey.s2q7, survey.s2q8, survey.s2q9, survey.s2q10, survey.s2q11, survey.s2q12, survey.s2q13, survey.s2q14,
                    survey.s2q15, survey.s2q16, survey.s3q1, survey.s3q2, survey.s3q3, survey.s3q4, survey.s3q5, survey.s3q6, survey.s3q7, survey.s3q8, survey.s3q9, survey.s3q10, survey.s3q11, survey.s3q12, survey.s3q13, survey.s3q14, survey.s3q15, survey.s3q16, survey.s3q17, survey.s3q18, survey.s3q19, survey.s3q20, survey.s3q21, survey.s4q1,
                    survey.s4q2, survey.s4q3, survey.s4q4, survey.s4q5, survey.s4q6, survey.s4q7, survey.s4q8, survey.s4q9, survey.s4q10, survey.s4q11, survey.s4q12, survey.s4q13, survey.s4q14, survey.s4q15, survey.s4q16, survey.s4q17, survey.s4q18, survey.s4q19, survey.s4q20, survey.s4q21, survey.s4q22, survey.s4q23, survey.s4q24, survey.s4q25,
                    survey.s4q26
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['THE END OF EXTRACTED FILE'])
        with open('log.csv', 'r') as logfile:
            return Res(data={'result': RES_SUCCESS, 'data': logfile.read().decode(encoding='utf-8')})
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username or password was not passed as a POST argument!'})
