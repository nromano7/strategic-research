from context import index, PROJECT_FILES_PATH

index.index_documents("projects", PROJECT_FILES_PATH, 
    verbose=False, testing=True)

index.index_documents("publications", PROJECT_FILES_PATH, 
    verbose=False, testing=True)


print("Test passed.")