from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))


def busca_potenciais_clientes(termos_pesquisa, cidades, pais, qnt_cliente_por_cidade):

    dados = []

    for i in range(len(cidades)):

        # Define the input for the Actor
        actor_input = {
            "searchStringsArray": termos_pesquisa,
            "locationQuery": f"{cidades[i]}, {pais}",
            "maxCrawledPlacesPerSearch": qnt_cliente_por_cidade[i],
            "language": "pt-BR",
        }

        # Run an Actor with an input
        try:
            finished_run = apify_client.actor('compass/crawler-google-places').call(run_input=actor_input)

            if finished_run.status != "SUCCEEDED":
                raise Exception(f"Actor run failed with status {finished_run.status} in city {cidades[i]}.")
            
            dataset_id = finished_run.default_dataset_id
            
            for item in apify_client.dataset(dataset_id).iterate_items():

                dados.append({
                    "Nome": item.get("title"),
                    "Telefone": item.get("phone"),
                    "Cidade pesquisada": cidades[i],
                    "Cidade": item.get("city"),
                    "Estado": item.get("state"),
                    "Categoria Principal": item.get("categoryName"),
                    "Categorias": ", ".join(item.get("categories", [])),
                    "Nota": item.get("totalScore"),
                    "Qtd. avaliações": item.get("reviewsCount"),
                    "Search String": item.get("searchString"),
                })

        except Exception as e:
            print("Erro na busca:", e)
            continue

    df = pd.DataFrame(dados)

    return df