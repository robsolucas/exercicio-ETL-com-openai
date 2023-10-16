"""
[E] Extrair: Extrair os ID's de usuario e utilizar para enviar uma requisicao para a API e obter os dados de clientes.


[T] Transform: Criar uma mensagem a partir da integracao com o ChatGPT e a personalizacao a partir dos dados obtidos.


[L] Load: Envia a transformacao gerada de maneiroa personalizada, para o usuario a partir do ID
"""
from random import randint

import json, \
    pandas as pd, \
    requests, \
    openai


# EXTRACAO
# endereco da API
santanderapi_url = 'https://sdw-2023-prd.up.railway.app'

# dados que serao utilizados para a requisicao
dataframe = pd.read_csv('SantanderDevWeek.csv')

# ids de usuario
user_IDs = dataframe['Ids'].tolist()

# criando a funcao para fazer o get
def get_user(id):
    response = requests.get(f'{santanderapi_url}/users/{id}')
    if response.status_code == 200:
        return response.json()
    else:
        return None


users = [get_user(id=ID) for ID in user_IDs if get_user(id=ID) is not None]


# TRANSFORMACAO
# chave da api openai
open_ai_key = '~bla bla bla~'
openai.api_key = open_ai_key

# criando a funcao para personalizar a mensagem
def generate_dica(nome, tema):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Seja um especialista em marketing financeiro"},
            {"role": "user", "content": f"Entregue uma mensagem de conselho financeiro a ser exibida no login de aplicativo"
                                        f"da Santander, com o tema {tema} para o usuario {nome}, utilizando ate 200 caracteres."},
        ]
    )
    return completion.choices[0].message.content.strip('\"')


nome = users[0]['name']
tema = str(users[0]['features'][randint(0, 3)]['description'])
mensagem = generate_dica(nome, tema)


#LOAD
# vamos subir a atualizacao com um post
def update_user(user):
    response = requests.put(f"{santanderapi_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f'{user} update: {success}')

