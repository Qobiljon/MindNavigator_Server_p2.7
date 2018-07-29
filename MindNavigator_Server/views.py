# coding=utf-8
import json
import random
import time
import unicodecsv as csv
import calendar as cal
import datetime as dt

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
        if Event.objects.filter(~Q(eventId=except_id), owner__username=username,
                                startTime__range=(start_time, end_time - 1)).exists():
            return True
        elif Event.objects.filter(~Q(eventId=except_id), owner__username=username,
                                  endTime__range=(start_time + 1, end_time)).exists():
            return True
        elif Event.objects.filter(~Q(eventId=except_id), owner__username=username, startTime__lte=start_time,
                                  endTime__gte=end_time).exists():
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
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'either of username, password, or name was not passed as a POST argument!'})


@api_view(['POST'])
def handle_login(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            user = User.objects.get(username=json_body['username'])
            user.usage = user.usage + 1
            user.save()
            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})


@api_view(['POST'])
def handle_event_submit(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and 'eventId' in json_body and 'title' in json_body and 'stressLevel' in json_body and 'startTime' in json_body and 'endTime' in json_body and 'intervention' in json_body \
            and 'interventionReminder' in json_body and 'stressType' in json_body and 'stressCause' in json_body and 'repeatId' in json_body and 'repeatTill' in json_body and 'repeatMode' in json_body and 'eventReminder' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) and not Event.objects.filter(
                eventId=json_body['eventId']).exists():
            if json_body['repeatMode'] is Event.NO_REPEAT:
                if not overlaps(username=json_body['username'], start_time=json_body['startTime'],
                                end_time=json_body['endTime']):
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
            if 'eventId' in json_body and Event.objects.filter(owner__username=json_body['username'],
                                                               eventId=json_body['eventId']).exists():
                Event.objects.get(eventId=json_body['eventId']).delete()
                return Res(data={'result': RES_SUCCESS})
            elif 'repeatId' in json_body and Event.objects.filter(owner__username=json_body['username'],
                                                                  repeatId=json_body['repeatId']).exists():
                array = []
                for event in Event.objects.filter(owner__username=json_body['username'],
                                                  repeatId=json_body['repeatId']):
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
def handle_intervention_submit(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and 'interventionName' in json_body and 'intervCreateMethod' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) and not Intervention.objects.filter(
                name=json_body['interventionName']).exists():
            if not Intervention.objects.filter(name=json_body['interventionName'], privateUsername=None).exists():
                Intervention.objects.create_intervention(name=json_body['interventionName'],
                                                         intervention_type=InterventionManager.PEER,
                                                         creation_method=json_body['intervCreateMethod'],
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
        return Res(
            data={'result': RES_BAD_REQUEST, 'reason': 'Username or password was not passed as a POST argument!'})


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
            User.objects.get(user__username=json_body['username'])
            return Res(data={'result': RES_SUCCESS, 'surveys': Survey.__questions_json__()})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(
            data={'result': RES_BAD_REQUEST, 'reason': 'Username or password was not passed as a POST argument!'})


@api_view(['POST'])
def handle_survey_submit(request):
    json_body = json.loads(request.body.decode('utf-8'))
    print(json_body)
    if 'username' in json_body and 'password' in json_body and 'survey1' in json_body and 'survey2' in json_body \
            and 'survey3' in json_body and len(json_body['survey1']) == 10 and len(json_body['survey2']) == 42 \
            and len(json_body['survey3']) == 56:
        if is_user_valid(json_body['username'], json_body['password']):
            Survey.objects.create_survey(
                user=User.objects.get(username=json_body['username']),
                date=int(round(time.time() * 1000)),
                s1q1=json_body['survey1'][0],
                s1q2=json_body['survey1'][1],
                s1q3=json_body['survey1'][2],
                s1q4=json_body['survey1'][3],
                s1q5=json_body['survey1'][4],
                s1q6=json_body['survey1'][5],
                s1q7=json_body['survey1'][6],
                s1q8=json_body['survey1'][7],
                s1q9=json_body['survey1'][8],
                s1q10=json_body['survey1'][9],
                s2q1=json_body['survey2'][0],
                s2q2=json_body['survey2'][1],
                s2q3=json_body['survey2'][2],
                s2q4=json_body['survey2'][3],
                s2q5=json_body['survey2'][4],
                s2q6=json_body['survey2'][5],
                s2q7=json_body['survey2'][6],
                s2q8=json_body['survey2'][7],
                s2q9=json_body['survey2'][8],
                s2q10=json_body['survey2'][9],
                s2q11=json_body['survey2'][10],
                s2q12=json_body['survey2'][11],
                s2q13=json_body['survey2'][12],
                s2q14=json_body['survey2'][13],
                s2q15=json_body['survey2'][14],
                s2q16=json_body['survey2'][15],
                s2q17=json_body['survey2'][16],
                s2q18=json_body['survey2'][17],
                s2q19=json_body['survey2'][18],
                s2q20=json_body['survey2'][19],
                s2q21=json_body['survey2'][20],
                s2q22=json_body['survey2'][21],
                s2q23=json_body['survey2'][22],
                s2q24=json_body['survey2'][23],
                s2q25=json_body['survey2'][24],
                s2q26=json_body['survey2'][25],
                s2q27=json_body['survey2'][26],
                s2q28=json_body['survey2'][27],
                s2q29=json_body['survey2'][28],
                s2q30=json_body['survey2'][29],
                s2q31=json_body['survey2'][30],
                s2q32=json_body['survey2'][31],
                s2q33=json_body['survey2'][32],
                s2q34=json_body['survey2'][33],
                s2q35=json_body['survey2'][34],
                s2q36=json_body['survey2'][35],
                s2q37=json_body['survey2'][36],
                s2q38=json_body['survey2'][37],
                s2q39=json_body['survey2'][38],
                s2q40=json_body['survey2'][39],
                s2q41=json_body['survey2'][40],
                s2q42=json_body['survey2'][41],
                s3q1=json_body['survey3'][0],
                s3q2=json_body['survey3'][1],
                s3q3=json_body['survey3'][2],
                s3q4=json_body['survey3'][3],
                s3q5=json_body['survey3'][4],
                s3q6=json_body['survey3'][5],
                s3q7=json_body['survey3'][6],
                s3q8=json_body['survey3'][7],
                s3q9=json_body['survey3'][8],
                s3q10=json_body['survey3'][9],
                s3q11=json_body['survey3'][10],
                s3q12=json_body['survey3'][11],
                s3q13=json_body['survey3'][12],
                s3q14=json_body['survey3'][13],
                s3q15=json_body['survey3'][14],
                s3q16=json_body['survey3'][15],
                s3q17=json_body['survey3'][16],
                s3q18=json_body['survey3'][17],
                s3q19=json_body['survey3'][18],
                s3q20=json_body['survey3'][19],
                s3q21=json_body['survey3'][20],
                s3q22=json_body['survey3'][21],
                s3q23=json_body['survey3'][22],
                s3q24=json_body['survey3'][23],
                s3q25=json_body['survey3'][24],
                s3q26=json_body['survey3'][25],
                s3q27=json_body['survey3'][26],
                s3q28=json_body['survey3'][27],
                s3q29=json_body['survey3'][28],
                s3q30=json_body['survey3'][29],
                s3q31=json_body['survey3'][30],
                s3q32=json_body['survey3'][31],
                s3q33=json_body['survey3'][32],
                s3q34=json_body['survey3'][33],
                s3q35=json_body['survey3'][34],
                s3q36=json_body['survey3'][35],
                s3q37=json_body['survey3'][36],
                s3q38=json_body['survey3'][37],
                s3q39=json_body['survey3'][38],
                s3q40=json_body['survey3'][39],
                s3q41=json_body['survey3'][40],
                s3q42=json_body['survey3'][41],
                s3q43=json_body['survey3'][42],
                s3q44=json_body['survey3'][43],
                s3q45=json_body['survey3'][44],
                s3q46=json_body['survey3'][45],
                s3q47=json_body['survey3'][46],
                s3q48=json_body['survey3'][47],
                s3q49=json_body['survey3'][48],
                s3q50=json_body['survey3'][49],
                s3q51=json_body['survey3'][50],
                s3q52=json_body['survey3'][51],
                s3q53=json_body['survey3'][52],
                s3q54=json_body['survey3'][53],
                s3q55=json_body['survey3'][54],
                s3q56=json_body['survey3'][55]
            ).save()

            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'Username, password, or survey elements were not completely passed as a POST argument!'})


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
            wr.writerow(['1.', 'Users'])
            wr.writerow(['Username', "User's name", 'Usage'])
            for user in User.objects.all():
                wr.writerow([
                    user.username,
                    user.email,
                    user.usage
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['2.', 'Events'])
            wr.writerow(
                ['Event Id', 'Owner name', 'Owner username', 'Title', 'Expected Stress Level', 'Real Stress Level',
                 'Event Start Time', 'Event End Time', 'Intervention Title', 'Intervention Reminder',
                 'Expected Stress Type',
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
            wr.writerow(['3.', 'Interventions Created By Peers'])
            wr.writerow(['Intervention Title', 'Intervention Type', 'Creation Method', 'Private Owner'])
            for intervention in Intervention.objects.filter(interventionType=InterventionManager.PEER):
                wr.writerow([
                    unicode(intervention.name),
                    unicode(intervention.interventionType),
                    unicode(intervention.creationMethod),
                    'Publicly Shared Intervention' if intervention.privateUsername is None else unicode(
                        intervention.privateUsername)
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['4.', 'Event Evaluations'])
            wr.writerow(['Event Id', 'Event Title', 'Event Start Time', 'Event End Time', 'Intervention Title',
                         'Intervention Was Applied',
                         'Intervention Effectiveness', 'Expected Stress Level', 'Real Stress Level',
                         'Expected Stress Cause', 'Real Stress Cause', 'Evaluation Journal'])
            for _eval in Evaluation.objects.all():
                wr.writerow([
                    _eval.event.eventId,
                    _eval.event.title,
                    to_time(_eval.startTime),
                    to_time(_eval.endTime),
                    _eval.interventionName,
                    _eval.interventionDone,
                    _eval.intervEffectiveness,
                    _eval.event.stressLevel,
                    _eval.realStressLevel,
                    _eval.event.stressCause,
                    _eval.realStressCause,
                    _eval.journal
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['5.', 'Survey'])
            wr.writerow([
                'Name',
                'Username',
                'Filled Date',
                u'예상치 않게 생긴 일 때문에 속상한 적이 얼마나 자주 있었습니까?',
                u'중요한 일을 조절할 수 없다고 느낀 적이 얼마나 자주 있었습니까?',
                u'불안하고 스트레스받았다고 느낀 적이 얼마나 자주 있었습니까?',
                u'개인적인 문제를 잘 처리할 수 있다고 자신감을 가진 적이 얼마나 자주 있었습니까?',
                u'일이 내 뜻대로 진행되고 있다고 느낀 적이 얼마나 자주 있었습니까?',
                u'자신이 해야 할 모든 일에 잘 대처할 수 없었던 적이 얼마나 자주 있었습니까?',
                u'일상에서 짜증나는 것을 잘 조절할 수 있었던 적이 얼마나 자주 있었습니까?',
                u'자신이 일을 잘 해냈다고 느낀 적이 얼마나 자주 있었습니까?',
                u'자신의 능력으로는 어떻게 해 볼 수 없는 일 때문에 화가 난 적이 얼마나 자주 있었습니까?',
                u'어려운 일이 너무 많아져서 극복할 수 없다고 느낀 적이 얼마나 자주 있었습니까?',
                u'대다수의 사람들과 의견이 다를 경우에도, 내 의견을 분명히 말하는 편이다.',
                u'나에게 주어진 상황은 내게 책임이 있다고 생각한다.',
                u'현재의 내 활동반경(생활영역)을 넓힐 생각이 없다.',
                u'대다수의 사람들은 나를 사랑스럽고 애정어리게 본다.',
                u'그저 하루하루를 살아가고 있을 뿐 장래에 대해서는 별로 생각하지 않는다.',
                u'살아 온 내 인생을 돌이켜 볼 때 현재의 결과에 만족한다.',
                u'는 무슨 일을 결정하는 데 있어 다른 사람들의 영향을 받지 않는 편이다.',
                u'매일매일 해야 하는 일들이 힘겹다.',
                u'나 자신과 인생살이에 자극을 줄 만한 새로운 경험을 하는 것이 중요하다고 생각한다.',
                u'남들과 친밀한 인간관계를 유지하는 것이 어렵고 힘들다.',
                u'나는 삶의 방향과 목적에 대한 감각을 가지고 있다.',
                u'나 자신에 대해 자부심과 자신감을 갖고 있다.',
                u'나는 다른 사람들이 나를 어떻게 생각하는지 걱정하는 경향이 있다.',
                u'나는 주변의 사람들과 지역사회에 잘 어울리지 않는다.',
                u'지난 세월을 되돌아 보면, 내 자신이 크게 발전하지 못했다고 생각된다.',
                u'나의 고민을 털어놓을 만한 가까운 친구가 별로 없어 가끔 외로움을 느낀다.',
                u'가끔 매일 하는 일들이 사소하고 중요하지 않은 것처럼 느껴진다.',
                u'내가 아는 많은 사람들은 인생에서 나보다 더 많은 것을 성취하는 것 같다.',
                u'나는 강한 의견을 가진 사람으로부터 영향을 받는 편이다.',
                u'매일의 생활에서 내가 해야 할 책임들을 잘 해내고 있다.',
                u'그동안 한 개인으로서 크게 발전해 왔다고 생각한다.',
                u'가족이나 친구들과 친밀한 대화를 나누는 것을 즐긴다.',
                u'내 인생에서 무엇을 성취하려고 하는지 잘 모르겠다.',
                u'내 성격의 거의 모든 면을 좋아한다.',
                u'내 의견이 비록 다른 여러 사람들의 의견과 반대되는 경우에도, 나는 내 의견이 옳다고 확신한다.',
                u'내가 해야 할 일들이 힘겹게 느껴질 때가 있다.',
                u'현재의 생활방식을 바꿔야 할 새로운 상황에 처하는 것을 싫어한다.',
                u'사람들은 나를 다른사람들에게 기꺼이 시간을 내어줄 수 있는 사람으로 묘사한다.',
                u'미래의 계획을 짜고 그 계획을 실현시키려고 노력하는 것을 즐긴다.',
                u'많은 면에서 내가 성취한 것에 대해 실망을 느낀다.',
                u'논쟁의 여지가 있는 문제들에 대해서 내 자신의 의견을 내세우지 못한다.',
                u'생활을 만족스럽게 꾸려 나가는 것이 쉽지 않다.',
                u'나에게 있어서 삶은 끊임없이 배우고, 변화하고, 성장하는 과정이었다.',
                u'다른 사람들과 다정하고 신뢰깊은 관계를 별로 경험하지 못했다.',
                u'나는 인생목표를 가지고 살아간다.',
                u'나는 나에 대해 다른사람들이 스스로 느끼는 것 만큼 긍정적이지 않다.',
                u'내 스스로 정한 기준에 의해 내 자신을 평가하지, 남들의 기준에 의해 평가하지 않는다.',
                u'내 가정과 생활방식을 내 맘에 들도록 꾸려올 수 있었다.',
                u'내 인생을 크게 개선하거나 바꾸겠다는 생각은 오래 전에 버렸다.',
                u'내 친구들은 믿을 수 있고, 그들도 나를 믿을 수 있다고 생각한다.',
                u'나는 마치 내가 인생에서 해야 할 모든 것을 다한것처럼 느낀다.',
                u'내 자신을 친구나 친지들과 비교할 때면 내 자신에 대해 흐뭇하게 느껴진다.',
                u'문제를 해결하려고 노력할 때 나는 직감을 믿으며 처음 떠오른 해결책을 적용한다.',
                u'직장 상사, 동료, 배우자, 자녀와 미리 계획한 대화를 나눌 때도 나는 언제가 감정적으로 대응한다.',
                u'앞으로의 건강이 걱정스럽다.',
                u'당면한 과제에 집중하지 못하게 방해하는 어떤 것도 능숙하게 차단한다.',
                u'첫 번째 해결책이 효과가 없으면 원점으로 돌아가서 문제가 해결될 때까지 다른 해결책을 끊임없이 시도한다.',
                u'호기심이 많다.',
                u'과제에 집중하게 도와줄 긍정적인 감정을 활용하지 못한다.',
                u'새로운 것을 시도하기를 좋아한다.',
                u'도전적이고 어려운 일보다는 자신있고 쉬운 일을 하는 것이 더 좋다.',
                u'사람들 표정을 보면 그가 어떤 감정을 느끼는지 알아차린다.',
                u'일이 잘 안풀리면 포기한다.',
                u'문제가 생기면 여러가지 해결책을 강구한 후 문제를 해결하려고 노력한다.',
                u'역경에 처할 때 감정을 통제할 수 있다.',
                u'나에 대한 다른 사람들 생각은 내 행동에 영향을 미치지 못한다.',
                u'문제가 일어나는 순간, 맨 처음에 떠오르는 생각이 무엇인지 알고있다.',
                u'내가 유일한 책임지가 아닌 상황이 가장 편안하다.',
                u'내 능력보다 타인의 능력에 의지할 수 있는 상황을 선호한다.',
                u'언제나 문제를 해결할 수는 없지만 해결할 수 있다고 믿는 것이 더 낫다.',
                u'문제가 일어나면 문제의 원인부터 철저히 파악한 후 해결을 시도한다.',
                u'직장이나 가정에서 나는 내 문제 해결 능력을 의심한다.',
                u'내가 통제할 수 없는 요인들에 대해 숙고하는데 시간을 허비하지 않는다.',
                u'변함없이 단순한 일상적인 일을 하는 것을 좋아한다.',
                u'내 감정에 휩쓸린다.',
                u'사람들이 느끼는 감정의 원인을 간파하지 못한다.',
                u'내가 어떤 생각을 하고 그것이 내 감정에 어떤 영향을 미치는지 잘 파악한다.',
                u'누군가에게 화가 나도 일단 마음을 진정하고 그것에 관해 대화할 알맞은 순간까지 기다릴 수 있다.',
                u'어떤 문제에 누군가 과잉 반응을 하면 그날 그 사람이 단지 기분이 나빠서 그런 거라고 생각한다.',
                u'나는 대부분의 일을 잘 해낼 것이다.',
                u'사람들은 문제 해결에 도움을 얻으려고 자주 나를 찾는다.',
                u'사람들이 특정 방식으로 대응하는 이류를 간파하지 못한다.',
                u'내 감정이 가정, 학교, 직장에서의 집중력에 영향을 미친다.',
                u'힘든 일에는 언제나 보상이 따른다.',
                u'과제를 완수한 후 부정적인 평가를 받을까 봐 걱정한다.',
                u'누군가 슬퍼하거나 분노하거나 당혹스러워할 때 그 사람이 어떤 생각을 하고 있는지 정확히 알고 있다.',
                u'새로운 도전을 좋아하지 않는다.',
                u'직업, 학업, 재정과 관련해서 미리 계획하지 않는다.',
                u'동료가 흥분할 때 그 원인을 꽤 정확하게 알아차린다.',
                u'어떤 일이든 미리 계획하기보다는 즉흥적으로 하는 것을 좋아한다.그것이 별로 효과적이지 않아도 그렇다.',
                u'대부분의 문제는 내가 통제할 수 없는 상황 때문에 일어난다.',
                u'도전은 나 자신이 성장하고 배우는 한 가지 방법이다.',
                u'내가 사건과 상황을 오해하고 있다는 말을 들은 적이 있다.',
                u'누군가 내게 화를 내면 대응하기 전에 그의 말을 귀 기울여 듣는다.',
                u'내 미래에 대해 생각할 때 성공한 내 모습이 상상되지 않는다.',
                u'문제가 일어날 때 내가 속단해 버린다는 말을 들은 적이 있다.',
                u'새로운 사람들을 만나는 것이 불편하다.',
                u'책이나 영화에 쉽게 몰입한다.',
                u'"예방이 치료보다 낫다."는 속담을 믿는다.',
                u'거의 모든 상황에서 문제의 진짜 원인을 잘 파악한다.',
                u'훌륭한 대처 기술을 갖고 있으며 대부분의 문제에 잘 대응한다.',
                u'배우자나 가까운 친구들은 내가 그들을 이해하지 못한다고 말한다.',
                u'판에 박힌 일과를 처리할 때 가장 편안하다.',
                u'문제는 최대한 빨리 해결하는 것이 중요하다.설령 그 문제를 충분히 파악하지 못하더라도 그렇다.',
                u'어려운 상황에 처할 때 나는 그것이 잘 해결될 거라고 자신한다.',
                u'동료와 친구들은 내가 그들 말을 경청하지 않는다고 말한다.',
                u'어떤 것이 갖고 싶으면 즉이 나가서 그것을 산다.',
                u'동료나 가족과 "민감한"주제에 대해 의논할 때 감정을 자제할 수 있다.'
            ])
            for survey in Survey.objects.all():
                wr.writerow([
                    survey.user.email,
                    survey.user.username,
                    to_time(survey.date),
                    survey.s1q1, survey.s1q2, survey.s1q3, survey.s1q4, survey.s1q5, survey.s1q6, survey.s1q7,
                    survey.s1q8, survey.s1q9, survey.s1q10, survey.s2q1, survey.s2q2, survey.s2q3, survey.s2q4,
                    survey.s2q5, survey.s2q6, survey.s2q7, survey.s2q8, survey.s2q9, survey.s2q10, survey.s2q11,
                    survey.s2q12, survey.s2q13, survey.s2q14, survey.s2q15, survey.s2q16, survey.s2q17, survey.s2q18,
                    survey.s2q19, survey.s2q20, survey.s2q21, survey.s2q22, survey.s2q23, survey.s2q24, survey.s2q25,
                    survey.s2q26, survey.s2q27, survey.s2q28, survey.s2q29, survey.s2q30, survey.s2q31, survey.s2q32,
                    survey.s2q33, survey.s2q34, survey.s2q35, survey.s2q36, survey.s2q37, survey.s2q38, survey.s2q39,
                    survey.s2q40, survey.s2q41, survey.s2q42, survey.s3q1, survey.s3q2, survey.s3q3, survey.s3q4,
                    survey.s3q5, survey.s3q6, survey.s3q7, survey.s3q8, survey.s3q9, survey.s3q10, survey.s3q11,
                    survey.s3q12, survey.s3q13, survey.s3q14, survey.s3q15, survey.s3q16, survey.s3q17, survey.s3q18,
                    survey.s3q19, survey.s3q20, survey.s3q21, survey.s3q22, survey.s3q23, survey.s3q24, survey.s3q25,
                    survey.s3q26, survey.s3q27, survey.s3q28, survey.s3q29, survey.s3q30, survey.s3q31, survey.s3q32,
                    survey.s3q33, survey.s3q34, survey.s3q35, survey.s3q36, survey.s3q37, survey.s3q38, survey.s3q39,
                    survey.s3q40, survey.s3q41, survey.s3q42, survey.s3q43, survey.s3q44, survey.s3q45, survey.s3q46,
                    survey.s3q47, survey.s3q48, survey.s3q49, survey.s3q50, survey.s3q51, survey.s3q52, survey.s3q53,
                    survey.s3q54, survey.s3q55, survey.s3q56
                ])
            wr.writerow([])
            wr.writerow([])
            wr.writerow(['THE END OF EXTRACTED FILE'])
        with open('log.csv', 'r') as logfile:
            return Res(data={'result': RES_SUCCESS, 'data': logfile.read().decode(encoding='utf-8')})
    else:
        return Res(
            data={'result': RES_BAD_REQUEST, 'reason': 'Username or password was not passed as a POST argument!'})
