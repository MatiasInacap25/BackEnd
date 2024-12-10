from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import requests

paises = ["USD", "EUR", "ARS", "BRL"]
url = 'https://v6.exchangerate-api.com/v6/9f92a658f32a5c886cbf89af/pair/CLP/X/monto'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_email_verified = models.BooleanField(default=False)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  

    
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
        help_text="Los grupos a los que pertenece este usuario.",
        verbose_name="grupos",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
        help_text="Permisos específicos para este usuario.",
        verbose_name="permisos de usuario",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def conversion_saldo(self):
        conversiones = {}
        try:
            for pais in paises:
                response = requests.get(url.replace('X', pais).replace('monto', str(self.saldo)), timeout=5)
                data = response.json()
                conversiones[pais] = data.get('conversion_result', 0)
            return conversiones
        except Exception as e:
            print(f"Error en la conversión: {str(e)}")
            return None

    def __str__(self):
        return self.email


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.nombre


class Presupuesto(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='presupuestos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='presupuestos')
    limite = models.DecimalField(max_digits=12, decimal_places=2)  
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()

    def __str__(self):
        return f"Presupuesto {self.categoria.nombre}: {self.limite}"

    def porcentaje_usado(self):
        gastos = self.categoria.transacciones.filter(
            usuario=self.usuario,
            tipo='Gasto',
            fecha__range=[self.periodo_inicio, self.periodo_fin]
        ).aggregate(total=models.Sum('monto'))['total'] or 0
        
        if self.limite > 0:
            return min(round((gastos / self.limite) * 100), 100)
        return 0

    def total_gastado(self):
        return self.categoria.transacciones.filter(
            usuario=self.usuario,
            tipo='Gasto',
            fecha__range=[self.periodo_inicio, self.periodo_fin]
        ).aggregate(total=models.Sum('monto'))['total'] or 0


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto'),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transacciones')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='transacciones')
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo}: {self.monto} ({self.categoria})"
