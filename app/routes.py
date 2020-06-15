from app import app
import requests

all_data = requests.get('https://api.covid19api.com/summary').json()
all_countries = []
all_countries_data = dict()
for country in all_data['Countries']:
    countryName = ""
    if '(' in country['Country']:
        countryName = country['Country'][:country['Country'].index('(')].rstrip()
    else:
        countryName = country['Country']
    all_countries.append(countryName)
    all_countries_data[countryName] = {'confirmed': country['TotalConfirmed'],
                                       'recovered': country['TotalRecovered'],
                                       'deaths': country['TotalDeaths'],
                                       'todayConfirmed': country['NewConfirmed'],
                                       'todayRecovered': country['NewRecovered'],
                                       'todayDeaths': country['NewDeaths']}

states_url = 'https://api.covidindiatracker.com/state_data.json'
all_states_data = dict()
all_states = []
for state in requests.get(states_url).json():
    stateName = ""
    if '(' in state['state']:
        stateName = state['state'][:state['state'].index('(')].rstrip()
    else:
        stateName = state['state']
    all_states.append(stateName)
    all_states_data[stateName] = {'confirmed': state['confirmed'],
                                  'recovered': state['recovered'],
                                  'deaths': state['deaths'],
                                  'active': state['active']}
all_states.sort()
all_countries.sort()

@app.route('/countries')
def countries():
    return {'countries': all_countries}


@app.route('/country/<name>')
def country_data(name):
    result = requests.get('https://api.covid19api.com/dayone/country/' + name).json()
    result = result[-20:]
    data = dict()
    confirmed = []
    deaths = []
    recovered = []
    active = []
    for countryName in result:
        confirmed.append(countryName['Confirmed'])
        deaths.append(countryName['Deaths'])
        recovered.append(countryName['Recovered'])
        active.append(countryName['Active'])
    data['confirmedData'] = confirmed
    data['deathsData'] = deaths
    data['recoveredData'] = recovered
    data['activeData'] = active
    data['confirmed'] = all_countries_data[name]['confirmed']
    data['recovered'] = all_countries_data[name]['recovered']
    data['deaths'] = all_countries_data[name]['deaths']
    data['active'] = active[-1]
    data['todayConfirmed'] = all_countries_data[name]['todayConfirmed']
    data['todayRecovered'] = all_countries_data[name]['todayRecovered']
    data['todayDeaths'] = all_countries_data[name]['todayDeaths']
    return data


@app.route('/states')
def states():
    return {'states': all_states}


@app.route('/state/<name>')
def state_data(name):
    return {'confirmed': all_states_data[name]['confirmed'],
            'recovered': all_states_data[name]['recovered'],
            'deaths': all_states_data[name]['deaths'],
            'active': all_states_data[name]['active']}
