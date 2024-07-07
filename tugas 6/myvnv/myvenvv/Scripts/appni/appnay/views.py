from django.shortcuts import render
from appni.models import AccountUser
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from appni.models import AccountUser
from appni.signals import check_nim
from appni.forms import StudentRegisterForm

# Create your views here.def readStudent(request):
    data = AccountUser.objects.all()
    context = {'data_list': data}

    return render(request, 'index.html', context)

@csrf_protect
def createStudent(request):
if request.method == 'POST':
form = StudentRegisterForm(request.POST)
        if form.is_valid(): post_save.disconnect(check_nim)
            data = form.save(commit=False)
            data.fullname = form.cleaned_data.get("fullname")
            data.nim = form.cleaned_data.get("nim")
            data.email = form.cleaned_data.get("email")
post_save.send(
                sender=AccountUser, created=None,
                instance=data,
                dispatch_uid="check_nim")
messages.success(request, 'Data Berhasil disimpan')
            return redirect('appni:create-data-student')
else:
        form = StudentRegisterForm()

    return render(request, 'form.html', {'form': form})
    # Create your views here.
