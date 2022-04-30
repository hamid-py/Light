import datetime
from datetime import datetime, timezone, date, timedelta, time

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Spectral6, Spectral4, Spectral5, Cividis256, RdYlGn11, Inferno256, Magma11, Plasma11, \
    Plasma256
from bokeh.plotting import figure
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

from .forms import QcScoreForm, VoiceForm, SetPolicyForm, QcOperatorForm, OutputQcScoreForm, RefScoreForm
from .models import Indicators, Voice, Agent, SetPolicy, QcOperator
from khayyam import *
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator

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
    'unnecessary_referral_to_another_unit': _("ارجاع بی مورد به واحد دیگر"),
    'express_unnecessary_issues': _("بیان مسائل غیر ضروری"),
    'call_duration_management': _("مدیریت زمان مکالمه/سکوت بی مورد"),
    'negotiation': _("مذاکره"),
    'final_sentences': _("بیان جملات پایانی"),
    'ref_starting_sentences': _("بیان جملات شروع"),
    'ref_say_customer_name': _("به کار بردن نام مشتری"),
    'ref_speaking_tone': _("لحن صحبت با مشتری"),
    'ref_respect_to_customer': _("احترام به مشتری"),
    'ref_effective_listening': _("گوش دادن موثر"),
    'ref_interrupt_customer_talk': _("قطع صحبت مشتری"),
    'ref_correct_customer_guidance': _("راهنمایی صحیح مشتری "),
    'ref_familiarity_with_okala_panel': _("آشنایی با پنل اکالا"),
    'ref_correct_reference': _("مرجوعی صحیح"),
    'ref_final_sentences': _("بیان جملات پایانی"),
    'comment': _("توضیحات"),
    'output_starting_sentences': _("بیان جملات شروع"),
    'output_say_customer_name': _("به کار بردن نام مشتری"),
    'output_speaking_tone': _("لحن صحبت با مشتری"),
    'output_respect_to_customer': _("احترام به مشتری"),
    'output_anger_management': _("مدیریت خشم"),
    'output_proper_interaction': _("تعامل مناسب با مشتری"),
    'output_do_not_use_negative_verbs': _("عدم استفاده از افعال منفی"),
    'output_effective_listening': _("گوش دادن موثر"),
    'output_interrupt_customer_talk': _("قطع صحبت مشتری"),
    'output_correct_customer_guidance': _("راهنمایی صحیح مشتری"),
    'output_not_offer_discounted_goods': _("پیشنهاد کالا پرتخفیف"),
    'output_not_productology': _("محصول شناسی"),
    'output_announce_final_price_invoice': _("اعلام قیمت نهایی فاکتور"),
    'output_cancel_offer': _("عدم پیشنهاد کنسلی"),
    'output_offer_discount_code_for_organic_order': _("پیشنهاد کد تخفیف برای سفارش ارگانیک"),
    'output_unsuccessful_negotiation': _("مذاکره موفق"),
    'output_bad_time_management': _("مدیریت زمان"),
    'output_final_sentences': _("بیان جملات پایانی"),
}


def to_jalali(date):
    jalali_date = JalaliDatetime(date)
    return jalali_date.strftime(("%Y %m %d"))


@login_required(login_url='login')
def set_policy(request):
    policy = SetPolicy.objects.all().last()
    form = SetPolicyForm(instance=policy)
    if request.method == 'POST':
        form = SetPolicyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('qc')
    return render(request, 'QC/set_policy.html', {'form': form})


@login_required(login_url='login')
def voice(request):
    user = request.user
    qc_agent = user.customuser.qc_agent.last()
    if request.method == 'POST':
        form = VoiceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.qc_operator = qc_agent
            form.save()
            if form.data['department'] == 'ورودی':
                return redirect('/qc/score')
            elif form.data['department'] == 'خروجی':
                return redirect('/qc/outscore')
            elif form.data['department'] == 'مرجوعی':
                return redirect('/qc/refscore')
    form = VoiceForm()
    return render(request, 'QC/voice.html', {'form': form})


