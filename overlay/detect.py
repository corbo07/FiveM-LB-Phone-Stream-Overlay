"""Erkennt per Screen-Capture, ob das Telefon im Spiel sichtbar ist, und meldet es an den lokalen Server.

  python detect.py --snap     Screenshot nach 5s als screenshot.png speichern (zum Ausschneiden von template.png)
  python detect.py            Erkennung starten
"""
import sys, time, urllib.request
import cv2, mss, numpy as np

SERVER = "http://127.0.0.1:3981/set?open="
TEMPLATE = "template.png"   # Ausschnitt vom Telefon (z.B. Rahmen/Header), siehe README
THRESHOLD = 0.92           # 0..1, hoeher = strenger
INTERVAL = 0.05             # Sekunden zwischen Pruefungen
CONFIRM = 2                 # so viele gleiche Ergebnisse in Folge noetig (gegen Flackern)
MONITOR = 2                 # 1 = Hauptmonitor
REGION = {"left": 4480, "top": 0, "width": 640, "height": 1440}             # optional: {"left":1500,"top":300,"width":400,"height":700} -> schneller und genauer

def grab(sct):
    img = np.array(sct.grab(REGION or sct.monitors[MONITOR]))
    return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

def post(state):
    try:
        urllib.request.urlopen(SERVER + ("1" if state else "0"), timeout=1).read()
    except Exception as e:
        print("Server nicht erreichbar (laeuft start.bat?):", e)

with mss.mss() as sct:
    if "--snap" in sys.argv:
        print("Screenshot in 5 Sekunden - Telefon im Spiel oeffnen!")
        time.sleep(5)
        cv2.imwrite("screenshot.png", np.array(sct.grab(REGION or sct.monitors[MONITOR])))
        print("Gespeichert: screenshot.png -> Telefon ausschneiden und als template.png speichern")
        sys.exit()

    tpl = cv2.imread(TEMPLATE, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        sys.exit("template.png fehlt. Erst 'python detect.py --snap' ausfuehren und Ausschnitt speichern.")

    state, streak, last = False, 0, None
    print("Erkennung laeuft. Strg+C zum Beenden.")
    while True:
        score = cv2.matchTemplate(grab(sct), tpl, cv2.TM_CCOEFF_NORMED).max()
        seen = score >= THRESHOLD
        streak = streak + 1 if seen == last else 1
        last = seen
        if streak >= CONFIRM and seen != state:
            state = seen
            print(f"Telefon {'AN' if state else 'AUS'} (score {score:.2f})")
            post(state)
        time.sleep(INTERVAL)
