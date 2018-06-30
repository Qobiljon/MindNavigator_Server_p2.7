# coding=utf-8
import time

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
    def create_event(self, event_id, owner, title, stress_level, start_time, end_time, intervention, interv_reminder,
                     stress_type, stress_cause, repeat_mode, event_reminder, repeat_id, repeat_till=0):
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
            eventReminder=event_reminder,
            repeatId=repeat_id,
            repeatTill=repeat_till
        )


class Event(models.Model):
    NO_REPEAT = 0
    REPEAT_EVERYDAY = 1
    REPEAT_WEEKLY = 2

    eventId = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    stressLevel = models.PositiveSmallIntegerField()
    realStressLevel = models.PositiveSmallIntegerField(default=0)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    intervention = models.CharField(max_length=128)
    interventionReminder = models.SmallIntegerField(default=0)
    stressType = models.CharField(max_length=32)
    stressCause = models.CharField(max_length=128)
    repeatMode = models.SmallIntegerField()
    repeatId = models.BigIntegerField(default=0)
    eventReminder = models.SmallIntegerField()
    evaluated = models.BooleanField(default=False)
    repeatTill = models.BigIntegerField(default=0)
    objects = EventManager()

    def __json__(self):
        return {
            'eventId': self.eventId,
            'title': self.title,
            'stressLevel': self.stressLevel,
            'realStressLevel': self.realStressLevel,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'intervention': self.intervention,
            'interventionReminder': self.interventionReminder,
            'stressType': self.stressType,
            'stressCause': self.stressCause,
            'repeatMode': self.repeatMode,
            'repeatId': self.repeatId,
            'eventReminder': self.eventReminder,
            'isEvaluated': self.evaluated,
            'repeatTill': self.repeatTill
        }


class InterventionManager(models.Manager):
    PEER = 'peer'
    SYSTEM = 'system'

    def create_intervention(self, name, intervention_type, private_username=None):
        return self.create(name=name, interventionType=intervention_type, privateUsername=private_username)


class Intervention(models.Model):
    name = models.CharField(max_length=128)
    interventionType = models.CharField(max_length=6)
    privateUsername = models.CharField(max_length=32, null=True, default=None)
    objects = InterventionManager()


class EvaluationManager(models.Manager):
    def create_evaluation(self, event, intervention_name, start_time, end_time, real_stress_level,
                          real_stress_cause, journal, event_done, intervention_done, shared_intervention,
                          interv_effectiveness):
        return self.create(
            event=event,
            interventionName=intervention_name,
            startTime=start_time,
            endTime=end_time,
            realStressLevel=real_stress_level,
            realStressCause=real_stress_cause,
            journal=journal,
            eventDone=event_done,
            interventionDone=intervention_done,
            sharedIntervention=shared_intervention,
            intervEffectiveness=interv_effectiveness
        )


class Evaluation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    interventionName = models.CharField(max_length=128)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    realStressLevel = models.PositiveSmallIntegerField()
    realStressCause = models.CharField(max_length=128, default='')
    journal = models.CharField(max_length=128, default='')
    eventDone = models.BooleanField()
    interventionDone = models.BooleanField()
    sharedIntervention = models.BooleanField()
    intervEffectiveness = models.PositiveSmallIntegerField()
    objects = EvaluationManager()

    def __json__(self):
        return {
            'userFullName': self.event.owner.email,
            'username': self.event.owner.username,
            'event': self.event.__json__(),
            'interventionName': self.interventionName,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'realStressLevel': self.realStressLevel,
            'realStressCause': self.realStressCause,
            'journal': self.journal,
            'eventDone': self.eventDone,
            'interventionDone': self.interventionDone,
            'sharedIntervention': self.sharedIntervention,
            'intervEffectiveness': self.intervEffectiveness
        }