@login_required(login_url='login')
def qc_score(request):
    policy = SetPolicy.objects.all().last()
    form = QcScoreForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.score = form.instance.get_score
            form.save()
            voice = Indicators.objects.all().last()
            if voice:
                if voice.get_score_from_hundred < policy.pass_score:
                    agent = voice.voice.agent_name.agent_warning
                    agent.add_remark
                    agent.add_warning
                    agent.save()
            return redirect('/qc/voice')
    form = QcScoreForm()
    form.fields["voice"].queryset = Voice.objects.filter(created_date__gte=datetime.now() - timedelta(minutes=1))

    # voice = Indicators.objects.all().last()
    # if voice:
    #     context = voice.get_score
    # else:
    #     context = 'no data'
    return render(request, 'QC/score.html', {'form': form})


@login_required(login_url='login')
def output_qc_score(request):
    policy = SetPolicy.objects.all().last()
    form = OutputQcScoreForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.score = form.instance.get_score
            form.save()
            voice = Indicators.objects.all().last()
            if voice:
                if voice.get_score_from_hundred < policy.pass_score:
                    agent = voice.voice.agent_name.agent_warning
                    agent.add_remark
                    agent.add_warning
                    agent.save()
            return redirect('/qc/voice')
    form = OutputQcScoreForm()
    form.fields["voice"].queryset = Voice.objects.filter(created_date__gte=datetime.now() - timedelta(minutes=1))

    # voice = Indicators.objects.all().last()
    # if voice:
    #     context = voice.get_score
    # else:
    #     context = 'no data'
    return render(request, 'QC/output_score.html', {'form': form})


@login_required(login_url='login')
def ref_qc_score(request):
    policy = SetPolicy.objects.all().last()
    form = RefScoreForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.score = form.instance.get_score
            form.save()
            voice = Indicators.objects.all().last()
            if voice:
                if voice.get_score_from_hundred < policy.pass_score:
                    agent = voice.voice.agent_name.agent_warning
                    agent.add_remark
                    agent.add_warning
                    agent.save()
            return redirect('/qc/voice')
    form = RefScoreForm()
    form.fields["voice"].queryset = Voice.objects.filter(created_date__gte=datetime.now() - timedelta(minutes=1))

    # voice = Indicators.objects.all().last()
    # if voice:
    #     context = voice.get_score
    # else:
    #     context = 'no data'
    return render(request, 'QC/refscore.html', {'form': form})


@login_required(login_url='login')
def complete_extra_voice(request, pk):
    voice = Voice.objects.get(id=pk)
    form = QcScoreForm()
    form.fields["voice"].queryset = Voice.objects.filter(id=pk)
    return render(request, 'QC/refscore.html', {'form': form})


@login_required(login_url='login')
def score_history(request):
    qc_agent_list = []
    qc_agent = QcOperator.objects.all()
    qc_agent_list.append('')
    for i in qc_agent:
        qc_agent_list.append(i)

    # form = QcOperatorForm()
    if request.method == 'POST':
        form = request.POST
        if form['start'] and form['end']:

            score_objects = Voice.objects.filter(created_date__range=[form['start'], form['end']])
            p = Paginator(score_objects, 10)
            page_number = request.GET.get('page')
            page_obj = p.get_page(page_number)
            if form['qc']:
                score_objects = score_objects.filter(qc_operator__qc_agent__user__username=form['qc'])
                p = Paginator(score_objects, 10)
                page_number = request.GET.get('page')
                page_obj = p.get_page(page_number)
                return render(request, 'QC/history.html', {'page_obj': page_obj, 'qc': qc_agent_list})
            return render(request, 'QC/history.html', {'page_obj': page_obj})
        return redirect('score_history')

    score_objects = Voice.objects.all()

    p = Paginator(score_objects, 10)
    # page_list = []
    # for i in p.page_range:
    #     page_list.append(p.page(i).object_list)
    # p1 = p.page(1).object_list
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'QC/history.html', {'page_obj': page_obj, 'qc': qc_agent_list})

    # return render(request, 'QC/history.html', {'context': score_objects, 'qc': qc_agent_list, 'page': page_list})


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


@login_required(login_url='login')
def detail_score(request, pk):
    # indicators = []
    voice = Voice.objects.filter(id=pk).last()
    group = voice.agent_name.group_user.last().group_type
    comment = voice.voice.comment
    # for key, value in voice.voice.__dict__.items():
    #     if value is True:
    #         indicators.append(labels[key])
    indicators = get_detail_indicators(pk)

    return render(request, 'QC/detail_score.html', {'context': voice, 'indicators': indicators, 'comment': comment,
                                                    'group': group})


@login_required(login_url='login')
def agent_history(request):
    agent = Agent.objects.all()
    return render(request, 'QC/agent.html', {'context': agent})


