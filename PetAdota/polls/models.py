from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Animal(models.Model):

    class Especie(models.TextChoices):
        GATO = "GAT", "Gato"
        CACHORRO = "CAC", "Cachorro"
        OUTRO = "OUT", "Outro"

    class Porte(models.TextChoices):
        PEQUENO = "P", "Pequeno"
        MEDIO = "M", "Médio"
        GRANDE = "G", "Grande"

    id_animal = models.AutoField(primary_key=True)
    especie = models.CharField(max_length=3, choices=Especie.choices)
    porte = models.CharField(max_length=1, choices=Porte.choices)
    data_nasc = models.DateField()
    descricao = models.TextField(max_length=100)
    adotado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_especie_display()} - {self.descricao}"

class Usuario(models.Model):
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message="O CPF deve estar no formato: 000.000.000-00"
    )
    telefone_regex = RegexValidator(regex=r'^\d{2} \d{5}-\d{4}$')
    
    id_usuario = models.AutoField(primary_key=True)
    cpf = models.CharField(
        max_length=14,
        validators=[cpf_validator],
        unique=True, 
        db_index=True,
        verbose_name="CPF"
    )
    nome = models.CharField(max_length=100)
    numero = models.CharField(validators=[telefone_regex], max_length=12, blank=False, null=False)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.nome

class OfertaDoacao(models.Model):
    id_ofertaDoacao = models.AutoField(primary_key=True)
    doador = models.ForeignKey(Usuario, on_delete=models.CASCADE) 
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)               
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=3, 
        choices=[('DIS', 'Disponível'), ('PRC', 'Em Processo'), ('ADT', 'Adotado')], 
        default='DIS'
    )

class PedidoDoacao(models.Model):

    class StatusPedido(models.TextChoices):
        PENDENTE = "PE", "Pendente"
        ACEITO = "AC", "Aceito"
        RECUSADO = "REC", "Recusado"

    idPedidoDoacao = models.AutoField(primary_key=True)
    id_ofertaDoacao = models.ForeignKey(
        OfertaDoacao,
        on_delete=models.CASCADE
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    data_pedido = models.DateTimeField(auto_now_add=True)
    status_pedido = models.CharField(
        max_length=3,
        choices=StatusPedido.choices,
        default=StatusPedido.PENDENTE
    )