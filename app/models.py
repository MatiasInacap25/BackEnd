from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_email_verified = models.BooleanField(default=False)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Cantidad de dinero del usuario

    # Solución: Añadir related_name a grupos y permisos
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


# Modelo para categorías de transacciones
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Ahora las categorías son globales y únicas

    def __str__(self):
        return self.nombre

# Modelo para presupuestos (Budgets)
class Presupuesto(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='presupuestos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='presupuestos')
    limite = models.DecimalField(max_digits=12, decimal_places=2)  # Límite del presupuesto
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

# Modelo para transacciones financieras
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
