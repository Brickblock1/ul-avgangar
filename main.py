from pyodide.http import pyfetch
from pyscript import document
from datetime import datetime, timedelta
import asyncio


def combine_departure(departure):
    varstr = "output_departures_" + departure["area"]
    global test
    #test[varstr] = test[varstr] + line_info["name"] + suffix + " mot " + line_info["towards"] + "\navgår: "+ thing[11:-4]+ " UTC trafikslag: " + traffictype["Name"] + "\n"
    deviations = departure["deviations"]
    combined_deviations = ""
    for d in range (0, len(deviations)):
        deviation = deviations[d]
        combined_deviations = combined_deviations + deviation["title"] 
    test[varstr] = test[varstr] + line_info["name"] + " " + line_info["towards"] + "\n"+ str(scheduled_a)[11:-3] + " " + shown_realtime + " " + str(combined_deviations) + "\n"

def write_departure():
    global response_dict
    areas = response_dict["areas"]
    for a in range (0, len(areas)):
        area = areas[a]
        id = "#_" + area["name"]
        output_div2 = document.querySelector(id)
        output_div2.innerText = test["output_departures_"+area["name"]]

def write_info():
    global response_dict
    zone = response_dict["zone"]
    info_div = document.querySelector("#_Info")
    info_div.innerText = "Zon: " + zone["name"] + "\nTid: " + str(datetime.today())[11:-10]

config_hidden = False
stop = "700600"

async def onclick(event):
    global stop
    areas = response_dict["areas"]
    for a in range (0, len(areas)):
        area = areas[a]
        target = document.getElementById(area["name"])
        target.style.display = "none"
    input_text = document.querySelector("#input")
    stop = input_text.value
    await callapi()
    create_divs()
    unhide_divs(1)
    toggle_config(1)
    

async def callapi():
    global response_dict
    response = await pyfetch(url="https://api.ul.se/api/v4/stop/" + stop, method="GET")
    response_dict = await response.json()

def unhide_divs(event):
    areas = response_dict["areas"]
    for a in range (0, len(areas)):
        area = areas[a]
        target = document.getElementById(area["name"])
        target.style.display = "block"
    target = document.getElementById("hide_Info")
    target.style.display = "block"

def create_divs():
    areas = response_dict["areas"]
    for a in range (0, len(areas)):
        area = areas[a]
        if None == document.getElementById(area["name"]):
            div = document.createElement('div')
            div.id = area["name"]
            document.getElementById("container").append(div)
            h2 = document.createElement('h2')
            h2.innerText = "Läge " + area["name"]
            onclick = document.createAttribute("onclick")
            onclick.value = "hide('" + area["name"] + "')"
            h2.setAttributeNode(onclick)
            document.getElementById(area["name"]).append(h2)
            p = document.createElement('p')
            p.id = "_" + area["name"]
            document.getElementById(area["name"]).append(p)

def toggle_config(event):
    target = document.getElementById("hide_config")
    global config_hidden
    if config_hidden == False:
        target.style.display = "none"
        config_hidden = True
    else:
        target.style.display = "block"
        config_hidden = False

def strip_time(time_str):
    striped_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ") # 2023-11-16T16:47:00Z
    return striped_time

def reset_text():
    global test
    test = {}
    global response_dict
    areas = response_dict["areas"]
    for a in range(0, len(areas)):
        area = areas[a]
        test["output_departures_" + area["name"]] = ""

await callapi()
create_divs()
unhide_divs(1)

while True:

    await callapi()

    header_name = f" {response_dict['name']}"

    reset_text()

    departures = response_dict["departures"]
    for d in range (0, len(departures)):
        depature = departures[d]
        hasrealtime = depature["hasRealTimeDepartureDeviation"]
        if hasrealtime == True:
            realtime = str(depature["realTimeDepartureDateTime"])
            realtime_a = strip_time(realtime) + timedelta(hours=1)
            shown_realtime = str(realtime_a)[11:-3]
        else:
            realtime_a = strip_time("0001-01-01T00:00:00Z")
            shown_realtime = ""
        scheduled = str(depature["departureDateTime"])
        scheduled_a = strip_time(scheduled) + timedelta(hours=1)
        current_time = datetime.today() - timedelta(hours=1)
        if (realtime_a >= current_time) | (scheduled_a >= current_time):
            first_departure = departures[d]
            line_info = first_departure["line"]
            combine_departure(depature)
    write_departure()
    write_info()
    output_div = document.querySelector("#request_text")
    output_div.innerText = header_name


