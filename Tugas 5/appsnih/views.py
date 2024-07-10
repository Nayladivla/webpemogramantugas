import sys
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from appsnih.models import AccountUser, Course, AttendingCourse
from appsnih.signal import check_nim
from appsnih.form import StudentRegisterForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def readCourse(request):
    data = Course.objects.all()[:1]  # limit data (1 pcs)
    context = {'data_list': data}
    return render(request, 'course.html', context)

@csrf_protect
def createCourse(request):
    return render(request, 'home.html')

@csrf_protect
def updateCourse(request):
    return render(request, 'home.html')

@csrf_protect
def deleteCourse(request):
    try:
        data = Course.objects.filter(course_id=id)
        if user:
            data.delete()
            messages.success(request, 'Data Berhasil dihapus')
            return redirect('appsnih:read-data-course')
        else:
            messages.success(request, 'Data Tidak ditemukan')
            return redirect('appsnih:read-data-course')
    except:
        return redirect('appsnih:read-data-course')

def readStudent(request):
    data = AccountUser.objects.all()
    context = {'data_list': data}
    return render(request, 'index.html', context)

@csrf_protect
def createStudent(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            post_save.disconnect(check_nim)
            form.fullname = form.cleaned_data.get("fullname")
            form.nim = form.cleaned_data.get("nim")
            form.email = form.cleaned_data.get("email")
            post_save.send(
                sender=AccountUser,
                created=None,
                instance=form,
                dispatch_uid="check_nim"
            )
            messages.success(request, 'Data Berhasil disimpan')
            return redirect('appsnih:read-data-student')
    else:
        form = StudentRegisterForm()
    return render(request, 'form.html', {'form': form})

@csrf_protect
def updateStudent(request, id):
    form_update = AccountUser.objects.get(account_user_related_user=id)
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form_update.account_user_fullname = form.cleaned_data.get("fullname")
            form_update.account_user_student_number = form.cleaned_data.get("nim")
            form_update.account_user_related_user = form.cleaned_data.get("email")
            form_update.account_user_updated_by = request.user.username
            form_update.save()
            messages.success(request, 'Data Berhasil diupdate')
            return redirect('apps:read-data-student')
    else:
        form = StudentRegisterForm(initial={
            'fullname': form_update.account_user_fullname,
            'nim': form_update.account_user_student_number,
            'email': form_update.account_user_related_user,
        })
    return render(request, 'form.html', {'form': form})

@csrf_protect
def deleteStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    member.delete()
    user.delete()
    messages.success(request, 'Data Berhasil dihapus')
    return redirect('appsnih:read-data-student')