@login_required(login_url='login')
def agent_history_detail(request, pk):
    agent = Agent.objects.get(id=pk)
    voices = Voice.objects.filter(agent_name__user__username=agent)
    indicators_count = []
    if request.method == 'POST':
        form = request.POST
        if form['start'] and form['end']:
            voices = voices.filter(created_date__range=[form['start'], form['end']])
    if voices:
        each_voice_list = []
        all_indicators = []
        for voice in voices:
            indicators = []
            for key, value in voice.voice.__dict__.items():
                if value is True:
                    indicators.append(labels[key])
                    all_indicators.append(labels[key])
            each_voice_list.append([voice.voice_date, voice.voice_name, voice.qc_operator, voice.voice.comment,
                                     voice.voice.get_score_from_hundred])
            each_voice_list.append(indicators)
        for i in all_indicators:
            indicators_count.append({i: all_indicators.count(i)})
        for j in indicators_count:
            if indicators_count.count(j) > 1:
                for _ in range(1, indicators_count.count(j)):
                    indicators_count.remove(j)
        for j in indicators_count:
            if indicators_count.count(j) > 1:
                for _ in range(1, indicators_count.count(j)):
                    indicators_count.remove(j)

    else:
        return HttpResponse('<h2>ویسی موجود نیست</h2>')
    if voices:
        warning_list = list()
        policy = SetPolicy.objects.all().last()
        number_of_voice = len(voices)
        warning_list = [i for i in voices if i.voice.get_score_from_hundred < policy.pass_score]
        num_of_remark = len(warning_list)

    else:
        return HttpResponse('<h2>ویسی موجود نیست</h2>')

    return render(request, 'QC/agent_detail.html', {'context': agent, 'indicators': indicators_count,
                                                    'number': number_of_voice,
                                                    'each': each_voice_list, 'remark': num_of_remark,
                                                    })


import io
import xlsxwriter


