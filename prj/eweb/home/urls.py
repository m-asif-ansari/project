from django.urls import path, include
from home import views
from django.contrib import admin

urlpatterns = [
    path('', views.home_index, name='home_index'),
    path('dashboard', views.dashboard, name='dashboard_index'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('entry', views.entry, name='entry'),
    path('task', views.task , name="task"),
    path('pending', views.pending, name='pending'),
    path('due', views.due, name='due'),
    path('update/<int:id>', views.update_pending, name='update_pending'),
    path('bill/<int:id>', views.bill, name="bill"),
    path('delete/<int:id>', views.delete_record, name="delete_record"),
    path('updatedue/<int:id>', views.update_paid_amt, name='update_paid_amt'),    
]

admin.site.site_header = 'Ansari E-Web Services'                    
admin.site.index_title = 'Website Admin Panel'                 
admin.site.site_title = 'Admin | Ansari eWeb Services'