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


# Create your views here.def home(request): #fungsi (def) nama fungsinya(home)    return render(request, 'home.html')


def readCourse(request):
    data = Course.objects.all()[:1] #limit data (1 pcs)
    context = {'data_list': data}
    return render(request, 'course.html', context)

@csrf_protect
def createCourse(request):
    return render(request, 'home.html')

@csrf_protect
def updateCourse(request):
    return render(request, 'home.html')

@csrf_protect
def deleteCourse(request, user=None):
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
            fullname = form.cleaned_data.get("fullname")
            nim = form.cleaned_data.get("nim")
            email = form.cleaned_data.get("email")

            # Simpan atau dapatkan pengguna berdasarkan email
            user, created = User.objects.get_or_create(username=email)

            # Jika pengguna baru dibuat, simpan objek pengguna
            if created:
                user.save()

            # Simpan data akun pengguna
            account_user = AccountUser(
                account_user_related_user=user,
                account_user_fullname=fullname,
                account_user_student_number=nim
            )
            account_user.save()

            messages.success(request, 'Data Berhasil disimpan')
            return redirect('account:read-data-student')
    else:
        form = StudentRegisterForm()

    return render(request, 'form.html', {'form': form})

@csrf_protect
def updateStudent(request, id):
    #Create Your Task Here...
    def updateStudent(request, id):
        member = AccountUser.objects.get(account_user_related_user=id)
        user = User.objects.get(username=id)

        if request.method == 'POST':
            form = StudentRegisterForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                account_user_student_number = form.cleaned_data.get("nim")
                email = form.cleaned_data.get("email")

                if account_user_student_number:
                    member.account_user_student_number = account_user_student_number
                else:
                    messages.error(request, 'Account user student number is required')
                    return render(request, 'form.html', {'form': form})

                user.email = email
                member.save()
                user.save()
                messages.success(request, 'Data Berhasil diupdate')
                return redirect('account:read-data-student')
            else:
                print(form.errors)
        else:
            initial_data = {
                'fullname': user.first_name + ' ' + user.last_name,  # tambahkan spasi di sini
                'nim': member.account_user_student_number,
                'email': user.email,
            }
            form = StudentRegisterForm(initial=initial_data)

        return render(request, 'form.html', {'form': form})
    messages.success(request, 'Data Berhasil disimpan')
    return redirect('appsnih:read-data-student')


@csrf_protect
def deleteStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    member.delete()
    user.delete()
    messages.success(request, 'Data Berhasil dihapus')
    return redirect('appsnih:read-data-student')


def home():
    return None