class SurveyManager(models.Manager):
    def create_survey(self, user):
        return self.create(
            user=user,
            date=int(round(time.time() * 1000)),

            s1q1=0,
            s1q2=0,
            s1q3=0,
            s1q4=0,
            s1q5=0,
            s1q6=0,
            s1q7=0,
            s1q8=0,
            s1q9=0,
            s1q10=0,

            s2q1=0,
            s2q2=0,
            s2q3=0,
            s2q4=0,
            s2q5=0,
            s2q6=0,
            s2q7=0,
            s2q8=0,
            s2q9=0,
            s2q10=0,
            s2q11=0,
            s2q12=0,
            s2q13=0,
            s2q14=0,
            s2q15=0,
            s2q16=0,

            s3q1=0,
            s3q2=0,
            s3q3=0,
            s3q4=0,
            s3q5=0,
            s3q6=0,
            s3q7=0,
            s3q8=0,
            s3q9=0,
            s3q10=0,
            s3q11=0,
            s3q12=0,
            s3q13=0,
            s3q14=0,
            s3q15=0,
            s3q16=0,
            s3q17=0,
            s3q18=0,
            s3q19=0,
            s3q20=0,
            s3q21=0,

            s4q1=0,
            s4q2=0,
            s4q3=0,
            s4q4=0,
            s4q5=0,
            s4q6=0,
            s4q7=0,
            s4q8=0,
            s4q9=0,
            s4q10=0,
            s4q11=0,
            s4q12=0,
            s4q13=0,
            s4q14=0,
            s4q15=0,
            s4q16=0,
            s4q17=0,
            s4q18=0,
            s4q19=0,
            s4q20=0,
            s4q21=0,
            s4q22=0,
            s4q23=0,
            s4q24=0,
            s4q25=0,
            s4q26=0
        )


