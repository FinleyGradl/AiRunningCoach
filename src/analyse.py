import xml.etree.ElementTree as ET
import pandas as pd

datei = "../data/Lauf18.06.26.tcx"

tree = ET.parse(datei)
root = tree.getroot()

ns = {
    "tcx": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
}

trackpoints = root.findall(".//tcx:Trackpoint", ns)

daten = []

for punkt in trackpoints:

    zeit = punkt.find("tcx:Time", ns)
    hoehe = punkt.find("tcx:AltitudeMeters", ns)
    distanz = punkt.find("tcx:DistanceMeters", ns)
    herz = punkt.find("tcx:HeartRateBpm/tcx:Value", ns)

    daten.append({
        "zeit": zeit.text if zeit is not None else None,
        "herzfrequenz": int(herz.text) if herz is not None else None,
        "hoehe": float(hoehe.text) if hoehe is not None else None,
        "distanz": float(distanz.text) if distanz is not None else None
    })

df = pd.DataFrame(daten)

print(df.head())

print()
print("Anzahl Messpunkte:", len(df))
print("Max HF:", df["herzfrequenz"].max())
print("Durchschnitt HF:", round(df["herzfrequenz"].mean(), 1))