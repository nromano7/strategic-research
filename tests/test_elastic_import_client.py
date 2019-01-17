from context import elastic

if not elastic.client.ping():
    raise ValueError("Connection failed.")
else:
    print("Connection successful.")