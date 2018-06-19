from geopy import Nominatim
import json

geolocator = Nominatim()

with open('./files/states.csv','r', encoding='utf-8-sig') as f:
  states = {}
  for line in f:
    state, abbrv = line.strip('\n').replace('\n','').split(',')
    loc = geolocator.geocode(state)
    latitude = loc.latitude
    longitude = loc.longitude
    address = loc.address
    country = address.split(',')[-1]

    # save with abbreviation as key
    states[abbrv] = {
      'abbrv':abbrv,
      'full':state,
      'country':country,
      'latitude':latitude,
      'longitude':longitude,
    }

    # save with full name as key
    states[state] = {
      'abbrv':abbrv,
      'full':state,
      'country':country,
      'latitude':latitude,
      'longitude':longitude,
    }

with open('./files/statesGeo.json','w') as f:
  json.dump(states,f)
