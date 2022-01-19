import string
from datetime import datetime, timezone, date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.views.generic.list import ListView

from .models import CustomUser, Group, Membership, Principal, AgentHistory, StartRest, EndRest
from django.shortcuts import render
from .forms import PrincipalForm, MembershipForm, PasswordChangeCustomForm

IN_rest_list = []
OUT_rest_list = []
CRM_rest_list = []


class LoginAdmin(LoginView):
    template_name = 'result/Login.html'


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'result/change_password.html', {
        'form': form
    })


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login'
    model = CustomUser
    template_name = 'result/user.html'

    def test_func(self):
        user = CustomUser.objects.get(user=self.request.user.id)

        if int(user.position) > 0:
            return True
        return False




class GroupLIstView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login'
    model = Group
    template_name = 'result/group.html'

    def test_func(self):
        user = CustomUser.objects.get(user=self.request.user.id)

        if int(user.position) > 0:
            return True
        return False


@login_required(login_url='login')
def principal_view(request):
    user = CustomUser.objects.get(user=request.user.id)

    if int(user.position) > 0:
        form = PrincipalForm(request.POST or None, request.FILES or None)
        context = {}

        # create object of form
        if request.method == 'POST':

            # check if form data is valid
            if form.is_valid():
                # save the form data to model
                form.save()

        context['form'] = form
        return render(request, "result/principal.html", context)
    return HttpResponse("<p><h2>You don't have permission to access this page<h2></p>")


@login_required(login_url='login')
def update_principal(request, pk):
    user = CustomUser.objects.get(user=request.user.id)

    if int(user.position) > 0:
        group = Group.objects.get(id=pk)
        new_pk = group.principal.id
        try:
            principal = Principal.objects.get(id=new_pk)
        except:
            raise Http404("Principal does not exist")

        form = PrincipalForm(instance=principal)

        if request.method == 'POST':
            form = PrincipalForm(request.POST, instance=principal)
            if form.is_valid():
                form.save()
                return redirect('group')
        context = {'form': form, 'new_pk': pk}
        return render(request, 'result/update_principal.html', context)
    return HttpResponse("<p><h2>You don't have permission to access this page<h2></p>")


@login_required(login_url='login')
def membership_view(request):
    user = CustomUser.objects.get(user=request.user.id)

    if int(user.position) > 0:
        members = Membership.objects.all()
        context = {'members': members}
        # form = MembershipForm(request.POST or None, request.FILES or None)
        # if request.method == 'POST':
        #     if form.is_valid():
        #         form.save()
        # context = {'form': form}
        return render(request, 'result/membership.html', context)
    return HttpResponse("<p><h2>You don't have permission to access this page<h2></p>")


@login_required(login_url='login')
def update_membership_view(request, pk):
    user = CustomUser.objects.get(user=request.user.id)

    if int(user.position) > 0:

        membership = Membership.objects.get(id=pk)
        user = membership.user
        group = membership.group

        form = MembershipForm(instance=membership)
        if request.method == 'POST':
            form = MembershipForm(request.POST, instance=membership)
            if form.is_valid():
                form.save()
                return redirect('membership')

        context = {'form': form, 'pk': pk}
        return render(request, 'result/update_membership.html', context)
    return HttpResponse("<p><h2>You don't have permission to access this page<h2></p>")


