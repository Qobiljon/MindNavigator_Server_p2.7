import json
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response as Res
from MindNavigator_Server.models import User, Event, Intervention, InterventionManager, Evaluation
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
    time = datetime.datetime(
        year=int(_time / 1000000),
        month=int(_time / 10000) % 100,
        day=int(_time / 100) % 100,
        hour=int(_time % 100)
    )
    if _add >= 0:
        time += datetime.timedelta(hours=int(_add / 60))
    else:
        time -= datetime.timedelta(hours=int(-_add / 60))
    return int("%02d%02d%02d%02d" % (time.year % 100, time.month, time.day, time.hour))


def overlaps(user, start_time, end_time, except_id=None):
    if except_id is None:
        if Event.objects.filter(owner=user, startTime__range=(start_time, end_time - 1)).exists():
            return True
        elif Event.objects.filter(owner=user, endTime__range=(start_time + 1, end_time)).exists():
            return True
        elif Event.objects.filter(owner=user, startTime__lte=start_time, endTime__gte=end_time).exists():
            return True
    else:
        if Event.objects.filter(~Q(eventId=except_id), owner=user,
                                startTime__range=(start_time, end_time - 1)).exists():
            return True
        elif Event.objects.filter(~Q(eventId=except_id), owner=user,
                                  endTime__range=(start_time + 1, end_time)).exists():
            return True
        elif Event.objects.filter(~Q(eventId=except_id), owner=user, startTime__lte=start_time,
                                  endTime__gte=end_time).exists():
            return True


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
            User.objects.create_user(username=username, password=password, name=name)
            return Res(data={'result': RES_SUCCESS})
    else:
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'either of username, password, or name was not passed as a POST argument!'})


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
    if 'username' in json_body and 'password' in json_body and 'eventId' in json_body and 'title' in json_body \
            and 'stressLevel' in json_body and 'startTime' in json_body and 'endTime' in json_body and 'intervention' in json_body \
            and 'interventionReminder' in json_body and 'stressType' in json_body and 'stressCause' in json_body \
            and 'repeatId' in json_body and 'repeatMode' in json_body and 'eventReminder' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) and not Event.objects.filter(
                eventId=json_body['eventId']).exists() \
                and not overlaps(User.objects.get(username=json_body['username']), start_time=json_body['startTime'],
                                 end_time=json_body['endTime']):
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
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Some arguments are missing in the POST request!'})


@api_view(['POST'])
def handle_event_edit(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and 'event_id' in json_body:
        if is_user_valid(json_body['username'], json_body['password']) and Event.objects.filter(
                owner__username=json_body['username'], eventId=json_body['event_id']).exists():
            event = Event.objects.get(eventId=json_body['event_id'])
            if 'stressLevel' in json_body:
                event.stressLevel = json_body['stressLevel']
            if 'title' in json_body:
                event.title = json_body['title']
            if 'startTime' in json_body and 'endTime' in json_body and not overlaps(
                    User.objects.get(username=json_body['username']), start_time=json_body['startTime'],
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
                         'reason': 'Username, password, or event_id was not passed as a POST argument!'})


@api_view(['POST'])
def handle_event_delete(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body and ('eventId' in json_body or 'repeatId' in json_body):
        if is_user_valid(json_body['username'], json_body['password']):
            if 'eventId' in json_body and Event.objects.filter(
                    owner__username=json_body['username'],
                    eventId=json_body['eventId']
            ).exists():
                Event.objects.get(eventId=json_body['eventId']).delete()
                return Res(data={'result': RES_SUCCESS})
            elif 'repeatId' in json_body and Event.objects.filter(
                    owner__username=json_body['username'],
                    repeatId=json_body['repeatId']
            ).exists():
                Event.objects.filter(owner__username=json_body['username'], repeatId=json_body['repeatId']).delete()
                return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
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
def handle_system_intervention_get(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            array = []
            for intervention in Intervention.objects.filter(interventionType=InterventionManager.SYSTEM):
                array.append(intervention.name)
            return Res(data={'result': RES_SUCCESS, 'names': array})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST,
                         'reason': 'Username, password, or event_id was not passed as a POST argument!'})


@api_view(['POST'])
def handle_peer_intervention_get(request):
    json_body = json.loads(request.body.decode('utf-8'))
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            array = []
            for intervention in Intervention.objects.filter(interventionType=InterventionManager.PEER,
                                                            privateUsername=None):
                array.append(intervention.name)
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
            Evaluation.objects.create_evaluation(
                event=Event.objects.get(eventId=json_body['eventId']),
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
