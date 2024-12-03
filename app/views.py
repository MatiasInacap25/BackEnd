from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  LoginForm, RegisterForm, CategoriaForm, TransaccionForm,PresupuestoForm
from .models import Presupuesto, Transaccion, Categoria

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            categorias_predeterminadas = ['Comida', 'Trabajo', 'Ropa', 'Transporte', 'Marakas']  # Ejemplo de categorías
            for nombre in categorias_predeterminadas:
                Categoria.objects.get_or_create(nombre=nombre)  # Crea la categoría si no existe
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegisterForm()
    return render(request, 'register.html',{'form':form})

@login_required()
def home(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    messages.success(request, '¡Hasta pronto!')
    return redirect('login')

@login_required
def presupuestos_view(request):
    presupuestos = Presupuesto.objects.filter(usuario=request.user)
    for presupuesto in presupuestos:
        presupuesto.porcentaje = presupuesto.porcentaje_usado()
        presupuesto.saldo_gastado = presupuesto.total_gastado()
    return render(request, 'presupuestos.html', {'presupuestos': presupuestos})

@login_required
def transacciones_view(request):
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'transacciones.html', {'transacciones': transacciones})

@login_required
def categorias_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})

@login_required
def crear_presupuesto_view(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.save()
            messages.success(request, 'Presupuesto creado exitosamente.')
            return redirect('presupuestos')
    else:
        form = PresupuestoForm()
    return render(request, 'crearPresupuestos.html', {'form': form})


@login_required
def crear_transaccion_view(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            
            # Actualizar el saldo del usuario
            if transaccion.tipo == 'Ingreso':
                request.user.saldo += transaccion.monto
            else:
                request.user.saldo -= transaccion.monto
            
            request.user.save()
            transaccion.save()
            
            messages.success(request, 'Transacción registrada exitosamente.')
            return redirect('transacciones')
    else:
        form = TransaccionForm()
    
    return render(request, 'crearTransacciones.html', {'form': form})

@login_required
def crear_categoria_view(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categorias')
    else:
        form = CategoriaForm()
    return render(request, 'crearCategorias.html', {'form': form})

@login_required
def editar_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editarCategoria.html', {'form': form})

@login_required
def eliminar_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
    return redirect('categorias')

@login_required
def editar_transaccion_view(request, id):
    transaccion = get_object_or_404(Transaccion, id=id, usuario=request.user)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            # Revertir el efecto de la transacción anterior en el saldo
            if transaccion.tipo == 'Ingreso':
                request.user.saldo -= transaccion.monto
            else:
                request.user.saldo += transaccion.monto
                
            # Aplicar la nueva transacción
            nueva_transaccion = form.save(commit=False)
            if nueva_transaccion.tipo == 'Ingreso':
                request.user.saldo += nueva_transaccion.monto
            else:
                request.user.saldo -= nueva_transaccion.monto
            
            request.user.save()
            nueva_transaccion.save()
            messages.success(request, 'Transacción actualizada exitosamente.')
            return redirect('transacciones')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'editarTransaccion.html', {'form': form})

@login_required
def eliminar_transaccion_view(request, id):
    transaccion = get_object_or_404(Transaccion, id=id, usuario=request.user)
    if request.method == 'POST':
        # Actualizar saldo antes de eliminar
        if transaccion.tipo == 'Ingreso':
            request.user.saldo -= transaccion.monto
        else:
            request.user.saldo += transaccion.monto
        request.user.save()
        
        transaccion.delete()
        messages.success(request, 'Transacción eliminada exitosamente.')
    return redirect('transacciones')

@login_required
def editar_presupuesto_view(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id, usuario=request.user)
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presupuesto actualizado exitosamente.')
            return redirect('presupuestos')
    else:
        form = PresupuestoForm(instance=presupuesto)
    return render(request, 'editarPresupuesto.html', {'form': form, 'presupuesto': presupuesto})

@login_required
def eliminar_presupuesto_view(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id, usuario=request.user)
    
    if request.method == "POST":
        presupuesto.delete()
        messages.success(request, "Presupuesto eliminado exitosamente.")
        return redirect('presupuestos')

    return render(request, 'eliminarPresupuesto.html', {'presupuesto': presupuesto})