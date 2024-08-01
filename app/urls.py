from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main, visit, doctor, pharmacy, partner
)

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # visits
    path("export-visits", visit.export_visits_view, name="export_visits"),

    # files
    re_path(r'^files/(?P<path>.*)$', main.get_file),


    path('successfully-created', main.successfully_created, name='successfully_created'),
    # doctor
    path('doctor-add', doctor.DoctorCreateView.as_view(), name='create_doctor'),
    path('pharmacy-add', pharmacy.PharmacyCreateView.as_view(), name='create_pharmacy'),
    path('partners-add', partner.PartnerCreateView.as_view(), name='create_partner'),
]
