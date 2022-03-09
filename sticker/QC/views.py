import datetime

from django.shortcuts import render, redirect

from .forms import QcScoreForm, VoiceForm, SetPolicyForm, QcOperatorForm
from .models import Indicators, Voice, Agent, SetPolicy, QcOperator
from khayyam import *
from django.utils.translation import ugettext_lazy as _

labels = {
    'voice': _("ویس"),
    'starting_sentences': _("بیان جملات شروع"),
    'say_customer_name': _("به کار بردن نام مشتری"),
    'speaking_tone': _("لحن صحبت با مشتری"),
    'respect_to_customer': _("احترام به مشتری"),
    'anger_management': _("مدیریت خشم"),
    'proper_interaction': _("تعامل مناسب با مشتری"),
    'do_not_use_negative_verbs': _("عدم استفاده از افعال منفی"),
    'effective_listening': _("گوش دادن موثر"),
    'interrupt_customer_talk': _("قطع صحبت مشتری"),
    'correct_customer_guidance': _("راهنمایی صحیح مشتری"),
    'proper_registration_complaint': _("ثبت صحیح شکایت"),
    'familiarity_with_application_site': _("آشنایی با اپلیکیشن و سایت"),
    'familiarity_with_okala_panel': _("آشنایی با پنل اکالا"),
    'proper_hold': _("hold مناسب"),
    'observe_hold_law': _("hold رعایت قانون"),
    'unnecessary_referral_to_another_unit': _("ارجاع به مورد به واحد دیگر"),
    'express_unnecessary_issues': _("بیان مسائل غیر ضروری"),
    'call_duration_management': _("مدیریت زمان مکالمه/سکوت بی مورد"),
    'negotiation': _("مذاکره"),
    'final_sentences': _("بیان جملات پایانی"),
}


def to_jalali(date):
    jalali_date = JalaliDatetime(date)
    return jalali_date.strftime(("%Y %m %d"))


def set_policy(request):
    form = SetPolicyForm()
    if request.method == 'POST':
        form = SetPolicyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('voice')
    return render(request, 'QC/set_policy.html', {'form': form})


def voice(request):
    user = request.user
    qc_agent = user.customuser.qc_agent.last()
    if request.method == 'POST':
        form = VoiceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.qc_operator = qc_agent
            form.save()
            return redirect('/qc/score')
    form = VoiceForm()
    return render(request, 'QC/voice.html', {'form': form})


def qc_score(request):
    policy = SetPolicy.objects.all().last()
    print(policy.pass_score, 'hello from policy score+++++++')
    form = QcScoreForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.score = form.instance.get_score
            form.save()
            voice = Indicators.objects.all().last()
            if voice:
                if voice.score < policy.pass_score:
                    agent = voice.voice.agent_name.agent_warning
                    agent.add_remark
                    agent.add_warning
                    agent.save()
            return redirect('/qc/voice')
    form = QcScoreForm()
    # voice = Indicators.objects.all().last()
    # if voice:
    #     context = voice.get_score
    # else:
    #     context = 'no data'
    return render(request, 'QC/score.html', {'form': form})


def score_history(request):
    qc_agent_list = []
    qc_agent = QcOperator.objects.all()
    for i in qc_agent:
        qc_agent_list.append(i)

    # form = QcOperatorForm()
    if request.method == 'POST':
        form = request.POST
        if form['start'] and form['end']:
            score_objects = Voice.objects.filter(created_date__range=[form['start'], form['end']])
            if form['qc']:
                score_objects = score_objects.filter(qc_operator__qc_agent__user__username=form['qc'])

            return render(request, 'QC/history.html', {'context': score_objects})
        # return redirect('score_history')

    score_objects = Voice.objects.all()

    return render(request, 'QC/history.html', {'context': score_objects, 'qc': qc_agent_list})


def delete_voice(request, pk):
    voice = Voice.objects.filter(id=pk).last()
    voice.delete()
    return redirect('score_history')


def get_detail_indicators(pk):
    indicators = []
    voice = Voice.objects.filter(id=pk).last()
    for key, value in voice.voice.__dict__.items():
        if value is True:
            indicators.append(labels[key])
    return indicators


def detail_score(request, pk):
    # indicators = []
    voice = Voice.objects.filter(id=pk).last()
    # for key, value in voice.voice.__dict__.items():
    #     if value is True:
    #         indicators.append(labels[key])
    indicators = get_detail_indicators(pk)

    return render(request, 'QC/detail_score.html', {'context': voice, 'indicators': indicators})


def agent_history(request):
    agent = Agent.objects.all()
    return render(request, 'QC/agent.html', {'context': agent})


def agent_history_detail(request, pk):
    agent = Agent.objects.get(id=pk)
    voices = Voice.objects.filter(agent_name__user__username=agent)
    indicators = []
    indicators_count = []
    if request.method == 'POST':
        form = request.POST
        if form['start'] and form['end']:
            voices = voices.filter(created_date__range=[form['start'], form['end']])
    if voices:
        for voice in voices:
            for key, value in voice.voice.__dict__.items():
                if value is True:
                    indicators.append(labels[key])
        for i in indicators:
            indicators_count.append({i: indicators.count(i)})
    number_of_voice = len(voices)

    return render(request, 'QC/agent_detail.html', {'context': agent, 'indicators': indicators_count,
                                                    'number': number_of_voice})
