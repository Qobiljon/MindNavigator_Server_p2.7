from django.db import models


class UserManager(models.Manager):
    def create_user(self, username, password, name):
        return self.create(username=username, password=password, email=name)


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    objects = UserManager()


class EventManager(models.Manager):
    def create_event(self, event_id, owner, title, stress_level, start_time, end_time, intervention, interv_reminder, stress_type, stress_cause, repeat_mode, event_reminder):
        return self.create(
            eventId=event_id,
            owner=owner,
            title=title,
            stressLevel=stress_level,
            startTime=start_time,
            endTime=end_time,
            intervention=intervention,
            interventionReminder=interv_reminder,
            stressType=stress_type,
            stressCause=stress_cause,
            repeatMode=repeat_mode,
            eventReminder=event_reminder
        )


class Event(models.Model):
    NO_REPEAT = 0
    REPEAT_EVERYDAY = 1
    REPEAT_WEEKLY = 2

    eventId = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    stressLevel = models.PositiveSmallIntegerField()
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    intervention = models.CharField(max_length=128)
    interventionReminder = models.SmallIntegerField(default=0)
    stressType = models.CharField(max_length=32)
    stressCause = models.CharField(max_length=128)
    repeatMode = models.SmallIntegerField()
    eventReminder = models.SmallIntegerField()
    evaluated = models.BooleanField(default=False)
    objects = EventManager()

    def __json__(self):
        return {
            'eventId': self.eventId,
            'title': self.title,
            'stressLevel': self.stressLevel,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'intervention': self.intervention,
            'interventionReminder': self.interventionReminder,
            'stressType': self.stressType,
            'stressCause': self.stressCause,
            'repeatMode': self.repeatMode,
            'eventReminder': self.eventReminder,
            'isEvaluated': self.evaluated
        }


class InterventionManager(models.Manager):
    PEER = 'peer'
    SYSTEM = 'system'

    def create_intervention(self, name, intervention_type, private_username=None):
        return self.create(name=name, interventionType=intervention_type, private_username=private_username)


class Intervention(models.Model):
    name = models.CharField(max_length=128, primary_key=True)
    interventionType = models.CharField(max_length=6)
    private_username = models.CharField(max_length=32, null=True, default=None)
    objects = InterventionManager()


class EvaluationManager(models.Manager):
    def create_evaluation(self, user, event_id, intervention_name, start_time, end_time, real_stress_level, event_done, intervention_done, intervention_done_before, shared_intervention, interv_effectiveness):
        return self.create(
            user=user,
            eventId=event_id,
            interventionName=intervention_name,
            startTime=start_time,
            endTime=end_time,
            realStressLevel=real_stress_level,
            eventDone=event_done,
            interventionDone=intervention_done,
            interventionDoneBefore=intervention_done_before,
            sharedIntervention=shared_intervention,
            intervEffectiveness=interv_effectiveness
        )


class Evaluation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    interventionName = models.CharField(max_length=128)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    realStressLevel = models.PositiveSmallIntegerField()
    eventDone = models.BooleanField()
    interventionDone = models.BooleanField()
    interventionDoneBefore = models.BooleanField()
    sharedIntervention = models.BooleanField()
    intervEffectiveness = models.PositiveSmallIntegerField()
    objects = EvaluationManager()

    def __json__(self):
        return {
            'userFullName': self.user.email,
            'username': self.user.username,
            'eventId': self.eventId,
            'interventionName': self.interventionName,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'eventDone': self.eventDone,
            'interventionDone': self.interventionDone,
            'interventionDoneBefore': self.interventionDoneBefore,
            'recommend': self.sharedIntervention
        }


class FeedbackManager(models.Manager):
    def create_feedback(self, user, event_id, stress_incr_reason):
        return self.create(
            user=user,
            eventId=event_id,
            stressIncrReason=stress_incr_reason
        )


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventId = models.BigIntegerField()
    stressIncrReason = models.CharField(max_length=128)
    objects = FeedbackManager()
