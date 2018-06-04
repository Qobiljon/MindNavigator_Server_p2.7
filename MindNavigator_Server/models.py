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
    def create_event(self, event_id, owner, title, stress_level, start_time, end_time, intervention, interv_reminder, stress_type, stress_cause, repeat_mode):
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
            repeatMode=repeat_mode
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
            'repeatMode': self.repeatMode
        }


class InterventionManager(models.Manager):
    PEER = 'peer'
    SYSTEM = 'system'

    def create_intervention(self, name, intervention_type):
        return self.create(name=name, interventionType=intervention_type)


class Intervention(models.Model):
    name = models.CharField(max_length=128, primary_key=True)
    interventionType = models.CharField(max_length=6)
    objects = InterventionManager()


class EvaluationManager(models.Manager):
    def create_evaluation(self, user, event_id, intervention_name, start_time, end_time, event_done, intervention_done, intervention_done_before, recommend):
        return self.create(
            user=user,
            eventId=event_id,
            interventionName=intervention_name,
            startTime=start_time,
            endTime=end_time,
            eventDone=event_done,
            interventionDone=intervention_done,
            interventionDoneBefore=intervention_done_before,
            recommend=recommend
        )


class Evaluation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    interventionName = models.CharField(max_length=128)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    eventDone = models.BooleanField()
    interventionDone = models.BooleanField()
    interventionDoneBefore = models.BooleanField()
    recommend = models.BooleanField()
    objects = EvaluationManager()


class FeedbackManager(models.Manager):
    def create_feedback(self, user, start_time, end_time, done):
        return self.create(user=user, startTime=start_time, endTime=end_time, done=done)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventTitle = models.CharField(max_length=128)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    stressLevel = models.IntegerField()
    stressLevelSunday = models.IntegerField()
    reason = models.CharField(max_length=128)
    objects = FeedbackManager()
