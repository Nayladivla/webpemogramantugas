app_name = 'appnni'
urlpatterns = [
path('read/', views.readStudent, name='read data student'),
path('create/', views.createStudent, name='create-data-student')
]

urlpatterns = [
    path('admin/', admin.site.urls),