class Survey(models.Model):
    user = models.OneToOneField(to=User)
    date = models.BigIntegerField()

    s1q1 = models.SmallIntegerField()
    s1q2 = models.SmallIntegerField()
    s1q3 = models.SmallIntegerField()
    s1q4 = models.SmallIntegerField()
    s1q5 = models.SmallIntegerField()
    s1q6 = models.SmallIntegerField()
    s1q7 = models.SmallIntegerField()
    s1q8 = models.SmallIntegerField()
    s1q9 = models.SmallIntegerField()
    s1q10 = models.SmallIntegerField()

    s2q1 = models.SmallIntegerField()
    s2q2 = models.SmallIntegerField()
    s2q3 = models.SmallIntegerField()
    s2q4 = models.SmallIntegerField()
    s2q5 = models.SmallIntegerField()
    s2q6 = models.SmallIntegerField()
    s2q7 = models.SmallIntegerField()
    s2q8 = models.SmallIntegerField()
    s2q9 = models.SmallIntegerField()
    s2q10 = models.SmallIntegerField()
    s2q11 = models.SmallIntegerField()
    s2q12 = models.SmallIntegerField()
    s2q13 = models.SmallIntegerField()
    s2q14 = models.SmallIntegerField()
    s2q15 = models.SmallIntegerField()
    s2q16 = models.SmallIntegerField()

    s3q1 = models.SmallIntegerField()
    s3q2 = models.SmallIntegerField()
    s3q3 = models.SmallIntegerField()
    s3q4 = models.SmallIntegerField()
    s3q5 = models.SmallIntegerField()
    s3q6 = models.SmallIntegerField()
    s3q7 = models.SmallIntegerField()
    s3q8 = models.SmallIntegerField()
    s3q9 = models.SmallIntegerField()
    s3q10 = models.SmallIntegerField()
    s3q11 = models.SmallIntegerField()
    s3q12 = models.SmallIntegerField()
    s3q13 = models.SmallIntegerField()
    s3q14 = models.SmallIntegerField()
    s3q15 = models.SmallIntegerField()
    s3q16 = models.SmallIntegerField()
    s3q17 = models.SmallIntegerField()
    s3q18 = models.SmallIntegerField()
    s3q19 = models.SmallIntegerField()
    s3q20 = models.SmallIntegerField()
    s3q21 = models.SmallIntegerField()

    s4q1 = models.SmallIntegerField()
    s4q2 = models.SmallIntegerField()
    s4q3 = models.SmallIntegerField()
    s4q4 = models.SmallIntegerField()
    s4q5 = models.SmallIntegerField()
    s4q6 = models.SmallIntegerField()
    s4q7 = models.SmallIntegerField()
    s4q8 = models.SmallIntegerField()
    s4q9 = models.SmallIntegerField()
    s4q10 = models.SmallIntegerField()
    s4q11 = models.SmallIntegerField()
    s4q12 = models.SmallIntegerField()
    s4q13 = models.SmallIntegerField()
    s4q14 = models.SmallIntegerField()
    s4q15 = models.SmallIntegerField()
    s4q16 = models.SmallIntegerField()
    s4q17 = models.SmallIntegerField()
    s4q18 = models.SmallIntegerField()
    s4q19 = models.SmallIntegerField()
    s4q20 = models.SmallIntegerField()
    s4q21 = models.SmallIntegerField()
    s4q22 = models.SmallIntegerField()
    s4q23 = models.SmallIntegerField()
    s4q24 = models.SmallIntegerField()
    s4q25 = models.SmallIntegerField()
    s4q26 = models.SmallIntegerField()

    objects = SurveyManager()

    def __json__(self):
        return {
            'date': self.date,
            'name': self.user.email,
            'survey1': [
                {'key': u'예상치 않게 생긴 일 때문에 속상한 적이 얼마나 자주 있었습니까?', 'value': self.s1q1},
                {'key': u'중요한 일을 조절할 수 없다고 느낀 적이 얼마나 자주 있었습니까?', 'value': self.s1q2},
                {'key': u'불안하고 스트레스받았다고 느낀 적이 얼마나 자주 있었습니까?', 'value': self.s1q3},
                {'key': u'개인적인 문제를 잘 처리할 수 있다고 자신감을 가진 적이 얼마나 자주 있었습니까?', 'value': self.s1q4},
                {'key': u'일이 내 뜻대로 진행되고 있다고 느낀 적이 얼마나 자주 있었습니까?', 'value': self.s1q5},
                {'key': u'자신이 해야 할 모든 일에 잘 대처할 수 없었던 적이 얼마나 자주 있었습니까?', 'value': self.s1q6},
                {'key': u'일상에서 짜증나는 것을 잘 조절할 수 있었던 적이 얼마나 자주 있었습니까?', 'value': self.s1q7},
                {'key': u'자신이 일을 잘 해냈다고 느낀 적이 얼마나 자주 있었습니까?', 'value': self.s1q8},
                {'key': u'자신의 능력으로는 어떻게 해 볼 수 없는 일 때문에 화가 난 적이 얼마나 자주 있었습니까?', 'value': self.s1q9},
                {'key': u'어려운 일이 너무 많아져서 극복할 수 없다고 느낀 적이 얼마나 자주 있었습니까?', 'value': self.s1q10}
            ],
            'survey2': [
                {'key': u'내가 무슨 일을 할 때 내 모든 관심을 쏟는다.', 'value': self.s2q1},
                {'key': u'나는 내가 좋아하지 않아도 필요한 일에는 집중한다.', 'value': self.s2q2},
                {'key': u'나는 목표를 달성할 때 내가 무엇을 해야하는지에 대해 잘 알고있다.', 'value': self.s2q3},
                {'key': u'나는 목표를 달성할 때 정기적으로 진행 상황을 추적한다.', 'value': self.s2q4},
                {'key': u'나는 무언가 열심히 일할 때 내 생각에 세심한 주의를 기울인다.', 'value': self.s2q5},
                {'key': u'나는 목표를 달성할 때 내가 나의 행동을 추적 할 수 있음을 안다.', 'value': self.s2q6},
                {'key': u'내 자신을 위해 중요한 목표를 설정할 때, 나는 보통 그것을 성취한다.', 'value': self.s2q7},
                {'key': u'나는 나에게 일어나는 대부분의 문제들에 대해 분명한 계획을 세울 수 있다.', 'value': self.s2q8},
                {'key': u'내가 성취 한 목표는 나에게 많은 의미가있다.', 'value': self.s2q9},
                {'key': u'나는 계획을 세우는 것이 중요하다고 생각한다.', 'value': self.s2q10},
                {'key': u'내 자신에 대한 기준이 분명하고, 이는 내가 어떻게 일을 하고있는지 판단 할 수있게 해준다.', 'value': self.s2q11},
                {'key': u'내가 무언가 진전이 있을때 나 자신을 축하한다.', 'value': self.s2q12},
                {'key': u'나는 나중에 나 자신을 즐겁게하기 위해 힘들게 한다.', 'value': self.s2q13},
                {'key': u'14 다른 사람들이 나를 칭찬하지 않을 때에도 나는 조용히 나를 칭찬한다.', 'value': self.s2q14},
                {'key': u'내가 옳은 일을 할 때, 나는 그 느낌을 즐기기 위해 시간을 들인다.', 'value': self.s2q15},
                {'key': u'나는 진전이있을 때 특별한 것을 나에게 준다.', 'value': self.s2q16}
            ],
            'survey3': [
                {'key': u'나는 내 삶을 어떻게 살아갈지에 대한 결정을 자유롭게 할 수 있습니다.', 'value': self.s3q1},
                {'key': u'나는 다른 사람들과 상호 작용하는 것을 매우 좋아합니다.', 'value': self.s3q2},
                {'key': u'종종, 나는 실력이 있다고 느끼지 않습니다.', 'value': self.s3q3},
                {'key': u'나는 내 인생에서 압박감을 느낍니다.', 'value': self.s3q4},
                {'key': u'내가 아는 사람들은 나에게 내가 하는 것을 잘하고있다고 말해줍니다.', 'value': self.s3q5},
                {'key': u'나는 내가 연락하는 사람들과 잘 지냅니다.', 'value': self.s3q6},
                {'key': u'나는 거의 내 자신에게 집중하고 많은 사회적 접촉이 없습니다.', 'value': self.s3q7},
                {'key': u'나는 내 생각과 의견을 자유롭게 표현할 수 있습니다.', 'value': self.s3q8},
                {'key': u'나는 정기적으로 상호 작용하는 사람들이 내 친구들이라고 생각합니다.', 'value': self.s3q9},
                {'key': u'나는 최근에 흥미로운 새로운 기술을 배울 수 있었습니다.', 'value': self.s3q10},
                {'key': u'나는 일상생활에서 내가 들은것은 자주 해야만 합니다.', 'value': self.s3q11},
                {'key': u'내 인생의 사람들은 나에 대해 관심이 있습니다.', 'value': self.s3q12},
                {'key': u'나는 요즘 내가 하는 일에서 성취감을 느낍니다.', 'value': self.s3q13},
                {'key': u'나와 매일 상호 작용하는 사람들은 나의 감정을 고려하는 경향이 있습니다.', 'value': self.s3q14},
                {'key': u'내 인생에서 나는 내가 얼마나 능력 있는지 보여줄 기회를 많이 얻지 못합니다.', 'value': self.s3q15},
                {'key': u'내가 가까이 지내는 사람들이 별로 없습니다.', 'value': self.s3q16},
                {'key': u'나는 일상 생활에서 온전히 내 자신이 될 수 있다고 느낍니다.', 'value': self.s3q17},
                {'key': u'정기적으로 교류하는 사람들은 나를 좋아하는 것처럼 보이지 않습니다.', 'value': self.s3q18},
                {'key': u'나는 종종 매우 유능하다고 느끼지 않는다.', 'value': self.s3q19},
                {'key': u'일상 생활에서 어떻게 해야할 지에 대해 스스로 결정할 기회는 별로 없습니다.', 'value': self.s3q20},
                {'key': u'사람들은 일반적으로 나에게 꽤 친절합니다. ', 'value': self.s3q21}
            ],
            'survey4': [
                {'key': u'우울해지는 것에서 벗어나기', 'value': self.s4q1},
                {'key': u'자신에게 긍정적으로 말하기', 'value': self.s4q2},
                {'key': u'변경할 수있는 항목과 변경할 수없는 항목을 정렬하기', 'value': self.s4q3},
                {'key': u'친구 및 가족으로부터 감정적인 지지 얻기', 'value': self.s4q4},
                {'key': u'나의 가장 어려운 문제에 대한 해결책을 찾기', 'value': self.s4q5},
                {'key': u'혼란스러운 문제를 작은 부분으로 나누기', 'value': self.s4q6},
                {'key': u'스트레스 받을 때 옵션을 열어두기', 'value': self.s4q7},
                {'key': u'문제에 직면했을 때 행동 계획을 세우고 따르기', 'value': self.s4q8},
                {'key': u'새로운 취미 또는 레크리에이션을 개발하기', 'value': self.s4q9},
                {'key': u'불쾌한 생각을 잊어 버리기', 'value': self.s4q10},
                {'key': u'부정적인 상황에서 좋은 점을 찾기', 'value': self.s4q11},
                {'key': u'슬픈 감정에 머무르지 않기', 'value': self.s4q12},
                {'key': u'격렬한 논쟁 중에 타인의 관점에서 바라보기', 'value': self.s4q13},
                {'key': u'첫 번째 솔루션이 작동하지 않는 경우 문제에 대한 다른 솔루션 시도', 'value': self.s4q14},
                {'key': u'불쾌한 생각으로 화가나는 것에서 벗어나기', 'value': self.s4q15},
                {'key': u'새 친구 사귀기', 'value': self.s4q16},
                {'key': u'필요한 것들을 도와 줄 친구 사귀기', 'value': self.s4q17},
                {'key': u'낙심할 때 나에게 긍정적인 행동 하기', 'value': self.s4q18},
                {'key': u'불쾌한 생각을 버리기', 'value': self.s4q19},
                {'key': u'한 번에 한개의 문제 생각하기', 'value': self.s4q20},
                {'key': u'즐거운 활동이나 장소를 시각화하기', 'value': self.s4q21},
                {'key': u'외로움을 느끼지 않게하기', 'value': self.s4q22},
                {'key': u'기도하거나 명상하기', 'value': self.s4q23},
                {'key': u'지역 사회 단체로부터 감정적인 지지 얻기', 'value': self.s4q24},
                {'key': u'기준을 세우고 내가 원하는 것을 위해 싸우기', 'value': self.s4q25},
                {'key': u'압박감을 느낄 때 급하게 행동하는 충동 막기', 'value': self.s4q26}
            ]
        }
