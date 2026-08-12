# -*- coding: utf-8 -*-
"""
Step 4: Topic-to-dimension mapping and dimension-level tables.

Track A topics are mapped to the five technological dimensions of the
Perception-Cognition-Action architecture (Vernon, 2014) extended with
Structure (embodiment; Pfeifer & Bongard, 2006).
Track B topics are mapped to experiential dimensions grounded in
Hassenzahl's (2003) UX model and Mori's (1970) uncanny valley theory.

The mapping is declared EXPLICITLY below (topic id -> dimension), with the
defining c-TF-IDF terms recorded next to each assignment, so that the
topic-to-dimension correspondence requested by the reviewers is fully
transparent and reproducible.

Outputs:
  output/trackA_dimensions.csv   (dimension, topics, count, share)
  output/trackB_dimensions.csv
  output/trackB_dim_sentiment.csv (dimension x VADER sentiment)
"""
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"

# ---- mapping tables ------------------------------------------------------
# Track A (K=14). Defining c-TF-IDF terms in comments.
MAP_A = {
    3:  "Actuation",     # foot, shank, leg, ankle, thigh, knee - leg mechanisms
    13: "Actuation",     # leg, hydraulic, thigh, hip - hydraulic leg assemblies
    8:  "Actuation",     # waist, hip, driving, joint - torso/hip drive units
    6:  "Actuation",     # gear, motor, screw, rotor, planetary - drive trains
    7:  "Actuation",     # pneumatic, muscles, air, cylinder - pneumatic actuation
    1:  "Manipulation",  # arm, finger, palm, wrist, knuckle, hand
    12: "Manipulation",  # mechanism, shoulder, arm, connecting - arm assemblies
    0:  "Control",       # control, target, motion, angle, state
    4:  "Control",       # biped, gait, mass, centroid, planning - balance control
    2:  "Control",       # control methods/devices, storage medium (verified by sampling)
    10: "Control",       # gait, reinforcement, learning, training - learned control
    11: "Perception",    # point, obstacle, cloud, image, map, camera
    9:  "Structure",     # expression, head modules - human-facing embodiment (verified)
    5:  "Structure",     # head, shell, charging, heat dissipation - housings
}

# Track B (K=15). Hassenzahl (2003) pragmatic/hedonic + Mori (1970).
MAP_B = {
    12: "Task needs",    # buy, want, need, clothes, house, cost, clean - demand/purchase
    2:  "Task needs",    # rack, plate, trash, drying, basket - household task commentary
    11: "Interaction",   # voice, speech, sounds - communication modalities
    10: "Acceptance",    # facial, uncanny, expressions, valley - uncanny valley
    14: "Acceptance",    # terrifying, scary, creepy, scared - fear
    4:  "Acceptance",    # terminator, skynet - existential threat framing
    3:  "Acceptance",    # cgi, real, believe, animation - authenticity distrust
    13: "Projection",    # agi, years, future, advanced - future expectations
    7:  "Projection",    # future, technology, progress, amazing
    8:  "Projection",    # ameca, atlas, boston dynamics, sophia - brand comparison
    5:  "Projection",    # optimus, tesla, transformers - brand symbolism
    1:  "Projection",    # movie, ai, hope, robot rights - societal imagination (verified)
    0:  "Projection",    # detroit become human - pop-culture imagination (verified)
    9:  "Projection",    # mitchells vs machines - pop-culture imagination
    6:  "Projection",    # parkour, backflip, walk - capability spectacle (verified)
}

# ---- Track A -------------------------------------------------------------
ta = pd.read_csv(OUT / "trackA_doc_topics.csv")
ta["dimension"] = ta["topic"].map(MAP_A)
dimA = (ta.groupby("dimension").agg(count=("topic", "size"))
        .assign(share=lambda d: (d["count"] / len(ta) * 100).round(1))
        .sort_values("count", ascending=False))
print("Track A dimensions:")
print(dimA.to_string())
dimA.to_csv(OUT / "trackA_dimensions.csv", encoding="utf-8-sig")

# ---- Track B -------------------------------------------------------------
tb = pd.read_csv(OUT / "trackB_doc_topics.csv")
yt = pd.read_csv(OUT / "youtube_sentiment.csv")
assert len(tb) == len(yt)
yt["topic"] = tb["topic"].values
yt["dimension"] = yt["topic"].map(MAP_B)

dimB = (yt.groupby("dimension").agg(count=("topic", "size"))
        .assign(share=lambda d: (d["count"] / len(yt) * 100).round(1))
        .sort_values("count", ascending=False))
print("\nTrack B dimensions:")
print(dimB.to_string())
dimB.to_csv(OUT / "trackB_dimensions.csv", encoding="utf-8-sig")

sent = (pd.crosstab(yt["dimension"], yt["sentiment"], normalize="index")
        .mul(100).round(1))
sent["n"] = yt.groupby("dimension").size()
print("\nTrack B dimension x sentiment (%):")
print(sent.to_string())
sent.to_csv(OUT / "trackB_dim_sentiment.csv", encoding="utf-8-sig")
