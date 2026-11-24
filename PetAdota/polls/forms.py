
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Animal, Usuario, OfertaDoacao, PedidoDoacao


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            "especie",
            "porte",
            "data_nasc",
            "descricao",
            "adotado",
            "foto"
        ]
        widgets = {
            "data_nasc": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"}
            )
        }


class UsuarioForm(forms.ModelForm):
    cpf = forms.CharField(
        label="CPF",
        min_length=11,
        max_length=11,
        widget=forms.TextInput(attrs={
            "placeholder": "00000000000",
            "inputmode": "numeric"
        })
    )

    numero = forms.CharField(
        label="Telefone",
        max_length=15,
        widget=forms.TextInput(attrs={
            "placeholder": "(88) 90292-1832",
            "inputmode": "numeric"
        })
    )

    def clean_numero(self):
        numero = self.cleaned_data["numero"]
        return numero.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

    class Meta:
        model = Usuario
        fields = [
            "cpf",
            "nome",
            "numero",
            "email"
        ]


class OfertaDoacaoForm(forms.ModelForm):
    class Meta:
        model = OfertaDoacao
        fields = [
            "animal",
            "endereco",
            "descricao"
        ]


class PedidoDoacaoForm(forms.ModelForm):
    class Meta:
        model = PedidoDoacao
        fields = [
            "id_ofertaDoacao"
        ]


class CadastroForm(UserCreationForm):
    username = forms.CharField(
        label="Usuário",
        max_length=150
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2"
        ]

class AtualizarPedidoForm(forms.ModelForm):
    class Meta:
        model = PedidoDoacao
        fields = [
            "status_pedido"
        ]