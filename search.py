from whoosh.index import open_dir
from whoosh.qparser import QueryParser

# Função para buscar no índice
def search_index(term):
    ix = open_dir("indexdir")
    results_list = []
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(term)
        results = searcher.search(query)
        for result in results:
            results_list.append(result['path'])
    return results_list
