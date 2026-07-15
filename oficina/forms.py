from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Peca, MaoDeObra, PecaEmFalta


class CadastroForm(UserCreationForm):
    """
    Formulário de cadastro de novo usuário.
    Além dos campos padrão (usuário/senha), pede o tipo (mecânico ou vendedor).
    O usuário criado começa com aprovado=False até alguém liberar no admin.
    """
    tipo = forms.ChoiceField(choices=PerfilUsuario.TIPO_CHOICES, label="Você é")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        usuario = super().save(commit=commit)
        if commit:
            PerfilUsuario.objects.create(
                usuario=usuario,
                tipo=self.cleaned_data['tipo'],
                aprovado=False,
            )
        return usuario


class PecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = ['nome', 'descricao', 'quantidade', 'preco']


class MaoDeObraForm(forms.ModelForm):
    class Meta:
        model = MaoDeObra
        fields = ['descricao', 'valor']


class PecaEmFaltaForm(forms.ModelForm):
    class Meta:
        model = PecaEmFalta
        fields = ['nome', 'quantidade_desejada']
