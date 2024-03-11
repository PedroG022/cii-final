import os.path
import pickle
from collections import Counter

import pandas as pd

with open(os.path.join(os.getcwd(), 'modelo.pkl'), 'rb') as model_file:
    print('Reading model...')
    kprot: pd.DataFrame = pickle.load(model_file)


# Encontra o cluster em que o livro selecionado é mais encontrado, em questão
# de reviews.
def get_target_cluster(tabela, isbn):
    entries = tabela[tabela['isbn'] == isbn]

    # Linhas com os nomes dos clusters
    cluster_identificators = entries['Cluster']

    # Contagem de quantas vezes o livro selecionado aparece nos clusters
    # assim podemos verificar em qual cluster ele mais apareceu
    appearence_list = [cluster for cluster in cluster_identificators]

    # ISBN não encontrado
    if len(appearence_list) == 0:
        raise Exception('Book not found in the database')

    # Lista única de clusters onde ele aparece
    unique_items = pd.unique(appearence_list)

    # Vê em que cluster o livro mais apareceu
    most_common = Counter(appearence_list).most_common(1)[0][0]

    return most_common


# Obtém 10 entradas presentes no mesmo cluster que o livro selecionado,
# removendo duplicatas e o próprio livro. Além disso, as entradas são
# ordenadas de acordo com a nota.
def get_top(table, cluster_name, target_isbn):
    # Entradas do cluster
    cluster_entries = table[table['Cluster'] == cluster_name]

    # Entradas que não são o livro escolhido
    different_entries = cluster_entries[cluster_entries['isbn'] != target_isbn]

    # Remoção de entradas duplicadas, ao agrupar por isbn e selecionar apenas
    # o primeiro de cada grupo
    no_duplicates = different_entries.groupby('isbn').apply(lambda x: x.head(1))

    # Ordenar de acordo com a nota
    ordered = no_duplicates.sort_values(by='nota', ascending=False)

    # Obter apenas os ISBNS
    isbns = [isbn for isbn in ordered.isbn]

    if len(ordered) < 10:
        raise Exception('The cluster that was found does not have enough entries!')

    # Amostra aleatória
    # recommended = random.sample(isbns, 10)
    recommended = isbns[0:10]

    return recommended


def get_recommendations(book_isbn):
    most_common = get_target_cluster(kprot, book_isbn)
    return get_top(kprot, most_common, book_isbn)
