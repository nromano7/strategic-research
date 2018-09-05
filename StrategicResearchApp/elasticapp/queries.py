def get_query(name):

  construction_quality = {
    "bool": {
      "must": [
        {
          "bool": {
            "should": [
              {"match": {"title":"construction"}},
              {"match": {"abstract":"construction"}}
            ]
          }
        }
      ],
      "should": [
        {"match":{"title":"quality"}},
        {"match":{"abstract":"quality"}},
        {"match":{"title.bigram":"construction quality"}},
        {"match":{"abstract.bigram":"construction quality"}}
      ]
    }
  }

  design_and_details = {
    "bool":{
      "must":[],
      "should":[],
      "must_not":[]
    }
  }

  queries = dict(
    construction_quality=construction_quality,
  )

  return queries.get(name)
