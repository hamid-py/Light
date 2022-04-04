import datetime

from django.db import models
from result.models import CustomUser
from django_jalali.db import models as jmodels


class Agent(models.Model):
    agent = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agent_warning')
    number_of_remark = models.IntegerField(default=0)
    number_of_warning = models.IntegerField(default=0)
    number_of_retraining = models.IntegerField(default=0)

    @property
    def add_remark(self):
        self.number_of_remark += 1
        return self.number_of_remark

    @property
    def add_warning(self):
        self.number_of_warning = self.number_of_remark // 5
        return self.number_of_remark

    def __str__(self):
        return f'{self.agent}'


class TeamLeader(models.Model):
    team_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='team_leader')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_leader.user.username


class Leader(models.Model):
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leader')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.leader.user.username


class QcOperator(models.Model):
    qc_agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='qc_agent')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.qc_agent}'


class SetPolicy(models.Model):
    pass_score = models.IntegerField(default=10)
    allowed_remark = models.IntegerField(default=3)
    allowed_warning = models.IntegerField(default=2)

    def __str__(self):
        return f'pass_score: {self.pass_score}, allowed_remark: {self.allowed_remark}'


class Voice(models.Model):
    voice_name = models.CharField(max_length=30)
    agent_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agent')
    qc_operator = models.ForeignKey(QcOperator, on_delete=models.SET_DEFAULT, default=1, related_name='qc')
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='sarteam')
    leader = models.ForeignKey(Leader, on_delete=models.ForeignKey, related_name='teamlead')
    voice_date = jmodels.jDateField(default=datetime.datetime.today())
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.voice_name


def get_time():
    time_ = datetime.datetime.now()
    return time_


class Indicators(models.Model):
    recent_time = get_time()
    starting_sentences = models.BooleanField(default=False)
    say_customer_name = models.BooleanField(default=False)
    speaking_tone = models.BooleanField(default=False)
    respect_to_customer = models.BooleanField(default=False)
    anger_management = models.BooleanField(default=False)
    proper_interaction = models.BooleanField(default=False)
    do_not_use_negative_verbs = models.BooleanField(default=False)
    effective_listening = models.BooleanField(default=False)
    interrupt_customer_talk = models.BooleanField(default=False)
    correct_customer_guidance = models.BooleanField(default=False)
    proper_registration_complaint = models.BooleanField(default=False)
    familiarity_with_application_site = models.BooleanField(default=False)
    familiarity_with_okala_panel = models.BooleanField(default=False)
    proper_hold = models.BooleanField(default=False)
    observe_hold_law = models.BooleanField(default=False)
    unnecessary_referral_to_another_unit = models.BooleanField(default=False)
    express_unnecessary_issues = models.BooleanField(default=False)
    call_duration_management = models.BooleanField(default=False)
    negotiation = models.BooleanField(default=False)
    final_sentences = models.BooleanField(default=False)

    comment = models.CharField(max_length=500, null=True, blank=True)
    voice = models.OneToOneField(Voice, on_delete=models.CASCADE,
                                 related_name='voice', null=True, limit_choices_to={'created_date__gte':
                                                                                        recent_time - datetime.timedelta(
                                                                                            minutes=1)})
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    score_from_hundred = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'voice:{self.voice}'

    @property
    def get_score(self):
        indicators_list = [self.starting_sentences, self.say_customer_name, self.speaking_tone,
                           self.respect_to_customer,
                           self.anger_management, self.proper_interaction, self.do_not_use_negative_verbs,
                           self.effective_listening, self.interrupt_customer_talk, self.correct_customer_guidance,
                           self.proper_registration_complaint, self.familiarity_with_application_site,
                           self.familiarity_with_okala_panel, self.proper_hold,
                           self.observe_hold_law, self.unnecessary_referral_to_another_unit,
                           self.express_unnecessary_issues, self.call_duration_management, self.negotiation,
                           self.final_sentences]
        self.score = len(indicators_list) - sum(indicators_list)
        return self.score

    @property
    def get_score_from_hundred(self):
        self.score_from_hundred = 50 - sum([int(self.starting_sentences) * 3, int(self.say_customer_name) * 2,
                                            int(self.speaking_tone) * 4,
                                            int(self.respect_to_customer) * 3,
                                            int(self.anger_management) * 3, int(self.proper_interaction) * 2,
                                            int(self.do_not_use_negative_verbs) * 1,
                                            int(self.effective_listening) * 4, int(self.interrupt_customer_talk) * 2,
                                            int(self.correct_customer_guidance) * 4,
                                            int(self.proper_registration_complaint) * 4,
                                            int(self.familiarity_with_application_site) * 3,
                                            int(self.familiarity_with_okala_panel) * 3, int(self.proper_hold) * 1,
                                            int(self.observe_hold_law) * 1,
                                            int(self.unnecessary_referral_to_another_unit) * 2,
                                            int(self.express_unnecessary_issues) * 1,
                                            int(self.call_duration_management) * 2,
                                            int(self.negotiation) * 3,
                                            int(self.final_sentences) * 2])
        return self.score_from_hundred
