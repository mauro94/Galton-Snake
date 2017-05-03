# Correlation for Non-numerical values functions
# Patricio Sanchez A01191893
# Mauro Amarante A01191893

pool = {
  'money': {
    'data': ['cost', 'price', 'sale', 'discount']
  },

  'date': {
    'data': ['month', 'quarter', 'day', 'week', 'year', 'hour', 'minute', 'season', 'second']
  },

  'movement': {
    'data': ['mph', 'kmph', 'mps']
  },
  
  'distance': {
    'data': ['kilometers', 'meters', 'centimeters', 'yards', 'inches']
  }
}

def beginCheck(headers):
  totalSum = []

  for h in headers:
    word = cleanWord(h)
    temp = poolCheck(word)
    totalSum = list(map(lambda x,y : x + y, temp, totalSum))

  return totalSum

def poolCheck(word):
  # Counter for ocurrences in every category
  weight_mon = 0
  weight_date = 0
  weight_m = 0
  weight_dis = 0

  # Iterate through all categories looking for matches
  for w in pool['money']['data']:
    if w in word:
      weight_mon += 1

  for w in pool['date']['data']:
    if w in word:
      weight_date += 1

  for w in pool['movement']['data']:
    if w in word:
      weight_m += 1

  for w in pool['distance']['data']:
    if w in word:
      weight_dis += 1

  # Return all acumulated weights for word
  weight = [weight_mon, weight_date, weight_m, weight_dis]
  return weight


def cleanWord(word):
  # Standarize headers
  word.replace('_', ' ')
  word.replace('.', ' ')
  word.replace('-', ' ')
  word.lower()

