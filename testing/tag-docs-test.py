from elastic.models import Project
from elastic import client, query

index = 'projects'
fields = ["title","abstract","notes"]

tags = ["deck"]

for tag in tags:
  
  should = query.construct_bool_clause([tag], fields)
  q = query.boolean(should=should)
  r = query.run_query(index, q)
  hits = query.process_response(r)

  for id in hits:
    doc = Project.get(using=client, index=index, id=id)
    tags = list(doc.tags)
    tags.append(tag)
    tag_set = set(tags)
    doc.update(using=client,index=index,tags=list(tag_set))
    print(f'Doc ({id}): updated')

