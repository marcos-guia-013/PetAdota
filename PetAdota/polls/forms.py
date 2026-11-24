from django import forms
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
            "doador",
            "animal",
            "endereco",
            "descricao",
            "status"
        ]


class PedidoDoacaoForm(forms.ModelForm):
    class Meta:
        model = PedidoDoacao
        fields = [
            "id_ofertaDoacao",
            "id_usuario",
            "status_pedido"
        ]