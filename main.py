import requests
import datetime as dt
import smtplib

MY_LAT = 12.971599
MY_LONG = 77.594566
MY_EMAIL ='xxxxxxxxx9@gmail.com'
PASSWORD = 'xxxxxxxxxx'


def iss_is_close():
    response_iss = requests.get("http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()
    longitude = float(data_iss['iss_position']['longitude'])
    latitude = float(data_iss['iss_position']['latitude'])
    #iss_position = (longitude, latitude)

    if MY_LAT - 5 <= latitude <= MY_LAT +5 and MY_LONG - 5 <= longitude <= MY_LONG + 5:
        return True
    else:
        return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data['results']['sunset'].split("T")[1].split(":")[0])
    now = dt.datetime.now()
    current_hours = now.hour

    if current_hours >= sunset or current_hours <= sunrise:
        return True
    else:
        return False


if is_dark() and iss_is_close():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg="Subject:IIS\n\n Look up")
