import requests
import datetime
import smtplib
import time

MY_LONG = 18.709220
MY_LAT = 54.361810

p_mail = 'pythonmcpython@gmail.com'
p_password = 'jgqypgbliavtnwki'


def is_iss_overhead():
    response_iss = requests.get(url='http://api.open-notify.org/iss-now.json')
    response_iss.raise_for_status()
    data = response_iss.json()

    longitude = float(data['iss_position']['longitude'])
    latitude = float(data['iss_position']['latitude'])
    if MY_LONG - 5 <= longitude <= MY_LONG + 5 and MY_LAT - 5 <= latitude <= MY_LAT + 5:
        return True


def is_night():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0
    }
    response_sun = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response_sun.raise_for_status()
    data = response_sun.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    now = datetime.datetime.now().hour

    if now >= sunset or now <= sunrise:
            return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=p_mail, password=p_password)
            connection.sendmail(from_addr=p_mail, to_addrs='hejtuspl@gmail.com',
                                msg="Subject:Look up!\n\nThe ISS is close by and it's dark!")
            connection.close()
