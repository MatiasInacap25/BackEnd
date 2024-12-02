from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Categoria, Transaccion, Presupuesto

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': 'Por favor ingresa un correo electrónico válido',
            'required': 'El correo electrónico es obligatorio'
        }
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'La contraseña es obligatoria'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages = {
            'invalid_login': 'Correo o contraseña incorrectos',
            'inactive': 'Esta cuenta está inactiva'
        }
        # Agregar placeholders a los campos
        self.fields['username'].widget.attrs['placeholder'] = 'Ingresa tu correo electrónico'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingresa tu contraseña'

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        error_messages = {
            'email': {
                'unique': 'Este correo electrónico ya está registrado.',
                'required': 'El correo electrónico es obligatorio.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de ayuda
        self.fields['password1'].help_text = 'Tu contraseña debe contener al menos 8 caracteres.'
        self.fields['password2'].help_text = 'Ingresa la misma contraseña para verificación.'
        
        # Eliminar los mensajes de ayuda adicionales
        self.fields['password1'].widget.attrs['help_text'] = None
        self.fields['password2'].widget.attrs['help_text'] = None
        
        # Mensajes de error personalizados
        self.error_messages = {
            'password_mismatch': 'Las contraseñas no coinciden.',
            'email': {
                'unique': 'Este correo electrónico ya está registrado.',
                'required': 'El correo electrónico es obligatorio.',
            },
        }

        # Etiquetas en español
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Usar la parte del email antes del @ como username
        user.username = self.cleaned_data['email'].split('@')[0]
        if commit:
            user.save()
        return user

class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de la categoría'
        })
    )

    class Meta:
        model = Categoria
        fields = ['nombre']

class TransaccionForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=[('Ingreso', 'Ingreso'), ('Gasto', 'Gasto')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    monto = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        })
    )
    
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción opcional'
        })
    )

    class Meta:
        model = Transaccion
        fields = ['tipo', 'categoria', 'monto', 'descripcion']

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['categoria', 'limite', 'periodo_inicio', 'periodo_fin']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'limite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'periodo_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'periodo_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }