from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Voice, Indicators, SetPolicy, QcOperator


class DateInput(forms.DateInput):
    input_type = 'date'


class QcOperatorForm(ModelForm):
    class Meta:
        model = QcOperator
        fields = ['qc_agent']


class SetPolicyForm(ModelForm):
    class Meta:
        model = SetPolicy
        fields = ['pass_score', 'allowed_remark', 'allowed_warning']


class QcScoreForm(ModelForm):
    class Meta:
        model = Indicators
        fields = ['voice', 'starting_sentences', 'say_customer_name', 'speaking_tone', 'respect_to_customer',
                  'anger_management', 'proper_interaction', 'do_not_use_negative_verbs', 'effective_listening',
                  'interrupt_customer_talk', 'correct_customer_guidance', 'proper_registration_complaint',
                  'familiarity_with_application_site', 'familiarity_with_okala_panel', 'proper_hold',
                  'observe_hold_law',
                  'unnecessary_referral_to_another_unit', 'express_unnecessary_issues', 'call_duration_management',
                  'negotiation', 'final_sentences', 'comment']
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
            'comment': _("توضیحات"),
        }

        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5, 'cols': 30})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'submit'))


class VoiceForm(ModelForm):
    class Meta:
        model = Voice
        fields = ['agent_name', 'team_leader', 'leader', 'voice_name', 'voice_date']
        widgets = {
            'voice_date': DateInput(),
        }
        labels = {
            'agent_name': _("نام اپراتور"),
            'team_leader': _('سرگروه'),
            'leader': _('لیدر'),
            'voice_name': _("شماره مشتری"),
            'voice_date': _("تاریخ تماس")

        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'submit'))


class OutputQcScoreForm(ModelForm):
    class Meta:
        model = Indicators
        fields = ['voice', 'output_starting_sentences', 'output_say_customer_name', 'output_speaking_tone',
                  'output_respect_to_customer', 'output_anger_management', 'output_proper_interaction',
                  'output_do_not_use_negative_verbs', 'output_effective_listening', 'output_interrupt_customer_talk',
                  'output_correct_customer_guidance', 'output_not_offer_discounted_goods', 'output_not_productology',
                  'output_announce_final_price_invoice', 'output_cancel_offer',
                  'output_offer_discount_code_for_organic_order', 'output_unsuccessful_negotiation',
                  'output_bad_time_management', 'output_final_sentences', 'comment']

        labels = {
            'voice': _("ویس"),
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
            'output_not_offer_discounted_goods': _("پیشنهاد کالا پرتخفیف "),
            'output_not_productology': _("محصول شناسی "),
            'output_announce_final_price_invoice': _("اعلام قیمت نهایی فاکتور"),
            'output_cancel_offer': _("عدم پیشنهاد کنسلی "),
            'output_offer_discount_code_for_organic_order': _("پیشنهاد کد تخفیف برای سفارش ارگانیک"),
            'output_unsuccessful_negotiation': _("مذاکره موفق"),
            'output_bad_time_management': _("مدیریت زمان "),
            'output_final_sentences': _("بیان جملات پایانی"),
            'comment': _("توضیحات"),
        }