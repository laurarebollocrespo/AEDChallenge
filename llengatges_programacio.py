import pandas as pd

df = pd.read_json('datathon_participants.json')


# Alternative approach with steps broken out
def get_lowercase_keys(d):
    return {k.lower().strip() for k in d.keys() if k.lower().strip() not in ('ui/ux design', 'java script', 'html/css')}

unique_keys = set().union(*df['programming_skills'].map(get_lowercase_keys))


print(unique_keys)