@login_required(login_url='login')
def excel_report(request):
    midnight = datetime.combine(datetime.today(), time.min)
    today = datetime.today()
    dellta = today - midnight
    delta_hours = dellta.seconds // 3600
    # create our spreadsheet.  I will create it in memory with a StringIO
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'ردیف')
    worksheet.write('B1', 'نام اپراتور')
    worksheet.write('C1', 'سرتیم')
    worksheet.write('D1', 'تیم لید')
    worksheet.write('E1', 'گروه')
    worksheet.write('F1', 'تاریخ بررسی')
    worksheet.write('G1', 'شماره تماس مشتری')
    worksheet.write('H1', 'تاریخ تماس')
    worksheet.write('I1', 'بیان جملات شروع')
    worksheet.write('J1', 'به کار بردن نام مشتری')
    worksheet.write('K1', 'لحن صحبت با مشتری')
    worksheet.write('L1', 'احترام به مشتری')
    worksheet.write('M1', 'مدیریت خشم')
    worksheet.write('N1', 'تعامل مناسب با مشتری')
    worksheet.write('O1', 'عدم استفاده از افعال منفی')
    worksheet.write('P1', 'گوش دادن موثر')
    worksheet.write('Q1', 'قطع صحبت مشتری')
    worksheet.write('R1', 'راهنمایی صحیح مشتری')
    worksheet.write('S1', 'ثبت صحیح شکایت')
    worksheet.write('T1', 'آشنایی با اپلیکیشن و سایت')
    worksheet.write('U1', 'آشنایی با پنل اکالا')
    worksheet.write('V1', 'مناسب Hold')
    worksheet.write('W1', 'Hold رعایت قانون')
    worksheet.write('X1', 'ارجاع بی مورد به واحد دیگر')
    worksheet.write('Y1', 'بیان مسائل غیرضروری')
    worksheet.write('Z1', 'مدیریت مدت زمان مکالمه/سکوت بی مورد')
    worksheet.write('AA1', 'مذاکره')
    worksheet.write('AB1', 'بیان جملات پایانی')
    worksheet.write('AC1', '')
    #output
    worksheet.write('AD1', 'بیان جملات شروع')
    worksheet.write('AE1', 'به کار بردن نام مشتری')
    worksheet.write('AF1', 'لحن صحبت با مشتری')
    worksheet.write('AG1', 'احترام به مشتری')
    worksheet.write('AH1', 'مدیریت خشم')
    worksheet.write('AI1', 'تعامل مناسب با مشتری')
    worksheet.write('AJ1', 'عدم استفاده از افعال منفی')
    worksheet.write('AK1', 'گوش دادن موثر')
    worksheet.write('AL1', 'قطع صحبت مشتری')
    worksheet.write('AM1', 'راهنمایی صحیح مشتری')
    worksheet.write('AN1', 'پیشنهاد کالا پرتخفیف')
    worksheet.write('AO1', 'محصول شناسی')
    worksheet.write('AP1', 'اعلام قیمت نهایی فاکتور')
    worksheet.write('AQ1', 'عدم پیشنهاد کنسلی')
    worksheet.write('AR1', 'پیشنهاد کد تخفیف برای سفارش ارگانیک')
    worksheet.write('AS1', 'مذاکره موفق')
    worksheet.write('AT1', 'مدیریت زمان')
    worksheet.write('AU1', 'بیان جملات پایانی')
    worksheet.write('AV1', '')
    #ref
    worksheet.write('AW1', 'بیان جملات شروع')
    worksheet.write('AX1', 'به کاربرد نام مشتری')
    worksheet.write('AY1', 'لحن صحبت با مشتری')
    worksheet.write('AZ1', 'احترام به مشتری')
    worksheet.write('BA1', 'گوش دادن موثر')
    worksheet.write('BB1', 'قطع صحبت مشتری')
    worksheet.write('BC1', 'راهنمایی صحیح مشتری')
    worksheet.write('BD1', 'آشنایی با پنل اکالا')
    worksheet.write('BE1', 'مرجوعی صحیح')
    worksheet.write('BF1', 'بیان جملات پایانی')
    worksheet.write('BG1', '')
    #RESULT
    worksheet.write('BH1', 'نمره از 50')
    worksheet.write('BI1', 'تایید/عدم تایید')
    try:
        voices = Voice.objects.filter(created_date__gte=datetime.today() - timedelta(hours=delta_hours))
        for index, voice in enumerate(voices):
            operator_name = voice.agent_name.user.username
            operator_group = voice.agent_name.group_user.last().group_type
            sarteam = voice.team_leader.team_leader.user.username
            teamlead = voice.leader.leader.user.username
            tarikh_baresi = voice.created_date
            customer_number = voice.voice_name
            tarikh_voice = str(voice.voice_date)
            starting_sentences = voice.voice.starting_sentences
            say_customer_name = voice.voice.say_customer_name
            speaking_tone = voice.voice.speaking_tone
            respect_to_customer = voice.voice.respect_to_customer
            anger_management = voice.voice.anger_management
            proper_interaction = voice.voice.proper_interaction
            do_not_use_negative_verbs = voice.voice.do_not_use_negative_verbs
            effective_listening = voice.voice.effective_listening
            interrupt_customer_talk = voice.voice.interrupt_customer_talk
            correct_customer_guidance = voice.voice.correct_customer_guidance
            proper_registration_complaint = voice.voice.proper_registration_complaint
            familiarity_with_application_site = voice.voice.familiarity_with_application_site
            familiarity_with_okala_panel = voice.voice.familiarity_with_okala_panel
            proper_hold = voice.voice.proper_hold
            observe_hold_law = voice.voice.observe_hold_law
            unnecessary_referral_to_another_unit = voice.voice.unnecessary_referral_to_another_unit
            express_unnecessary_issues = voice.voice.express_unnecessary_issues
            call_duration_management = voice.voice.call_duration_management
            negotiation = voice.voice.negotiation
            final_sentences = voice.voice.final_sentences
            #result
            score = voice.voice.score
            score_from_hundred = voice.voice.get_score_from_hundred
            #output
            output_starting_sentences = voice.voice.output_starting_sentences
            output_say_customer_name = voice.voice.output_say_customer_name
            output_speaking_tone = voice.voice.output_speaking_tone
            output_respect_to_customer = voice.voice.output_respect_to_customer
            output_anger_management = voice.voice.output_anger_management
            output_proper_interaction = voice.voice.output_proper_interaction
            output_do_not_use_negative_verbs = voice.voice.output_do_not_use_negative_verbs
            output_effective_listening = voice.voice.output_effective_listening
            output_interrupt_customer_talk = voice.voice.output_interrupt_customer_talk
            output_correct_customer_guidance = voice.voice.output_correct_customer_guidance
            output_not_offer_discounted_goods = voice.voice.output_not_offer_discounted_goods
            output_not_productology = voice.voice.output_not_productology
            output_announce_final_price_invoice = voice.voice.output_announce_final_price_invoice
            output_cancel_offer = voice.voice.output_cancel_offer
            output_offer_discount_code_for_organic_order = voice.voice.output_offer_discount_code_for_organic_order
            output_unsuccessful_negotiation = voice.voice.output_unsuccessful_negotiation
            output_bad_time_management = voice.voice.output_bad_time_management
            output_final_sentences = voice.voice.output_final_sentences
            # Rejection
            ref_starting_sentences  = voice.voice.ref_starting_sentences
            ref_say_customer_name = voice.voice.ref_say_customer_name
            ref_speaking_tone = voice.voice.ref_speaking_tone
            ref_respect_to_customer = voice.voice.ref_respect_to_customer
            ref_effective_listening = voice.voice.ref_effective_listening
            ref_interrupt_customer_talk = voice.voice.ref_interrupt_customer_talk
            ref_correct_customer_guidance = voice.voice.ref_correct_customer_guidance
            ref_familiarity_with_okala_panel = voice.voice.ref_familiarity_with_okala_panel
            ref_correct_reference = voice.voice.ref_correct_reference
            ref_final_sentences = voice.voice.ref_final_sentences


            worksheet.write(f'A{index + 2}', index + 1)
            worksheet.write(f'B{index + 2}', operator_name)
            worksheet.write(f'C{index + 2}', sarteam)
            worksheet.write(f'D{index + 2}', teamlead)
            worksheet.write(f'E{index + 2}', operator_group)
            worksheet.write(f'F{index + 2}', f'{tarikh_baresi.date()}')
            worksheet.write(f'G{index + 2}', customer_number)
            worksheet.write(f'H{index + 2}', tarikh_voice)
            worksheet.write(f'I{index + 2}', not (starting_sentences))
            worksheet.write(f'J{index + 2}', not (say_customer_name))
            worksheet.write(f'K{index + 2}', not (speaking_tone))
            worksheet.write(f'L{index + 2}', not (respect_to_customer))
            worksheet.write(f'M{index + 2}', not (anger_management))
            worksheet.write(f'N{index + 2}', not (proper_interaction))
            worksheet.write(f'O{index + 2}', not (do_not_use_negative_verbs))
            worksheet.write(f'P{index + 2}', not (effective_listening))
            worksheet.write(f'Q{index + 2}', not (interrupt_customer_talk))
            worksheet.write(f'R{index + 2}', not (correct_customer_guidance))
            worksheet.write(f'S{index + 2}', not (proper_registration_complaint))
            worksheet.write(f'T{index + 2}', not (familiarity_with_application_site))
            worksheet.write(f'U{index + 2}', not (familiarity_with_okala_panel))
            worksheet.write(f'V{index + 2}', not (proper_hold))
            worksheet.write(f'W{index + 2}', not (observe_hold_law))
            worksheet.write(f'X{index + 2}', not (unnecessary_referral_to_another_unit))
            worksheet.write(f'Y{index + 2}', not (express_unnecessary_issues))
            worksheet.write(f'Z{index + 2}', not (call_duration_management))
            worksheet.write(f'AA{index + 2}', not (negotiation))
            worksheet.write(f'AB{index + 2}', not (final_sentences))
            worksheet.write(f'AC{index + 2}', )
            #RESULT
            worksheet.write(f'BH{index + 2}', score_from_hundred)
            worksheet.write(f'BI{index + 2}', '')
            #OUTPUT
            worksheet.write(f'AD{index + 2}', not (output_starting_sentences))
            worksheet.write(f'AE{index + 2}', not (output_say_customer_name ))
            worksheet.write(f'AF{index + 2}', not (output_speaking_tone ))
            worksheet.write(f'AG{index + 2}', not (output_respect_to_customer ))
            worksheet.write(f'AH{index + 2}', not (output_anger_management ))
            worksheet.write(f'AI{index + 2}', not (output_proper_interaction ))
            worksheet.write(f'AJ{index + 2}', not (output_do_not_use_negative_verbs ))
            worksheet.write(f'AK{index + 2}', not (output_effective_listening ))
            worksheet.write(f'AL{index + 2}', not (output_interrupt_customer_talk ))
            worksheet.write(f'AM{index + 2}', not (output_correct_customer_guidance ))
            worksheet.write(f'AN{index + 2}', not (output_not_offer_discounted_goods ))
            worksheet.write(f'AO{index + 2}', not (output_not_productology ))
            worksheet.write(f'AP{index + 2}', not (output_announce_final_price_invoice ))
            worksheet.write(f'AQ{index + 2}', not (output_cancel_offer ))
            worksheet.write(f'AR{index + 2}', not (output_offer_discount_code_for_organic_order ))
            worksheet.write(f'AS{index + 2}', not (output_unsuccessful_negotiation ))
            worksheet.write(f'AT{index + 2}', not (output_bad_time_management ))
            worksheet.write(f'AU{index + 2}', not (output_final_sentences ))
            #REF
            worksheet.write(f'AW{index + 2}', not (ref_starting_sentences ))
            worksheet.write(f'AX{index + 2}', not (ref_say_customer_name ))
            worksheet.write(f'AY{index + 2}', not (ref_speaking_tone ))
            worksheet.write(f'AZ{index + 2}', not (ref_respect_to_customer ))
            worksheet.write(f'BA{index + 2}', not (ref_effective_listening ))
            worksheet.write(f'BB{index + 2}', not (ref_interrupt_customer_talk ))
            worksheet.write(f'BC{index + 2}', not (ref_correct_customer_guidance ))
            worksheet.write(f'BD{index + 2}', not (ref_familiarity_with_okala_panel ))
            worksheet.write(f'BE{index + 2}', not (ref_correct_reference ))
            worksheet.write(f'BF{index + 2}', not (ref_final_sentences ))
    except:
        return redirect('extra')
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'report-{datetime.today()}.xlsx')


