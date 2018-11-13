from context import elastic, index

index_name = 'projects'
index.create_index(index_name)
if not elastic.client.indices.exists(index=index_name):
    raise(Exception(f"Index '{index_name}' does not exist."))

index_name = 'publications'
index.create_index(index_name)
if not elastic.client.indices.exists(index=index_name):
    raise(Exception(f"Index '{index_name}' does not exist."))

print("Test passed. Indicies created successfully.")
