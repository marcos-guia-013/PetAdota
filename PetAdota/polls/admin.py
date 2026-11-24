from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Animal, Usuario, OfertaDoacao, PedidoDoacao


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        "id_animal",
        "especie",
        "porte",
        "data_nasc",
        "adotado",
    )

    list_filter = (
        "especie",
        "porte",
        "adotado",
    )

    search_fields = (
        "descricao",
    )

    ordering = ("id_animal",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id_usuario",
        "nome",
        "cpf",
        "numero",
        "email",
    )

    search_fields = (
        "nome",
        "cpf",
        "email",
    )

    ordering = ("nome",)


@admin.register(OfertaDoacao)
class OfertaDoacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id_ofertaDoacao",
        "doador",
        "animal",
        "endereco",
        "data_criacao",
        "status",
    )

    list_filter = (
        "status",
        "data_criacao",
    )

    search_fields = (
        "doador__nome",
        "animal__descricao",
        "endereco",
    )

    ordering = ("-data_criacao",)


@admin.register(PedidoDoacao)
class PedidoDoacaoAdmin(admin.ModelAdmin):
    list_display = (
        "idPedidoDoacao",
        "id_ofertaDoacao",
        "id_usuario",
        "data_pedido",
        "status_pedido",
    )

    list_filter = (
        "status_pedido",
        "data_pedido",
    )

    search_fields = (
        "id_usuario__nome",
        "id_ofertaDoacao__doador__nome",
        "id_ofertaDoacao__animal__descricao",
    )

    ordering = ("-data_pedido",)
