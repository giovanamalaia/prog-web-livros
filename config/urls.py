from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    
    path('', include('core.urls')),

    # Início da recuperação de senha:
    path('senha/recuperar/', auth_views.PasswordResetView.as_view(
        template_name='core/auth/password_reset_form.html',
        html_email_template_name='core/auth/password_reset_email.html',
        subject_template_name='core/auth/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),

    # Página informando que o email foi enviado: 
    path('senha/recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/auth/password_reset_done.html'
    ), name='password_reset_done'),

    # Link que vem no email:
    path('senha/recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/auth/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),

    # Página informando que a senha foi resetada com sucesso:
    path('senha/recuperar/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
