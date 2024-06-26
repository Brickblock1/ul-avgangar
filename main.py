import asyncio, micropip
await micropip.install("python-dateutil")
from pyodide.http import pyfetch
from pyscript import document, window
from datetime import datetime, timedelta
from dateutil import tz


def combine_departure(departure):
    varstr = "output_departures_" + departure["area"]
    global departure_strings
    #departure_strings[varstr] = departure_strings[varstr] + line_info["name"] + suffix + " mot " + line_info["towards"] + "\navgår: "+ thing[11:-4]+ " UTC trafikslag: " + traffictype["Name"] + "\n"
    deviations = departure["deviations"]
    combined_deviations = ""
    for d in range (0, len(deviations)):
        deviation = deviations[d]
        if d == len(deviations) - 1:
            combined_deviations = combined_deviations + deviation["header"]
        else:
            combined_deviations = combined_deviations + deviation["header"] + ", "
    if line_info["trainNo"] == 0:
        departure_strings[varstr] = departure_strings[varstr] + line_info["name"] + " " + line_info["towards"] + "\n"+ str(scheduled_a)[11:-9] + " " + shown_realtime + " " + str(combined_deviations) + "\n"
    else:
        if line_info["lineNo"] == 995:
            linenumber = " 40 "
        elif line_info["lineNo"] == 996:
            linenumber = " 43 "
        else:
            linenumber = " "
        departure_strings[varstr] = departure_strings[varstr] + traffictype["Name"] + linenumber + line_info["towards"] + " " + str(line_info["trainNo"]) + "\n"+ str(scheduled_a)[11:-9] + " " + shown_realtime + " " + str(combined_deviations) + "\n"


def write_departure():
    global response_dict
    areas = response_dict["areas"]
    for a in range (0, len(areas)):
        area = areas[a]
        id = "#_" + area["name"]
        output_div2 = document.querySelector(id)
        output_div2.innerText = departure_strings["output_departures_"+area["name"]]

def write_info():
    info_div = document.querySelector("#_Info")
    info_div.innerText = str(current_time)[11:-16]

async def onclick(event):
    global stop
    areas = response_dict["areas"]
    for a in range (0, len(areas)):
        area = areas[a]
        target = document.getElementById(area["name"])
        target.style.display = "none"
    input_text = document.querySelector("#input")
    #stop = input_text.value
    url = document.URL
    position = url.rfind("?")
    if position == -1:
        new_url=url + "?" + input_text.value
    else:
        new_url = url[:position] + "?" + input_text.value
    window.history.pushState(0, 0, new_url)
    get_query()
    await callapi()
    create_divs()
    unhide_divs(1)
    toggle_config(1)
    

async def callapi():
    global response_dict
    try:
        response = await pyfetch(url="https://api.ul.se/api/v4/stop/" + stop, method="GET")
        response_dict = await response.json()
    except:
        response_dict = {
            'name': "CORS (Cross origin resource sharing) isn't enabled",
            'areas': [{'name': "fel"}],
            'departures': [{'hasRealTimeDepartureDeviation': False,
                            'departureDateTime': '2023-11-16T16:47:00Z'}]
            }

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
        if document.getElementById(area["name"]) == None:
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
    if target.style.display == "block":
        target.style.display = "none"
    else:
        target.style.display = "block"

def strip_time(time_str):
    striped_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ") # 2023-11-16T16:47:00Z
    return striped_time

def reset_text():
    global departure_strings
    departure_strings = {}
    global response_dict
    areas = response_dict["areas"]
    for a in range(0, len(areas)):
        area = areas[a]
        departure_strings["output_departures_" + area["name"]] = ""

def get_query():
    global stop 
    url = document.URL
    position = url.find("?")
    stop = url[position + 1:]
    len(stop)
    if len(stop) != 6:
        stop = "700600"

def make_time_aware(time):
    time = time.replace(tzinfo=tz.gettz("UTC"))
    time = time.astimezone(tz.gettz("Stockholm"))
    return time
        

get_query()
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
            realtime_a = strip_time(realtime)
            realtime_a = make_time_aware(realtime_a)
            shown_realtime = str(realtime_a)[11:-9]
        else:
            realtime_a = strip_time("0002-01-01T00:00:00Z")
            realtime_a = make_time_aware(realtime_a)
            shown_realtime = ""
        scheduled = str(depature["departureDateTime"])
        scheduled_a = strip_time(scheduled)
        scheduled_a = make_time_aware(scheduled_a)
        current_time = datetime.now(tz=tz.gettz("UTC"))
        current_time = make_time_aware(current_time)
        if (realtime_a >= current_time) | (scheduled_a >= current_time):
            first_departure = departures[d]
            line_info = first_departure["line"]
            traffictype = line_info["trafficType"]
            combine_departure(depature)
    write_departure()
    write_info()
    output_div = document.querySelector("#request_text")
    output_div.innerText = header_name