@login_required(login_url='login')
def start_rest(request):
    context = {'status': True}
    user = CustomUser.objects.get(user=request.user.id)

    allowed_number_of_rest = user.group_user.first().principal.limit_number_of_rest_number
    group = user.group_user.last().group_type
    rest_start_list = StartRest.objects.filter(in_rest_flag=1)
    rest_start_user = [i.user for i in rest_start_list]
    if IN_rest_list:
        for i in IN_rest_list:
            if i not in rest_start_user:
                IN_rest_list.remove(i)
    if OUT_rest_list:
        for i in OUT_rest_list:
            if i not in rest_start_user:
                OUT_rest_list.remove(i)
    if CRM_rest_list:
        for i in CRM_rest_list:
            if i not in rest_start_user:
                CRM_rest_list.remove(i)
    if group == 'IN':
        group_list_name = IN_rest_list
    elif group == 'OUT':
        group_list_name = OUT_rest_list
    elif group == 'CRM':
        group_list_name = CRM_rest_list
    if request.method == 'POST':

        if len(group_list_name) < allowed_number_of_rest:
            group_list_name.append(user)
            # if user.group_user.first().rest_flag == 0:
            group_id = user.group_user.first().id
            a = Group.objects.get(id=group_id)
            a.rest_flag += 1
            a.save()
            StartRest.objects.create(user=user)

            return redirect('end_rest', pk=request.user.id)

        elif request.user in [name.user for name in group_list_name]:
            return redirect('end_rest', pk=request.user.id)

        else:
            return redirect('start_rest')

    if request.user in [name.user for name in IN_rest_list + OUT_rest_list + CRM_rest_list]:
        return redirect('end_rest', pk=request.user.id)
    if len(group_list_name) >= allowed_number_of_rest:
        context = {'group_list': group_list_name}
        return render(request, 'result/rest.html', context)
    else:
        return render(request, 'result/rest.html', context)


@login_required(login_url='login')
def end_rest(request, pk):
    user = CustomUser.objects.get(user=pk)
    context = {'status': True}
    if request.user == user.user:
        if request.method == 'POST':
            user_object = CustomUser.objects.get(user=pk)
            group = user_object.group_user.last().group_type
            if group == 'IN':
                group_list_name = IN_rest_list
            elif group == 'OUT':
                group_list_name = OUT_rest_list
            elif group == 'CRM':
                group_list_name = CRM_rest_list
            group_id = user_object.group_user.first().id
            a = Group.objects.get(id=group_id)
            a.rest_flag -= 1
            a.save()
            if user_object in group_list_name:
                EndRest.objects.create(user=user, start_rest=user.start.last())

                group_list_name.remove(user_object)
            else:
                return redirect('start_rest')
            allowed_rest_time = user.group_user.first().principal.limit_rest_time
            rest_time = user.end.last().end_rest - user.end.last().start_rest.start_rest
            minute_time = rest_time.seconds // 60
            seconds_time = rest_time.seconds % 60
            if rest_time > allowed_rest_time:
                extra_time = rest_time - allowed_rest_time
                extra_time_seconds = extra_time.seconds
                extra_minute_time = extra_time.seconds // 60
                extra_seconds_time = extra_time.seconds % 60
            else:
                extra_time_seconds = 0
                extra_minute_time = 0
                extra_seconds_time = 0
            AgentHistory.objects.create(
                user=user,
                total_rest_time=f'{minute_time} minutes {seconds_time} seconds',
                total_error_time=f'{extra_minute_time} minutes {extra_seconds_time} seconds',
                total_error_seconds=extra_time_seconds,
                total_rest_seconds=rest_time.seconds)
            user_start_rest = user.start.last()
            user_start_rest.in_rest_flag = 0
            user_start_rest.save()
            return redirect('start_rest')
        if request.user in [name.user for name in IN_rest_list + OUT_rest_list + CRM_rest_list]:
            return render(request, 'result/end.html', context)
        else:
            return redirect('start_rest')

    return render(request, 'result/rest.html', context)


class AgentHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login'
    model = AgentHistory
    template_name = 'result/agent_history.html'

    ordering = ['-created_date', 'user']

    # def get_ordering(self):
    #     ordering = self.request.GET.get('user')
    #     # validate ordering here
    #     return ordering

    def test_func(self):
        user = CustomUser.objects.get(user=self.request.user.id)

        if int(user.position) > 0:
            return True
        return False


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(user=request.user.id)
        position = int(user.position)
        context = {'position': position}

        return render(request, 'result/home.html', context)
    return redirect('login')


