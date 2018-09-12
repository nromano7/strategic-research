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
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title":"design"}},
              {"match": {"abstract":"design"}}
            ]
          }
        }
      ],
      "should":[],
      "must_not":[]
    }
  }

  material_specifications = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title":"materials"}},
              {"match": {"abstract":"materials"}}
            ]
          }
        }
      ],
      "should":[
        {"match": {"title.bigram":"material specifications"}},
        {"match": {"abstract.bigram":"material specifications"}}
      ],
      "must_not":[]
    }
  }

  live_load = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title.bigram":"live load"}},
              {"match": {"abstract.bigram":"live load"}}
            ]
          }
        }
      ],
      "should":[],
      "must_not":[]
    }
  }

  environment = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title":"environment"}},
              {"match": {"abstract":"environment"}}
            ]
          }
        }
      ],
      "should":[],
      "must_not":[]
    }
  }

  maintenance_and_preservation = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title":"maintenance"}},
              {"match": {"abstract":"maintenance"}},
              {"match": {"title":"preservation"}},
              {"match": {"abstract":"preservation"}}
            ]
          }
        }
      ],
      "should":[
        {"match": {"title.bigram":"maintenance and preservation"}},
        {"match": {"abstract.bigram":"maintenance and preservation"}}
      ],
      "must_not":[]
    }
  }

  structural_integrity = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title.bigram":"structural integrity"}},
              {"match": {"abstract.bigram":"structural integrity"}}
            ]
          }
        }
      ],
      "should":[],
      "must_not":[]
    }
  }

  structural_condition = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title.bigram":"structural condition"}},
              {"match": {"abstract.bigram":"structural condition"}}
            ]
          }
        }
      ],
      "should":[],
      "must_not":[]
    }
  }

  functionality = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title":"functionality"}},
              {"match": {"abstract":"functionality"}}
            ]
          }
        }
      ],
      "should":[],
      "must_not":[]
    }
  }

  cost = {
    "bool":{
      "must":[
        {
          "bool": {
            "should": [
              {"match": {"title":"cost"}},
              {"match": {"abstract":"cost"}}
            ]
          }
        }
      ],
      "should":[],
      "must_not":[]
    }
  }

  queries = dict(
    construction_quality=construction_quality,
    design_and_details=design_and_details,
    material_specifications=material_specifications,
    live_load=live_load,
    environment=environment,
    maintenance_and_preservation=maintenance_and_preservation,
    structural_integrity=structural_integrity,
    structural_condition=structural_condition,
    functionality=functionality,
    cost=cost
  )

  return queries.get(name)
