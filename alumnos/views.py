from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import Alumno
from .forms import RegistroForm, AlumnoForm
from .utils import generar_pdf_alumno
import io

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Enviar email de bienvenida
            try:
                send_mail(
                    '¡Bienvenido al Sistema de Gestión de Alumnos!',
                    f'Hola {user.username},\n\nGracias por registrarte en nuestro sistema.\n\nYa puedes comenzar a gestionar tus alumnos.\n\nSaludos,\nEl equipo',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, '¡Registro exitoso! Te hemos enviado un correo de bienvenida.')
            except Exception as e:
                messages.warning(request, f'Registro exitoso, pero no se pudo enviar el correo: {str(e)}')
            
            return redirect('dashboard')
    else:
        form = RegistroForm()
    
    return render(request, 'alumnos/registro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'alumnos/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

@login_required
def dashboard_view(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})

@login_required
def crear_alumno_view(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, f'Alumno {alumno.nombre} creado exitosamente.')
            return redirect('dashboard')
    else:
        form = AlumnoForm()
    
    return render(request, 'alumnos/crear_alumno.html', {'form': form})

@login_required
def editar_alumno_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, f'Alumno {alumno.nombre} actualizado exitosamente.')
            return redirect('dashboard')
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'alumnos/editar_alumno.html', {'form': form, 'alumno': alumno})

@login_required
def eliminar_alumno_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        nombre = alumno.nombre
        alumno.delete()
        messages.success(request, f'Alumno {nombre} eliminado exitosamente.')
        return redirect('dashboard')
    
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})

@login_required
def enviar_pdf_alumno_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    # Generar PDF
    buffer = generar_pdf_alumno(alumno)
    
    # Enviar por correo
    try:
        email_destino = request.POST.get('email_destino', request.user.email)
        
        send_mail(
            subject=f'Información del Alumno: {alumno.nombre}',
            message=f'Adjunto encontrarás la información completa del alumno {alumno.nombre}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_destino],
            fail_silently=False,
            html_message=f'<p>Adjunto encontrarás la información completa del alumno <strong>{alumno.nombre}</strong>.</p>',
        )
        
        # Adjuntar PDF
        from django.core.mail import EmailMessage
        email = EmailMessage(
            subject=f'Información del Alumno: {alumno.nombre}',
            body=f'Adjunto encontrarás la información completa del alumno {alumno.nombre}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_destino],
        )
        email.attach(f'alumno_{alumno.dni}.pdf', buffer.getvalue(), 'application/pdf')
        email.send()
        
        messages.success(request, f'PDF enviado exitosamente a {email_destino}')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {str(e)}')
    
    return redirect('dashboard')

@login_required
def descargar_pdf_alumno_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    # Generar PDF
    buffer = generar_pdf_alumno(alumno)
    
    # Retornar como respuesta HTTP
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="alumno_{alumno.dni}.pdf"'
    
    return response