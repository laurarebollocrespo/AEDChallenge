
import json
from programming_skills import divide_by_skill
import pandas as pd
#si quiere ir solo, separarlo,   ammigos, idioma, lenguage
participants = pd.read_json("data/datathon_participants.json")
 # Dividir en tres grupos por habilidad
high_skill, mid_skill, low_skill = divide_by_skill(participants)
