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

config_hidden = False
stop = "700600"
all_areas = ["A", "B", "C", "D", "E", "F", "G", "J", "X", "A1", "A2", "A3", "A4", "A5", "B1", "B2", "B2a", "B3", "B4", "B5", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "E1", "E2", "1a", "1b", "2a", "2b", "3", "4", "5", "6", "7a", "7b", "8a", "8b", "10"]

async def onclick(event):
    global stop
    global show_has_ran
    input_text = document.querySelector("#input")
    stop = input_text.value
    for a in range (0, len(all_areas)):
        target = document.getElementById("hide_" + all_areas[a])
        target.style.display = "none"
    await callapi()
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
        target = document.getElementById("hide_" + area["name"])
        target.style.display = "block"

def hide_div(div):
    target = document.getElementById("hide_" + div)    
    target.style.display = "none"

def hide_A(event):
    hide_div("A")

def hide_B(event):
    hide_div("B")

def hide_C(event):
    hide_div("C")

def hide_D(event):
    hide_div("D")

def hide_E(event):
    hide_div("E")

def hide_F(event):
    hide_div("F")

def hide_G(event):
    hide_div("G")

def hide_J(event):
    hide_div("J")

def hide_X(event):
    hide_div("X")

def hide_A1(event):
    hide_div("A1")

def hide_A2(event):
    hide_div("A2")

def hide_A3(event):
    hide_div("A3")

def hide_A4(event):
    hide_div("A4")

def hide_A5(event):
    hide_div("A5")

def hide_B1(event):
    hide_div("B1")

def hide_B2(event):
    hide_div("B2")

def hide_B2a(event):
    hide_div("B2a")

def hide_B3(event):
    hide_div("B3")

def hide_B4(event):
    hide_div("B4")

def hide_B5(event):
    hide_div("B5")

def hide_C1(event):
    hide_div("C1")

def hide_C2(event):
    hide_div("C2")

def hide_C3(event):
    hide_div("C3")

def hide_C4(event):
    hide_div("C4")

def hide_C5(event):
    hide_div("C5")

def hide_D1(event):
    hide_div("D1")

def hide_D2(event):
    hide_div("D2")

def hide_E1(event):
    hide_div("E1")

def hide_E2(event):
    hide_div("E2")

def hide_1a(event):
    hide_div("1a")

def hide_1b(event):
    hide_div("1b")

def hide_2a(event):
    hide_div("2a")

def hide_2b(event):
    hide_div("2b")

def hide_3(event):
    hide_div("3")

def hide_4(event):
    hide_div("4")

def hide_5(event):
    hide_div("5")

def hide_6(event):
    hide_div("6")

def hide_7a(event):
    hide_div("7a")

def hide_7b(event):
    hide_div("7b")

def hide_8a(event):
    hide_div("8a")

def hide_8b(event):
    hide_div("8b")

def hide_10(event):
    hide_div("10")

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

await callapi()
unhide_divs(1)

if True:

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
    output_div = document.querySelector("#request_text")
    output_div.innerText = header_name


