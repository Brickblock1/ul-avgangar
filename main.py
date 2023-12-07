from pyodide.http import pyfetch
from pyscript import document
import asyncio
import time


def combine_departure(departure):
    varstr = "output_departures_" + departure["area"]
    global test
    #test[varstr] = test[varstr] + line_info["name"] + suffix + " mot " + line_info["towards"] + "\navgår: "+ thing[11:-4]+ " UTC trafikslag: " + traffictype["Name"] + "\n"
    deviations = departure["deviations"]
    combined_deviations = ""
    for d in range (0, len(deviations)):
        deviation = deviations[d]
        combined_deviations = combined_deviations + deviation["title"] 
    test[varstr] = test[varstr] + line_info["name"] + " " + line_info["towards"] + "\n"+ thing[11:-4]+ " UTC " + str(combined_deviations) + "\n"

def write_departure():
    global response_dict
    areas = response_dict["areas"]
    for a in range (0, len(areas)):
        area = areas[a]
        id = "#_" + area["name"]
        output_div2 = document.querySelector(id)
        output_div2.innerText = test["output_departures_"+area["name"]]

response = await pyfetch(url="https://api.ul.se/api/v4/stop/" + "700600", method="GET")
response_dict = await response.json()

header_name = f" {response_dict['name']}"

departures = response_dict["departures"]
test = {
"output_departures_A": "",
"output_departures_B": "",
"output_departures_C": "",
"output_departures_D": "",
"output_departures_E": "",
"output_departures_F": "",
"output_departures_G": "",
"output_departures_J": "",
"output_departures_X": "",
"output_departures_A1": "",
"output_departures_A2": "",
"output_departures_A3": "",
"output_departures_A4": "",
"output_departures_A5": "",
"output_departures_B1": "",
"output_departures_B2": "",
"output_departures_B2a": "",
"output_departures_B3": "",
"output_departures_B4": "",
"output_departures_B5": "",
"output_departures_C1": "",
"output_departures_C2": "",
"output_departures_C3": "",
"output_departures_C4": "",
"output_departures_C5": "",
"output_departures_D1": "",
"output_departures_D2": "",
"output_departures_E1": "",
"output_departures_E2": "",
"output_departures_1a": "",
"output_departures_1b": "",
"output_departures_2a": "",
"output_departures_2b": "",
"output_departures_3": "",
"output_departures_4": "",
"output_departures_5": "",
"output_departures_6": "",
"output_departures_7a": "",
"output_departures_7b": "",
"output_departures_8a": "",
"output_departures_8b": "",
"output_departures_10": "",
}
for d in range (0, len(departures)):
    depature = departures[d]
    has_realtime = depature["hasRealTimeDepartureDeviation"] 
    if has_realtime == True:
        thing = str(depature["realTimeDepartureDateTime"])
    else:
        thing = str(depature["departureDateTime"])
    departure_time = time.strptime(str(thing), "%Y-%m-%dT%H:%M:%SZ") # 2023-11-16T16:47:00Z
    current_time = time.gmtime()
    if departure_time >= current_time:
        first_departure = departures[d]
        line_info = first_departure["line"]
        traffictype = line_info["trafficType"]
        if line_info["trainNo"] == 0:
            suffix = ":an"
        else:
            suffix = ""
        combine_departure(depature)
write_departure()
output_div = document.querySelector("#request_text")
output_div.innerText = header_name


#hide unused stopmarkers
areas = response_dict["areas"]
for a in range (0, len(areas)):
    area = areas[a]
    target = document.getElementById("hide_" + area["name"])
    target.style.display = "block"
