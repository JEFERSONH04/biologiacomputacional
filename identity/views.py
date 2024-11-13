from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from identity.models import AdditionalUserInfoForm, Tipografias
from BiologiaComputacional.forms import UsuarioForm, RegisterCustomForm, ProfileForm, ProfileAdditionalInfo, Tipografias
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import forms
import re
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.views.generic import TemplateView
from django.http.response import JsonResponse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

# Create your views here.

# Logica para mostrar un profesional

@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    template_name = "identity/profile.html"


    def get(self, request, *args, **kwargs):
        user = request.user
        # Intenta obtener la información adicional del usuario
        try:
            additional_info = ProfileAdditionalInfo.objects.get(user=user)
        except ProfileAdditionalInfo.DoesNotExist:
            # Si no existe, crea una nueva instancia
            additional_info = ProfileAdditionalInfo(user=user)
            additional_info.save()

        usuario_form = UsuarioForm(instance=user)
        additional_info_form = AdditionalUserInfoForm(instance=additional_info)
        return render(request, self.template_name, {'usuario_form': usuario_form, 'additional_info_form': additional_info_form})

    def post(self, request, *args, **kwargs):
        user = request.user

        # Intenta obtener la información adicional del usuario
        try:
            additional_info = ProfileAdditionalInfo.objects.get(user=user)
        except ProfileAdditionalInfo.DoesNotExist:
            # Si no existe, crea una nueva instancia
            additional_info = ProfileAdditionalInfo(user=user)
            additional_info.save()

        usuario_form = UsuarioForm(request.POST, instance=user)
        additional_info_form = AdditionalUserInfoForm(
            request.POST, request.FILES, instance=additional_info)

        if usuario_form.is_valid() and additional_info_form.is_valid():
            phone_number = additional_info_form.cleaned_data['phone_number']
            first_name = usuario_form.cleaned_data['first_name']
            last_name = usuario_form.cleaned_data['last_name']
            email = usuario_form.cleaned_data['email']

            if not phone_number:
                messages.error(
                    request, 'El campo Teléfono no puede estar vacío.')
            elif not phone_number.isdigit():
                messages.error(
                    request, 'El número de teléfono solo debe contener dígitos.')
            elif len(first_name) < 3:
                messages.error(
                    request, 'El nombre debe tener al menos 3 caracteres.')
            elif len(last_name) < 3:
                messages.error(
                    request, 'El apellido debe tener al menos 3 caracteres.')

            else:
                try:
                    validate_email(email)
                except ValidationError:
                    messages.error(
                        request, 'Ingrese una dirección de correo electrónico válida.')
                    return redirect('perfil')

                usuario_form.save()
                additional_info_form.save()
                messages.success(request, 'Información actualizada con éxito.')
        else:
            print("Errores de usuario_form:", usuario_form.errors)
            print("Errores de additional_info_form:",
                  additional_info_form.errors)
            messages.error(request, 'Error al actualizar la información.')

        return redirect('perfil')
    
    


# Logica para registrar un usuario
def register(request):
    if request.user.is_authenticated:  
        return redirect('inicio')



    if request.method == 'POST':
        user_form = RegisterCustomForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
              


        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Generar token de verificación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Crear enlace de verificación
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta'
            message = render_to_string('identity/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })

            # Enviar correo de verificación
            send_mail(
                mail_subject,
                message,
                'sinfoniadefragancias@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return render(request, 'identity/look_email.html')
        else:
            # Mostrar mensajes de error
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        user_form = RegisterCustomForm()
        profile_form = ProfileForm()

    return render(request, 'identity/register.html', {
        'form': user_form,
        'profile_form': profile_form,
        'messages': messages.get_messages(request),
    })

# Logica para cerrar sesion


def user_logout(request):

    logout(request)

    return redirect('inicio')

# Validaciones para el formulario Login


User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        errors = []

        if not re.match(r'^\w+$', username):
            errors.append(
                '• El nombre de usuario no debe contener caracteres especiales.')

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                errors.append(
                    '• Usuario en problemas, comuníquese con nosotros.')

        except User.DoesNotExist:
            errors.append('• El nombre de usuario no existe.')

        if errors:
            raise forms.ValidationError(errors)

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        errors = []

        if len(password) < 8:
            errors.append('• La contraseña debe tener al menos 8 caracteres.')

        if not re.search(r'[a-z]', password):
            errors.append(
                '• La contraseña debe contener al menos una letra minúscula.')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return password  # Evitamos verificar la contraseña si el usuario no existe

        if user.check_password(password):
            return password
        else:
            errors.append('• La contraseña no coincide con el usuario.')
            raise forms.ValidationError(errors)

# Logica formulario login


def signin(request):
    if request.user.is_authenticated:

        return redirect('inicio')
    
    messages_list = []
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)


        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if 'remember_me' in request.POST:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

                return redirect('inicio')

            else:
                messages_list.append(
                    "Nombre de usuario o contraseña incorrectos.")
        else:
            messages_list.append(
                "Por favor, corrija los errores en el formulario.")

        return render(request, 'identity/signin.html', {'form': form, 'messages': messages_list})
    else:
        return render(request, 'identity/signin.html', {'form': CustomAuthenticationForm()})

# Cambiar contraseña de usuario con sesion iniciada


class ProfilePasswordChangeView(PasswordChangeView):

    template_name = "identity/change_password.html"
    success_url = reverse_lazy('cambio_contrasena')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_changed'] = self.request.session.get(
            'password_changed', False)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Cambio de contraseña exitoso')
        update_session_auth_hash(self.request, form.user)
        self.request.session['password_changed'] = True
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'No se pudo cambiar la contraseña')
        return super().form_invalid(form)


