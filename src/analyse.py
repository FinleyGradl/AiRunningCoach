import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

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
df["zeit"] = pd.to_datetime(df["zeit"])
startzeit = df["zeit"].iloc[0]

df["sekunden"] = (
    df["zeit"] - startzeit
).dt.total_seconds()

df["delta_distanz"] = df["distanz"].diff()
df["delta_zeit"] = df["sekunden"].diff()

df["pace_min_pro_km"] = (
    df["delta_zeit"] /
    df["delta_distanz"]
) * 1000 / 60
import numpy as np

df["pace_min_pro_km"] = df["pace_min_pro_km"].replace(
    [np.inf, -np.inf],
    np.nan
)
df.loc[
    (df["pace_min_pro_km"] < 3)
    | (df["pace_min_pro_km"] > 15),
    "pace_min_pro_km"
] = np.nan

df["pace_geglattet"] = (
    df["pace_min_pro_km"]
    .rolling(window=30, min_periods=1)
    .mean()
)

print(df.head())
print()
print(df.dtypes)

print()
print("Anzahl Messpunkte:", len(df))
print("Max HF:", df["herzfrequenz"].max())
print("Durchschnitt HF:", round(df["herzfrequenz"].mean(), 1))

plt.figure(figsize=(12, 6))
plt.plot(df["herzfrequenz"])
plt.title("Herzfrequenz während des Laufs")
plt.xlabel("Messpunkt")
plt.ylabel("Herzfrequenz (bpm)")
plt.grid()
plt.savefig("../herzfrequenz.png")

plt.figure(figsize=(12, 6))
plt.plot(
    df["sekunden"] / 60,
    df["pace_geglattet"]
)
plt.title("Pace-Verlauf")
plt.xlabel("Zeit (min)")
plt.ylabel("Pace (min/km)")
plt.grid()
plt.savefig("../pace.png")

print()
print(df[["sekunden", "distanz"]].head())
print()
print(
    df[
        [
            "sekunden",
            "distanz",
            "pace_min_pro_km"
        ]
    ].head(20)
)
print(
    df[
        [
            "pace_min_pro_km",
            "pace_geglattet"
        ]
    ].tail(20)
)

print()
print(
    "Durchschnittspace:",
    round(
        df["pace_geglattet"].mean(),
        2
    ),
    "min/km"
)