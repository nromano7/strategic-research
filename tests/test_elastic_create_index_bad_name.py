from context import index

try:
    index.create_index('test') # should raise an error
except Exception as e:
    print(e)
