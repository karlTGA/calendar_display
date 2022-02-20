import network
from time import sleep
import urequests

NETWORK_SSID = 'Nota'
NETWORK_PASSWORD = 'hL819m%:n*JG":XC'
URL = "https://calendar.google.com/calendar/ical/r6hqf4rspl214j1vt7sk77mg34%40group.calendar.google.com/private-14d918f326f76e89a5a2c3ec77ee9142/basic.ics"

def connect_wifi():
    print("Try to connect to wifi network...")

    sta_if = network.WLAN(network.STA_IF)

    if (not sta_if.active(True)):
        print("Failed to activate wifi interface.")
        return

    sta_if.connect(NETWORK_SSID, NETWORK_PASSWORD)
    
    while not sta_if.isconnected():
        print("...")
        sleep(1)

    print(f"Conntect to wifi network {NETWORK_SSID}.")
    print(f"IP: {sta_if.ifconfig()[0]}")

def load_ics():
    ics = urequests.get(URL)

    lines = ics.text.splitlines()
    events = []

    for line in lines:
        if line == 'BEGIN:VEVENT':
            events.append({
                "name": "",
                "start": "",
                "end": "",
                "location": ""
            })
            continue

        if len(events) == 0:
            continue

        if line.startswith("DTSTART"):
            events[-1]['start'] = line.replace('DTSTART:', '')
            continue

        if line.startswith("DTEND"):
            events[-1]['end'] = line.replace('DTEND:', '')
            continue

        if line.startswith("SUMMARY"):
            events[-1]['name'] = line.replace('SUMMARY:', '')
            continue

        if line.startswith("LOCATION"):
            events[-1]['location'] = line.replace('LOCATION:', '')
            continue

    print(events)
