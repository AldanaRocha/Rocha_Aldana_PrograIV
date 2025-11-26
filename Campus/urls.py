
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from alumnos import views as alumnos_views
from scrapper import views as scraper_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('', alumnos_views.login_view, name='login'),
    path('registro/', alumnos_views.registro_view, name='registro'),
    path('logout/', alumnos_views.logout_view, name='logout'),
    
    # Dashboard y gestión de alumnos
    path('dashboard/', alumnos_views.dashboard_view, name='dashboard'),
    path('alumno/crear/', alumnos_views.crear_alumno_view, name='crear_alumno'),
    path('alumno/<int:pk>/editar/', alumnos_views.editar_alumno_view, name='editar_alumno'),
    path('alumno/<int:pk>/eliminar/', alumnos_views.eliminar_alumno_view, name='eliminar_alumno'),
    path('alumno/<int:pk>/enviar-pdf/', alumnos_views.enviar_pdf_alumno_view, name='enviar_pdf_alumno'),
    path('alumno/<int:pk>/descargar-pdf/', alumnos_views.descargar_pdf_alumno_view, name='descargar_pdf_alumno'),
    
    # Scraper
    path('scraper/', scraper_views.scraper_view, name='scraper'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)