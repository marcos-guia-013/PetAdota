# PetAdota

Projeto acadêmico desenvolvido em Python e Django para auxiliar na adoção de animais.

## Funcionalidades

- Cadastro, listagem, atualização e exclusão de animais.
- Cadastro e atualização de usuários.
- Cadastro e consulta de ofertas e pedidos de adoção.
- Filtragem de animais por espécie.

## Como executar no Linux

Na pasta que contém o arquivo `manage.py`, execute:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000/polls/ no navegador.

O banco SQLite é criado localmente pelas migrações. A pasta `venv` não faz parte do repositório.

## Estrutura

- `PetAdota/`: configurações do Django.
- `polls/`: modelos, views, rotas e templates.
- `diagramas/`: diagramas do trabalho.

Projeto destinado ao aprendizado e à execução local, não à produção.
