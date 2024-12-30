import googlemaps
import requests
import time
import pandas as pd

# Configurar API Key do Google Maps
gmaps = googlemaps.Client(key='Sua API Key') #Acessar o site https://console.cloud.google.com e Cria sua API Key!!!

# Função para obter as cidades do estado de SP usando a API do IBGE
def obter_cidades_por_estado(sigla_estado):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla_estado}/municipios"
    response = requests.get(url)
    if response.status_code == 200:
        municipios = response.json()    
        # Retornar apenas os nomes das cidades
        return [municipio["nome"] for municipio in municipios]
    else:
        print(f"Erro ao acessar a API do IBGE para o estado {sigla_estado}.")
        return []

# Configurar o estado
sigla_estado = "SP" #Sigla do Estado
capital = "Palmas" #Capital do Estado

# Obter as cidades do estado
cidades = obter_cidades_por_estado(sigla_estado)

# Lista para armazenar os resultados
distancias = []

print(f"Iniciando consultas para o estado {sigla_estado} ({capital})...")

for cidade in cidades:
    try:
        # Consultar a distância da capital para a cidade
        resultado = gmaps.distance_matrix(origins=capital, destinations=f"{cidade}, {sigla_estado}", mode="driving")
        distancia = resultado['rows'][0]['elements'][0]['distance']['text']
        distancias.append({"Origem": capital, "Destino": cidade, "Distância": distancia})
        print(f"{capital} > {cidade}: {distancia}")
        time.sleep(0.2)  # Intervalo entre consultas
    except Exception as e:
        distancias.append({"Origem": capital, "Destino": cidade, "Distância": f"ERRO ({e})"})
        print(f"Erro ao consultar {cidade}: {e}")
