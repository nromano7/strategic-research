from elastic import query
import json

allStatus = ['Active', 'Completed', 'Programmed', 'Proposed']
index = "projects"

tag = "all"
element_tag = "untreated_decks"

q = query.get_query(tag, {"record_set": element_tag}, index)
s = query.run_query(index, q)

res={}
res['total'] = s.count()
for status in allStatus:
    res[status.lower()] = s.filter("match",status=status).count()

print(json.dumps(res, indent=2))