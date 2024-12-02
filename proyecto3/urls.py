"""
URL configuration for proyecto3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('presupuestos/', views.presupuestos_view, name='presupuestos'),
    path('transacciones/', views.transacciones_view, name='transacciones'),
    path('categorias/', views.categorias_view, name='categorias'),
    path('presupuestos/editar/<int:id>/', views.editar_presupuesto_view, name='editar_presupuesto'),
    path('presupuestos/eliminar/<int:id>/', views.eliminar_presupuesto_view, name='eliminar_presupuesto'),
    path('presupuestos/crear/', views.crear_presupuesto_view, name='crear_presupuesto'),
    path('transacciones/crear/', views.crear_transaccion_view, name='crear_transaccion'),
    path('categorias/crear/', views.crear_categoria_view, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria_view, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria_view, name='eliminar_categoria'),
    path('transacciones/editar/<int:id>/', views.editar_transaccion_view, name='editar_transaccion'),
    path('transacciones/eliminar/<int:id>/', views.eliminar_transaccion_view, name='eliminar_transaccion'),
]
