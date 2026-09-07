import re
def extract_claims(text):return [s.strip() for s in re.split(r"(?<=[.!?])\s+",text.strip()) if len(s.strip())>15]
