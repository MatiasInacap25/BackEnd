from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

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

        