from database import LOCATION_NAME_TO_ID

keys = [k for k in LOCATION_NAME_TO_ID if k.startswith("Amazon")]
print(keys)