# Casa-Pau-dos-Ferros-backend

## Sobre
Este projeto é referente a disciplina de Engenharia de Software da UTFPR e tem como objetivo implementar funcionalidades básicas de um marketplace e 2 testes unitários sobre estas funcionalidades básicas

## Setup inicial
### Pré-requisitos
[Python](https://www.python.org/downloads/)
### Requisitos

1. Criar ambiente virtual
```
python3 -m venv .venv
```

2. Ativar ambiente virtual
```
source .venv/bin/activate
```

3. Instalar requerimentos
```
pip install -r requirements.txt
```


## Subindo o backend
1. Caso o ambiente virtual não esteja ativo, ativá-lo
```
source .venv/bin/activate
```

2. Subir o servidor django
```
python manage.py runserver
```

3. Caso a porta padrão (`8000`) já esteja ocupada
```
python manage.py runserver <porta>
```

## Tecnologias utilizadas
- [Python](https://www.python.org/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Sqlite](https://www.sqlite.org/)
