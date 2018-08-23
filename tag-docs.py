from elastic.models import Project
from elastic import client, query

fields = ["title","abstract","notes", "TRID_INDEX_TERMS", "TRID_SUBJECT_AREAS"]

element_tags = [
  "deck",
  "joint",
  "bearing",
  "girder",
  "beam",
  "overlay",
  "wearing surface",
  "sealant",
  "sealer",
  "rebar",
  "reinforcement",
  "rebar coating"
  "jointless",
  "coating"
]

input_attribute_tags = [
  "design",
  "construction",
  "environment",
  "maintenance",
  "preservation",
  "materials",
  "live load"
]

performance_tags = [
  "cost",
  "functionality",
  "condition",
  "structural integrity",
  "structural condition",
  "serviceability",
  "service limit state",
  "strength limit state",
  "inspection"
]

def assign_tags(tags, index):

  for tag in tags:
    
    should = query.construct_bool_clause([tag], fields)
    q = query.boolean(should=should)
    r = query.run_query(index, q)
    hits = query.process_response(r)

    for id in hits:
      doc = Project.get(using=client, index=index, id=id)
      current_tags = list(doc.tags)
      current_tags.append(tag)
      current_tags_set = set(current_tags)
      doc.update(using=client,index=index,tags=list(current_tags_set))
      print(f'Doc ({id}): updated')

assign_tags(element_tags,'projects')
assign_tags(input_attribute_tags,'projects')
assign_tags(performance_tags,'projects')


