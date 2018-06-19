def fixStateNames(x):
  x = x.lower()
  with open('./files/states.csv','r', encoding='utf-8-sig') as f:
    states = {}
    for line in f:
      name, abbrv = line.replace('\n','').split(',')
      states[abbrv.lower()] = (name.lower(), abbrv.lower())
  state, abbrv = states.get(x, [x, None])
  if abbrv:
    return abbrv.upper()
  else:
    for state, abbrv in states.values():
      if x == state:
        return abbrv.upper()
    else:
      raise(Exception)

test_cases = [
  'TX', # pass
  'tx', # pass
  'Texas', # pass
  'TEXAS', # pass
  'CU'] # fail
for x in test_cases:
  print(fixStateNames(x))

