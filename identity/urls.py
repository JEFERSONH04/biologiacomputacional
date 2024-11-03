from django.urls import path
from identity import views
from identity.views import ProfileView, ProfilePasswordChangeView, password_reset_confirm, PasswordResetInvalidView, ManageUsersView, info_usuarios, detalle_usuarios, ascender_administrador
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),
    path('perfil/', ProfileView.as_view(), name='perfil'),
    path('cambio_contrasena/', ProfilePasswordChangeView.as_view(), name='cambio_contrasena'),
    path('gestion_usuarios/', ManageUsersView.as_view(), name='gestion_usuarios'),
    path('detalle_usuarios/id=<int:pk>/', detalle_usuarios, name='detalle_usuarios'),
    path('ascender_administrador/id=<int:pk>/', ascender_administrador, name='ascender_administrador'),
    path('descender_administrador/id=<int:pk>/', views.descender_administrador, name='descender_administrador'),
    path('desactivar_usuario/id=<int:pk>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('activar_usuario/id=<int:pk>/', views.activar_usuario, name='activar_usuario'),
    path('eliminar_usuario/id=<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('info_usuarios/', info_usuarios, name='info_usuarios'),
    
    # Activacion de correo electronico
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    # Cambio de contraseña con correo
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="identity/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="identity/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="identity/password_reset_complete.html"),name="password_reset_complete"),
    path('reset/invalid/', PasswordResetInvalidView.as_view(), name='password_reset_invalid'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
