import sys
import time
from datetime import datetime
import json
from random import seed
from random import randint
import requests

input_file = "./greenhouse_sensor_data.csv"


url = "http://172.28.0.5:10200/contentListener"
header = {'Content-type': 'application/json'}

print("Default settings? [bool -> true / false]: ")
defaultInput = input()
defaultSettings = defaultInput != "false"

if defaultSettings:
    sensorNumber = 5
    averageTimeBetween = 1000
    makeDifferent = False

else:
    print("Number of different sensors [int]: ")
    sensorNumber = int(input())

    print(
        "Time between sends [int in milliseconds] (advised min is 10ms): ")
    averageTimeBetween = int(input())

    print(
        "Make them slightly different than \"real\" meassured data [bool -> true / false] (to avoid duplicates after long running): ")
    stringInput = input()
    makeDifferent = stringInput == "true"

    # print(str(makeDifferent))

seed(420)


while True:
    breakAgain = False
    # Waste first line with header info
    fh_input = open(input_file, "r")
    currentLine = fh_input.readline()

    while currentLine != '':
        if breakAgain:
            break

        # Do it for each sensor
        i = 1
        now = datetime.now()  # current date and time
        # old version
        # timestamp = now.strftime("%d-%m-%Y %H:%M:%S")  1994-11-05T13:15:30Z
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        while i <= sensorNumber:
            currentLine = fh_input.readline()
            parts = currentLine.split(',')

            if len(parts) < 5:
                breakAgain = True  # Not very pretty but i dont wanna refactor to a function like I should
                break

            sensorName = "sensor" + str(i)
            fertilizer_level = float(parts[1])
            light = float(parts[2])
            soil_moisture_percent = float(parts[3])
            air_temperature = float(parts[4].split(
                '\n')[0])  # To remove the newline

            # Randomize Part
            if makeDifferent:
                if randint(0, 1) == 0:
                    fertilizer_level = fertilizer_level + \
                        float(randint(0, 100)) / 100
                else:
                    fertilizer_level = fertilizer_level - \
                        float(randint(0, 100)) / 100
                    if fertilizer_level < 0:
                        fertilizer_level = 0

                if randint(0, 1) == 0:
                    light = light + float(randint(0, 100)) / 100
                else:
                    light = light - float(randint(0, 100)) / 1000
                    if light < 0:
                        light = 0

                if randint(0, 1) == 0:
                    soil_moisture_percent = soil_moisture_percent + \
                        float(randint(0, 100)) / 10
                    if soil_moisture_percent > 100:
                        soil_moisture_percent = 100
                else:
                    soil_moisture_percent = soil_moisture_percent - \
                        float(randint(0, 100)) / 50
                    if soil_moisture_percent < 0:
                        soil_moisture_percent = 0

                if randint(0, 1) == 0:
                    air_temperature = air_temperature + \
                        float(randint(0, 100)) / 10
                else:
                    air_temperature = air_temperature - \
                        float(randint(0, 100)) / 10

            # print(timestamp)
            sensorDataJson = {
                'name': f'{sensorName}',
                'time_measured': f'{timestamp}',
                'fertilizer': float("%.2f" % fertilizer_level),
                'light': float("%.2f" % light),
                'soil_moisture_percent': float("%.2f" % soil_moisture_percent),
                'air_temperature': float("%.2f" % air_temperature)
            }
            json_data = json.dumps(sensorDataJson)
            print(json_data)

            returnRequest = requests.post(url, data=json_data, headers=header)
            # print("Return from request: " + str(returnRequest))

            i = i + 1

        time.sleep(averageTimeBetween/1000)