# Cambiar contraseña de usuario sin sesion iniciada
UserModel = get_user_model()


def password_reset_confirm(request, uidb64, token):
    # Decodificar el uid y verificar si es válido
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    # Verificar si el token es válido
    if user is not None and default_token_generator.check_token(user, token):
        # Si el usuario y el token son válidos, procesar el formulario
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'identity/password_reset_confirm.html', {'form': form})
    else:
        # Si el usuario o el token no son válidos, redireccionar a una página de error o mostrar un mensaje
        return redirect('password_reset_invalid')


class PasswordResetInvalidView(TemplateView):

    template_name = "identity/password_reset_invalid.html"


@method_decorator(login_required, name='dispatch')
class ManageUsersView(TemplateView):

    template_name = "identity/manage_users.html"


# Metodos para admin o staff
def is_superuser(user):

    return user.is_superuser


def is_staff(user):

    return user.is_staff


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_staff_or_superuser)
def info_usuarios(request):
    info_users = list(User.objects.values())
    data = {'info_users': info_users}
    return JsonResponse(data, safe=False)


@user_passes_test(is_staff_or_superuser)
def detalle_usuarios(request, pk):
    usuarios = get_object_or_404(User, pk=pk)
    usuarios_adicional_info = get_object_or_404(
        ProfileAdditionalInfo, user=usuarios)
    return render(request, 'identity/detalle_usuarios.html', {'usuarios': usuarios, 'usuarios_adicional_info': usuarios_adicional_info})


@user_passes_test(is_superuser)
def ascender_administrador(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_staff = True
    usuario.save()

    messages.success(
        request, f"El usuario {usuario.username} ha sido ascendido a Administrador.")

    return redirect('detalle_usuarios', pk=pk)


@user_passes_test(is_superuser)
def descender_administrador(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_staff = False
    usuario.save()

    messages.success(
        request, f"El usuario {usuario.username} ha sido descendido a Estudiante.")

    return redirect('detalle_usuarios', pk=pk)


@user_passes_test(is_staff_or_superuser)
def desactivar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.user.is_superuser or (request.user.is_staff and not usuario.is_staff):
        usuario.is_active = False
        usuario.save()
        messages.success(
            request, f"El usuario {usuario.username} ha sido desactivado correctamente.")
    else:
        messages.error(
            request, f"Imposible desactivar un usuario del mismo rango.")
    return redirect('detalle_usuarios', pk=pk)


@user_passes_test(is_staff_or_superuser)
def activar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = True
    usuario.save()

    messages.success(
        request, f"El usuario {usuario.username} ha sido activado correctamente.")

    return redirect('detalle_usuarios', pk=pk)


@user_passes_test(is_superuser)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.delete()

    messages.success(
        request, f"El usuario {usuario.username} ha sido eliminado correctamente.")

    return redirect('gestion_usuarios')

# Activacion de cuentas por correo


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, 'identity/activation_success.html')
        else:
            return render(request, 'identity/activation_invalid.html')
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return render(request, 'identity/activation_invalid.html')