@login_required(login_url='login')
def report_export(request):
    user = CustomUser.objects.get(user=request.user.id)
    user_in_rest = IN_rest_list + OUT_rest_list + CRM_rest_list

    if int(user.position) > 0:
        user_history_list = []
        for user in CustomUser.objects.all():
            if not int(user.position) > 0:

                if user.history.all():
                    total_seconds = 0
                    total_error = 0
                    number_of_error = 0
                    number_of_rest = 0
                    report = {}
                    for history in user.history.filter(created_date__gte=datetime.today() - timedelta(days=1)):
                        total_seconds += history.total_rest_seconds
                        total_error += history.total_error_seconds
                        if history.total_error_seconds:
                            number_of_error += 1
                        number_of_rest += 1
                    total_seconds_min = total_seconds // 60
                    total_seconds_seconds = total_seconds % 60
                    total_error_min = total_error // 60
                    total_error_seconds = total_error % 60
                    report['total_seconds_min'] = total_seconds_min
                    report['total_seconds_seconds'] = total_seconds_seconds
                    report['total_error_min'] = total_error_min
                    report['total_error_seconds'] = total_error_seconds
                    report['number_of_error'] = number_of_error
                    report['number_of_rest'] = number_of_rest
                    report['user'] = user.user
                    user_history_list.append(report)
        context = {'history': user_history_list, 'rest': user_in_rest}

        return render(request, 'result/report.html', context)
    return HttpResponse("<p><h2>You don't have permission to access this page<h2></p>")


import io
import xlsxwriter


@login_required(login_url='login')
def excelreport(request):
    user = CustomUser.objects.get(user=request.user.id)

    if int(user.position) > 0:
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()

        user_history_list = []
        for user in CustomUser.objects.all():
            if not int(user.position) > 0:

                if user.history.all():
                    total_seconds = 0
                    total_error = 0
                    number_of_error = 0
                    number_of_rest = 0
                    report = {}
                    for history in user.history.filter(created_date__gte=datetime.today() - timedelta(days=1)):
                        total_seconds += history.total_rest_seconds
                        total_error += history.total_error_seconds
                        if history.total_error_seconds:
                            number_of_error += 1
                        number_of_rest += 1
                    total_seconds_min = total_seconds // 60
                    total_seconds_seconds = total_seconds % 60
                    total_error_min = total_error // 60
                    total_error_seconds = total_error % 60
                    report['total_seconds_min'] = total_seconds_min
                    report['total_seconds_seconds'] = total_seconds_seconds
                    report['total_error_min'] = total_error_min
                    report['total_error_seconds'] = total_error_seconds
                    report['number_of_error'] = number_of_error
                    report['number_of_rest'] = number_of_rest
                    report['user'] = user.user.username
                    user_history_list.append(report)
        date = datetime.today()
        alphabet = list(string.ascii_uppercase)
        worksheet.write('A1', 'user')
        worksheet.write('A2', 'Total rest time(minute)')
        worksheet.write('A3', 'Total rest time(second)')
        worksheet.write('A4', 'Total error time(minute)')
        worksheet.write('A5', 'Total error time(second)')
        worksheet.write('A6', 'number_of_rest')
        worksheet.write('A7', 'number_of_error')
        worksheet.write('A8', str(date))
        for i, report in enumerate(user_history_list):
            worksheet.write(f'{alphabet[i + 1]}1', report['user'])
            worksheet.write(f'{alphabet[i + 1]}2', report['total_seconds_min'])
            worksheet.write(f'{alphabet[i + 1]}3', report['total_seconds_seconds'])
            worksheet.write(f'{alphabet[i + 1]}4', report['total_error_min'])
            worksheet.write(f'{alphabet[i + 1]}5', report['total_error_seconds'])
            worksheet.write(f'{alphabet[i + 1]}6', report['number_of_rest'])
            worksheet.write(f'{alphabet[i + 1]}7', report['number_of_error'])

        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='report.xlsx')
    return HttpResponse("<p><h2>You don't have permission to access this page<h2></p>")