def qc(request):
    return render(request, 'QC/qc.html')


import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.palettes import Spectral11
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, FactorRange
import colorcet as cc


@login_required(login_url='login')
def plot(request):
    df = pd.DataFrame(columns=['name', 'score', 'voice'])
    data_list = []
    agent = Agent.objects.all()
    for i in agent:
        operator_data = {}
        score_list = []
        operator_data['name'] = i.agent.user.username
        try:
            first_of_month = datetime.today().replace(day=1)
            voices = Voice.objects.filter(agent_name__user__username=i.agent.user.username). \
                filter(created_date__range=[first_of_month, datetime.today()])


        except:
            return redirect('extra')
        if voices:
            each_voice_list = []
            indicators = []
            indicators_count = []
            for voice in voices:
                for key, value in voice.voice.__dict__.items():
                    if value is True:
                        indicators.append(labels[key])
                each_voice_list.append([voice.voice_date, voice.voice_name, voice.qc_operator, voice.voice.comment])
                each_voice_list.append(indicators)

            for d in indicators:
                indicators_count.append({d: indicators.count(d)})
            for indic_dict in indicators_count:
                for key, value in indic_dict.items():
                    operator_data[key] = value

        operator_data['voice'] = len(voices)
        if voices:
            for j in voices:
                score_list.append(j.voice.score)
            operator_data['score'] = score_list
            data_list.append(operator_data)
    if data_list:
        for i in data_list:
            df_new = pd.DataFrame(i)
            df = pd.concat([df, df_new])
        data = df.groupby('name')['score', 'voice'].mean()
        data_source = ColumnDataSource(data)
        y = [sum(i['score']) / len(i['score']) for i in data_list]
        y2 = [i['voice'] for i in data_list]
        y3 = [i['بیان جملات شروع'] if 'بیان جملات شروع' in i else 0 for i in data_list]
        y4 = [i['به کار بردن نام مشتری'] if 'به کار بردن نام مشتری' in i else 0 for i in data_list]
        y5 = [i['لحن صحبت با مشتری'] if 'لحن صحبت با مشتری' in i else 0 for i in data_list]
        y6 = [i['احترام به مشتری'] if 'احترام به مشتری' in i else 0 for i in data_list]
        y7 = [i['مدیریت خشم'] if 'مدیریت خشم' in i else 0 for i in data_list]
        y8 = [i['تعامل مناسب با مشتری'] if 'تعامل مناسب با مشتری' in i else 0 for i in data_list]
        y9 = [i['عدم استفاده از افعال منفی'] if 'عدم استفاده از افعال منفی' in i else 0 for i in data_list]
        y10 = [i['گوش دادن موثر'] if 'گوش دادن موثر' in i else 0 for i in data_list]
        y11 = [i['قطع صحبت مشتری'] if 'قطع صحبت مشتری' in i else 0 for i in data_list]
        y12 = [i['راهنمایی صحیح مشتری'] if 'راهنمایی صحیح مشتری' in i else 0 for i in data_list]
        y13 = [i['ثبت صحیح شکایت'] if 'ثبت صحیح شکایت' in i else 0 for i in data_list]
        y14 = [i['آشنایی با اپلیکیشن و سایت'] if 'آشنایی با اپلیکیشن و سایت' in i else 0 for i in data_list]
        y15 = [i['آشنایی با پنل اکالا'] if 'آشنایی با پنل اکالا' in i else 0 for i in data_list]
        y16 = [i['hold مناسب'] if 'hold مناسب' in i else 0 for i in data_list]
        y17 = [i['hold رعایت قانون'] if 'hold رعایت قانون' in i else 0 for i in data_list]
        y18 = [i['ارجاع بی مورد به واحد دیگر'] if 'ارجاع بی مورد به واحد دیگر' in i else 0 for i in data_list]
        y19 = [i['بیان مسائل غیر ضروری'] if 'بیان مسائل غیر ضروری' in i else 0 for i in data_list]
        y20 = [i['مدیریت زمان مکالمه/سکوت بی مورد'] if 'مدیریت زمان مکالمه/سکوت بی مورد' in i else 0 for i in
               data_list]
        y21 = [i['مذاکره'] if 'مذاکره' in i else 0 for i in data_list]
        y22 = [i['بیان جملات پایانی'] if 'بیان جملات پایانی' in i else 0 for i in data_list]
        #ref
        y23 = [i['مرجوعی صحیح'] if 'مرجوعی صحیح' in i else 0 for i in data_list]
        #output
        y24 = [i['پیشنهاد کالا پرتخفیف'] if 'پیشنهاد کالا پرتخفیف' in i else 0 for i in data_list]
        y25 = [i['محصول شناسی'] if 'محصول شناسی' in i else 0 for i in data_list]
        y26 = [i['اعلام قیمت نهایی فاکتور'] if 'اعلام قیمت نهایی فاکتور' in i else 0 for i in data_list]
        y27 = [i['عدم پیشنهاد کنسلی'] if 'عدم پیشنهاد کنسلی' in i else 0 for i in data_list]
        y28 = [i['پیشنهاد کد تخفیف برای سفارش ارگانیک'] if
               'پیشنهاد کد تخفیف برای سفارش ارگانیک' in i else 0 for i in data_list]
        y29 = [i['مذاکره موفق'] if 'مذاکره موفق' in i else 0 for i in data_list]
        y30 = [i['مدیریت زمان'] if 'مدیریت زمان' in i else 0 for i in data_list]
        # name_list = data_source.data['name'].tolist()
        name_list = [i['name'] for i in data_list]
        my_data = {'name_list': name_list,
                   'score': y,
                   'number of voice': y2,
                   'بیان جملات شروع': y3,
                   'به کار بردن نام مشتری': y4,
                   'لحن صحبت با مشتری': y5,
                   'احترام به مشتری': y6,
                   'مدیریت خشم': y7,
                   'تعامل مناسب با مشتری': y8,
                   'عدم استفاده از افعال منفی': y9,
                   'گوش دادن موثر': y10,
                   'قطع صحبت مشتری': y11,
                   'راهنمایی صحیح مشتری': y12,
                   'ثبت صحیح شکایت': y13,
                   'آشنایی با اپلیکیشن و سایت': y14,
                   'آشنایی با پنل اکالا': y15,
                   'hold مناسب': y16,
                   'hold رعایت قانون': y17,
                   'ارجاع بی مورد بی واحد دیگر': y18,
                   'بیان مسائل غیر ضروری': y19,
                   'مدیریت زمان مکالمه/سکوت بی مورد': y20,
                   'مذاکره': y21,
                   'بیان جملات پایانی': y22,
                   'مرجوعی صحیح': y23,
                   'پیشنهاد کالا پرتخفیف': y24,
                   'محصول شناسی': y25,
                   'اعلام قیمت نهایی فاکتور': y26,
                   'عدم پیشنهاد کنسلی': y27,
                   'پیشنهاد کد تخفیف برای سفارش ارگانیک': y28,
                   'مذاکره موفق': y29,
                   'مدیریت زمان': y30,



                   }
        cols = ['green', 'yellow']
        y_list = ['score', 'number of voice', 'بیان جملات شروع', 'به کار بردن نام مشتری', 'لحن صحبت با مشتری',
                  'احترام به مشتری',
                  'مدیریت خشم', 'تعامل مناسب با مشتری', 'عدم استفاده از افعال منفی', 'گوش دادن موثر', 'قطع صحبت مشتری',
                  'راهنمایی صحیح مشتری',
                  'ثبت صحیح شکایت', 'آشنایی با اپلیکیشن و سایت', 'آشنایی با پنل اکالا', 'hold مناسب',
                  'hold رعایت قانون',
                  'ارجاع بی مورد بی واحد دیگر',
                  'بیان مسائل غیر ضروری', 'مدیریت زمان مکالمه/سکوت بی مورد', 'مذاکره', 'بیان جملات پایانی',
                  'مرجوعی صحیح',
                  'پیشنهاد کالا پرتخفیف', 'محصول شناسی', 'اعلام قیمت نهایی فاکتور', 'عدم پیشنهاد کنسلی',
                  'پیشنهاد کد تخفیف برای سفارش ارگانیک', 'مذاکره موفق', 'مدیریت زمان']
        palette = [cc.rainbow[i * 15] for i in range(17)]
        x = [(name, data) for name in name_list for data in y_list]
        counts = sum(zip(my_data['score'], my_data['number of voice'], my_data['بیان جملات شروع'],
                         my_data['به کار بردن نام مشتری'], my_data['لحن صحبت با مشتری'],
                         my_data['احترام به مشتری'],
                         my_data['مدیریت خشم'], my_data['تعامل مناسب با مشتری'],
                         my_data['عدم استفاده از افعال منفی'],
                         my_data['گوش دادن موثر'], my_data['قطع صحبت مشتری'],
                         my_data['راهنمایی صحیح مشتری'],
                         my_data['ثبت صحیح شکایت'], my_data['آشنایی با اپلیکیشن و سایت'],
                         my_data['آشنایی با پنل اکالا'],
                         my_data['hold مناسب'], my_data['hold رعایت قانون'],
                         my_data['ارجاع بی مورد بی واحد دیگر'],
                         my_data['بیان مسائل غیر ضروری'], my_data['مدیریت زمان مکالمه/سکوت بی مورد'],
                         my_data['مذاکره'],
                         my_data['بیان جملات پایانی'], my_data['مرجوعی صحیح'], my_data['پیشنهاد کالا پرتخفیف'],
                         my_data['محصول شناسی'], my_data['اعلام قیمت نهایی فاکتور'], my_data['عدم پیشنهاد کنسلی'],
                         my_data['پیشنهاد کد تخفیف برای سفارش ارگانیک'], my_data['مذاکره موفق'],
                         my_data['مدیریت زمان']), ())
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        h = HoverTool()
        h.tooltips = [
            ("مقدار", "@counts"),
        ]
        my_colour = ("#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#ffffbf", "#fee08b", "#fdae61", "#f46d43",
                     "#d53e4f", "#9e0142", '#000003', '#160B39', '#410967', '#6A176E', '#932567', '#BA3655', '#DC5039',
                     '#F2751A', '#FBA40A', '#F6D542', '#FCFEA4', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#808000', '#EEE8AA',
                     '#C71585', '#FF4500', '#DDA0DD','#48D1CC', '#AFEEEE')

        p = figure(x_range=FactorRange(*x))
        p.vbar(x='x', top='counts', width=0.9, source=source,
               fill_color=factor_cmap('x', palette=my_colour, factors=y_list, start=1, end=2)
               )
        # q = figure(x_range=name_list)
        # q.vbar_stack(y_list, x='name_list', source=my_data,color=cols, width=0.5,
        #              legend_label=y_list)
        operators = Agent.objects.all()
        number_of_operator = len([i for i in operators if i.agent.agent])
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        p.add_tools(h)
        p.plot_width = number_of_operator * 600
        script, div = components(p)
        # show(p)
        # show(q)
        return render(request, 'QC/bokeh.html', {'script': script, 'div': div})
    return HttpResponse('<h2>There is no voice yet in this month</h2>')


@login_required(login_url='login')
def extra_voice(request):
    extra_voice = []
    voices = Voice.objects.all()
    for i in voices:
        if not hasattr(i, 'voice'):
            extra_voice.append(i)

    return render(request, 'QC/extra.html', {'context': extra_voice})
