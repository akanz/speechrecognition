import requests,config

location = input('input the location ')

resp = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ location + config.api_key)

if resp.status_code == 200:
    data = [resp.json()]
    for i in data:
        weather = i['weather']

    for j in weather:
        main = j['main']
        print(main)
else:
    print('Error ' + str(resp.status_code) + ' occurred')