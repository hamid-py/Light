# Generated by Django 3.2.9 on 2022-04-25 14:14

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('QC', '0002_alter_indicators_voice'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicators',
            name='output_anger_management',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_announce_final_price_invoice',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_bad_time_management',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_cancel_offer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_correct_customer_guidance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_do_not_use_negative_verbs',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_effective_listening',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_final_sentences',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_interrupt_customer_talk',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_not_offer_discounted_goods',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_not_productology',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_offer_discount_code_for_organic_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_proper_interaction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_respect_to_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_say_customer_name',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_speaking_tone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_starting_sentences',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='output_unsuccessful_negotiation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_correct_customer_guidance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_correct_reference',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_effective_listening',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_familiarity_with_okala_panel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_final_sentences',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_interrupt_customer_talk',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_respect_to_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_say_customer_name',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_speaking_tone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicators',
            name='ref_starting_sentences',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='voice',
            field=models.OneToOneField(limit_choices_to={'created_date__gte': datetime.datetime(2022, 4, 25, 18, 43, 19, 720281)}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voice', to='QC.voice'),
        ),
        migrations.AlterField(
            model_name='voice',
            name='voice_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2022, 4, 25)),
        ),
    ]
