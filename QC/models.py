from django.db import models
from result.models import CustomUser


class Voice(models.Model):
    voice_name = models.CharField(max_length=30)
    agent_name = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Indicators(models.Model):
    pass_indicator = models.BooleanField(default=False)
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE, related_name='voice')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    voice_date = models.DateTimeField()
    score = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class SleepyVoice(Indicators):
    error_name = 'sleepy voice'
    category = 'Tune of voice'
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

