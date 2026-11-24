# 
from django.db import migrations


def normalizar_cpf(apps, schema_editor):
    Usuario = apps.get_model("polls", "Usuario")
    usuarios = Usuario.objects.using(schema_editor.connection.alias)
    cpfs = []

    for usuario in usuarios.all():
        cpf = usuario.cpf.replace(".", "").replace("-", "")

        if len(cpf) != 11 or not cpf.isascii() or not cpf.isdigit():
            raise ValueError("Existe um CPF inválido no banco.")

        if cpf in cpfs:
            raise ValueError("Existem CPFs duplicados no banco.")

        cpfs.append(cpf)

    for usuario in usuarios.all():
        usuario.cpf = usuario.cpf.replace(".", "").replace("-", "")
        usuario.save(update_fields=["cpf"])


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_usuario_cpf_alter_usuario_numero'),
    ]

    operations = [
        migrations.RunPython(normalizar_cpf),
    ]
