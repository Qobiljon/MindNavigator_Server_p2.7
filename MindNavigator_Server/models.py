# coding=utf-8
import time

from django.db import models


class UserManager(models.Manager):

    def create_user(self, username, password, name):
        return self.create(username=username, password=password, email=name, usage=0)


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    usage = models.IntegerField()
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

    def create_intervention(self, name, intervention_type, creation_method, private_username=None):
        return self.create(name=name, interventionType=intervention_type, creationMethod=creation_method,
                           privateUsername=private_username)


class Intervention(models.Model):
    name = models.CharField(max_length=128)
    interventionType = models.CharField(max_length=6)
    privateUsername = models.CharField(max_length=32, null=True, default=None)
    creationMethod = models.CharField(max_length=6)
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
            usern=user,
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
            s2q17=0,
            s2q18=0,
            s2q19=0,
            s2q20=0,
            s2q21=0,
            s2q22=0,
            s2q23=0,
            s2q24=0,
            s2q25=0,
            s2q26=0,
            s2q27=0,
            s2q28=0,
            s2q29=0,
            s2q30=0,
            s2q31=0,
            s2q32=0,
            s2q33=0,
            s2q34=0,
            s2q35=0,
            s2q36=0,
            s2q37=0,
            s2q38=0,
            s2q39=0,
            s2q40=0,
            s2q41=0,
            s2q42=0,

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
            s3q22=0,
            s3q23=0,
            s3q24=0,
            s3q25=0,
            s3q26=0,
            s3q27=0,
            s3q28=0,
            s3q29=0,
            s3q30=0,
            s3q31=0,
            s3q32=0,
            s3q33=0,
            s3q34=0,
            s3q35=0,
            s3q36=0,
            s3q37=0,
            s3q38=0,
            s3q39=0,
            s3q40=0,
            s3q41=0,
            s3q42=0,
            s3q43=0,
            s3q44=0,
            s3q45=0,
            s3q46=0,
            s3q47=0,
            s3q48=0,
            s3q49=0,
            s3q50=0,
            s3q51=0,
            s3q52=0,
            s3q53=0,
            s3q54=0,
            s3q55=0,
            s3q56=0
        )


class Survey(models.Model):
    user = models.ForeignKey(to=User)
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
    s2q17 = models.SmallIntegerField()
    s2q18 = models.SmallIntegerField()
    s2q19 = models.SmallIntegerField()
    s2q20 = models.SmallIntegerField()
    s2q21 = models.SmallIntegerField()
    s2q22 = models.SmallIntegerField()
    s2q23 = models.SmallIntegerField()
    s2q24 = models.SmallIntegerField()
    s2q25 = models.SmallIntegerField()
    s2q26 = models.SmallIntegerField()
    s2q27 = models.SmallIntegerField()
    s2q28 = models.SmallIntegerField()
    s2q29 = models.SmallIntegerField()
    s2q30 = models.SmallIntegerField()
    s2q31 = models.SmallIntegerField()
    s2q32 = models.SmallIntegerField()
    s2q33 = models.SmallIntegerField()
    s2q34 = models.SmallIntegerField()
    s2q35 = models.SmallIntegerField()
    s2q36 = models.SmallIntegerField()
    s2q37 = models.SmallIntegerField()
    s2q38 = models.SmallIntegerField()
    s2q39 = models.SmallIntegerField()
    s2q40 = models.SmallIntegerField()
    s2q41 = models.SmallIntegerField()
    s2q42 = models.SmallIntegerField()
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
    s3q22 = models.SmallIntegerField()
    s3q23 = models.SmallIntegerField()
    s3q24 = models.SmallIntegerField()
    s3q25 = models.SmallIntegerField()
    s3q26 = models.SmallIntegerField()
    s3q27 = models.SmallIntegerField()
    s3q28 = models.SmallIntegerField()
    s3q29 = models.SmallIntegerField()
    s3q30 = models.SmallIntegerField()
    s3q31 = models.SmallIntegerField()
    s3q32 = models.SmallIntegerField()
    s3q33 = models.SmallIntegerField()
    s3q34 = models.SmallIntegerField()
    s3q35 = models.SmallIntegerField()
    s3q36 = models.SmallIntegerField()
    s3q37 = models.SmallIntegerField()
    s3q38 = models.SmallIntegerField()
    s3q39 = models.SmallIntegerField()
    s3q40 = models.SmallIntegerField()
    s3q41 = models.SmallIntegerField()
    s3q42 = models.SmallIntegerField()
    s3q43 = models.SmallIntegerField()
    s3q44 = models.SmallIntegerField()
    s3q45 = models.SmallIntegerField()
    s3q46 = models.SmallIntegerField()
    s3q47 = models.SmallIntegerField()
    s3q48 = models.SmallIntegerField()
    s3q49 = models.SmallIntegerField()
    s3q50 = models.SmallIntegerField()
    s3q51 = models.SmallIntegerField()
    s3q52 = models.SmallIntegerField()
    s3q53 = models.SmallIntegerField()
    s3q54 = models.SmallIntegerField()
    s3q55 = models.SmallIntegerField()
    s3q56 = models.SmallIntegerField()

    objects = SurveyManager()

    @staticmethod
    def __questions_json__():
        return {
            'survey1': [
                {'key': u'예상치 않게 생긴 일 때문에 속상한 적이 얼마나 자주 있었습니까?'},
                {'key': u'중요한 일을 조절할 수 없다고 느낀 적이 얼마나 자주 있었습니까?'},
                {'key': u'불안하고 스트레스받았다고 느낀 적이 얼마나 자주 있었습니까?'},
                {'key': u'개인적인 문제를 잘 처리할 수 있다고 자신감을 가진 적이 얼마나 자주 있었습니까?'},
                {'key': u'일이 내 뜻대로 진행되고 있다고 느낀 적이 얼마나 자주 있었습니까?'},
                {'key': u'자신이 해야 할 모든 일에 잘 대처할 수 없었던 적이 얼마나 자주 있었습니까?'},
                {'key': u'일상에서 짜증나는 것을 잘 조절할 수 있었던 적이 얼마나 자주 있었습니까?'},
                {'key': u'자신이 일을 잘 해냈다고 느낀 적이 얼마나 자주 있었습니까?'},
                {'key': u'자신의 능력으로는 어떻게 해 볼 수 없는 일 때문에 화가 난 적이 얼마나 자주 있었습니까?'},
                {'key': u'어려운 일이 너무 많아져서 극복할 수 없다고 느낀 적이 얼마나 자주 있었습니까?'}
            ],
            'survey2': [
                {'key': u'대다수의 사람들과 의견이 다를 경우에도, 내 의견을 분명히 말하는 편이다.'},
                {'key': u'나에게 주어진 상황은 내게 책임이 있다고 생각한다.'},
                {'key': u'현재의 내 활동반경(생활영역)을 넓힐 생각이 없다.'},
                {'key': u'대다수의 사람들은 나를 사랑스럽고 애정어리게 본다.'},
                {'key': u'그저 하루하루를 살아가고 있을 뿐 장래에 대해서는 별로 생각하지 않는다.'},
                {'key': u'살아 온 내 인생을 돌이켜 볼 때 현재의 결과에 만족한다.'},
                {'key': u'는 무슨 일을 결정하는 데 있어 다른 사람들의 영향을 받지 않는 편이다.'},
                {'key': u'매일매일 해야 하는 일들이 힘겹다.'},
                {'key': u'나 자신과 인생살이에 자극을 줄 만한 새로운 경험을 하는 것이 중요하다고 생각한다.'},
                {'key': u'남들과 친밀한 인간관계를 유지하는 것이 어렵고 힘들다.'},
                {'key': u'나는 삶의 방향과 목적에 대한 감각을 가지고 있다.'},
                {'key': u'나 자신에 대해 자부심과 자신감을 갖고 있다.'},
                {'key': u'나는 다른 사람들이 나를 어떻게 생각하는지 걱정하는 경향이 있다.'},
                {'key': u'나는 주변의 사람들과 지역사회에 잘 어울리지 않는다.'},
                {'key': u'지난 세월을 되돌아 보면, 내 자신이 크게 발전하지 못했다고 생각된다.'},
                {'key': u'나의 고민을 털어놓을 만한 가까운 친구가 별로 없어 가끔 외로움을 느낀다.'},
                {'key': u'가끔 매일 하는 일들이 사소하고 중요하지 않은 것처럼 느껴진다.'},
                {'key': u'내가 아는 많은 사람들은 인생에서 나보다 더 많은 것을 성취하는 것 같다.'},
                {'key': u'나는 강한 의견을 가진 사람으로부터 영향을 받는 편이다.'},
                {'key': u'매일의 생활에서 내가 해야 할 책임들을 잘 해내고 있다.'},
                {'key': u'그동안 한 개인으로서 크게 발전해 왔다고 생각한다.'},
                {'key': u'가족이나 친구들과 친밀한 대화를 나누는 것을 즐긴다.'},
                {'key': u'내 인생에서 무엇을 성취하려고 하는지 잘 모르겠다.'},
                {'key': u'내 성격의 거의 모든 면을 좋아한다.'},
                {'key': u'내 의견이 비록 다른 여러 사람들의 의견과 반대되는 경우에도, 나는 내 의견이 옳다고 확신한다.'},
                {'key': u'내가 해야 할 일들이 힘겹게 느껴질 때가 있다.'},
                {'key': u'현재의 생활방식을 바꿔야 할 새로운 상황에 처하는 것을 싫어한다.'},
                {'key': u'사람들은 나를 다른사람들에게 기꺼이 시간을 내어줄 수 있는 사람으로 묘사한다.'},
                {'key': u'미래의 계획을 짜고 그 계획을 실현시키려고 노력하는 것을 즐긴다.'},
                {'key': u'많은 면에서 내가 성취한 것에 대해 실망을 느낀다.'},
                {'key': u'논쟁의 여지가 있는 문제들에 대해서 내 자신의 의견을 내세우지 못한다.'},
                {'key': u'생활을 만족스럽게 꾸려 나가는 것이 쉽지 않다.'},
                {'key': u'나에게 있어서 삶은 끊임없이 배우고, 변화하고, 성장하는 과정이었다.'},
                {'key': u'다른 사람들과 다정하고 신뢰깊은 관계를 별로 경험하지 못했다.'},
                {'key': u'나는 인생목표를 가지고 살아간다.'},
                {'key': u'나는 나에 대해 다른사람들이 스스로 느끼는 것 만큼 긍정적이지 않다.'},
                {'key': u'내 스스로 정한 기준에 의해 내 자신을 평가하지, 남들의 기준에 의해 평가하지 않는다.'},
                {'key': u'내 가정과 생활방식을 내 맘에 들도록 꾸려올 수 있었다.'},
                {'key': u'내 인생을 크게 개선하거나 바꾸겠다는 생각은 오래 전에 버렸다.'},
                {'key': u'내 친구들은 믿을 수 있고, 그들도 나를 믿을 수 있다고 생각한다.'},
                {'key': u'나는 마치 내가 인생에서 해야 할 모든 것을 다한것처럼 느낀다.'},
                {'key': u'내 자신을 친구나 친지들과 비교할 때면 내 자신에 대해 흐뭇하게 느껴진다.'}
            ],
            'survey3': [
                {'key': u'문제를 해결하려고 노력할 때 나는 직감을 믿으며 처음 떠오른 해결책을 적용한다.'},
                {'key': u'직장 상사, 동료, 배우자, 자녀와 미리 계획한 대화를 나눌 때도 나는 언제가 감정적으로 대응한다.'},
                {'key': u'앞으로의 건강이 걱정스럽다.'},
                {'key': u'당면한 과제에 집중하지 못하게 방해하는 어떤 것도 능숙하게 차단한다.'},
                {'key': u'첫 번째 해결책이 효과가 없으면 원점으로 돌아가서 문제가 해결될 때까지 다른 해결책을 끊임없이 시도한다.'},
                {'key': u'호기심이 많다.'},
                {'key': u'과제에 집중하게 도와줄 긍정적인 감정을 활용하지 못한다.'},
                {'key': u'새로운 것을 시도하기를 좋아한다.'},
                {'key': u'도전적이고 어려운 일보다는 자신있고 쉬운 일을 하는 것이 더 좋다.'},
                {'key': u'사람들 표정을 보면 그가 어떤 감정을 느끼는지 알아차린다.'},
                {'key': u'일이 잘 안풀리면 포기한다.'},
                {'key': u'문제가 생기면 여러가지 해결책을 강구한 후 문제를 해결하려고 노력한다.'},
                {'key': u'역경에 처할 때 감정을 통제할 수 있다.'},
                {'key': u'나에 대한 다른 사람들 생각은 내 행동에 영향을 미치지 못한다.'},
                {'key': u'문제가 일어나는 순간, 맨 처음에 떠오르는 생각이 무엇인지 알고있다.'},
                {'key': u'내가 유일한 책임지가 아닌 상황이 가장 편안하다.'},
                {'key': u'내 능력보다 타인의 능력에 의지할 수 있는 상황을 선호한다.'},
                {'key': u'언제나 문제를 해결할 수는 없지만 해결할 수 있다고 믿는 것이 더 낫다.'},
                {'key': u'문제가 일어나면 문제의 원인부터 철저히 파악한 후 해결을 시도한다.'},
                {'key': u'직장이나 가정에서 나는 내 문제 해결 능력을 의심한다.'},
                {'key': u'내가 통제할 수 없는 요인들에 대해 숙고하는데 시간을 허비하지 않는다.'},
                {'key': u'변함없이 단순한 일상적인 일을 하는 것을 좋아한다.'},
                {'key': u'내 감정에 휩쓸린다.'},
                {'key': u'사람들이 느끼는 감정의 원인을 간파하지 못한다.'},
                {'key': u'내가 어떤 생각을 하고 그것이 내 감정에 어떤 영향을 미치는지 잘 파악한다.'},
                {'key': u'누군가에게 화가 나도 일단 마음을 진정하고 그것에 관해 대화할 알맞은 순간까지 기다릴 수 있다.'},
                {'key': u'어떤 문제에 누군가 과잉 반응을 하면 그날 그 사람이 단지 기분이 나빠서 그런 거라고 생각한다.'},
                {'key': u'나는 대부분의 일을 잘 해낼 것이다.'},
                {'key': u'사람들은 문제 해결에 도움을 얻으려고 자주 나를 찾는다.'},
                {'key': u'사람들이 특정 방식으로 대응하는 이류를 간파하지 못한다.'},
                {'key': u'내 감정이 가정, 학교, 직장에서의 집중력에 영향을 미친다.'},
                {'key': u'힘든 일에는 언제나 보상이 따른다.'},
                {'key': u'과제를 완수한 후 부정적인 평가를 받을까 봐 걱정한다.'},
                {'key': u'누군가 슬퍼하거나 분노하거나 당혹스러워할 때 그 사람이 어떤 생각을 하고 있는지 정확히 알고 있다.'},
                {'key': u'새로운 도전을 좋아하지 않는다.'},
                {'key': u'직업, 학업, 재정과 관련해서 미리 계획하지 않는다.'},
                {'key': u'동료가 흥분할 때 그 원인을 꽤 정확하게 알아차린다.'},
                {'key': u'어떤 일이든 미리 계획하기보다는 즉흥적으로 하는 것을 좋아한다.그것이 별로 효과적이지 않아도 그렇다.'},
                {'key': u'대부분의 문제는 내가 통제할 수 없는 상황 때문에 일어난다.'},
                {'key': u'도전은 나 자신이 성장하고 배우는 한 가지 방법이다.'},
                {'key': u'내가 사건과 상황을 오해하고 있다는 말을 들은 적이 있다.'},
                {'key': u'누군가 내게 화를 내면 대응하기 전에 그의 말을 귀 기울여 듣는다.'},
                {'key': u'내 미래에 대해 생각할 때 성공한 내 모습이 상상되지 않는다.'},
                {'key': u'문제가 일어날 때 내가 속단해 버린다는 말을 들은 적이 있다.'},
                {'key': u'새로운 사람들을 만나는 것이 불편하다.'},
                {'key': u'책이나 영화에 쉽게 몰입한다.'},
                {'key': u'"예방이 치료보다 낫다."는 속담을 믿는다.'},
                {'key': u'거의 모든 상황에서 문제의 진짜 원인을 잘 파악한다.'},
                {'key': u'훌륭한 대처 기술을 갖고 있으며 대부분의 문제에 잘 대응한다.'},
                {'key': u'배우자나 가까운 친구들은 내가 그들을 이해하지 못한다고 말한다.'},
                {'key': u'판에 박힌 일과를 처리할 때 가장 편안하다.'},
                {'key': u'문제는 최대한 빨리 해결하는 것이 중요하다.설령 그 문제를 충분히 파악하지 못하더라도 그렇다.'},
                {'key': u'어려운 상황에 처할 때 나는 그것이 잘 해결될 거라고 자신한다.'},
                {'key': u'동료와 친구들은 내가 그들 말을 경청하지 않는다고 말한다.'},
                {'key': u'어떤 것이 갖고 싶으면 즉이 나가서 그것을 산다.'},
                {'key': u'동료나 가족과 "민감한"주제에 대해 의논할 때 감정을 자제할 수 있다.'}
            ]
        }
