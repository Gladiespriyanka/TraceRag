import re
def chunk_text(text,chunk_size=900,overlap=120):
    text=re.sub(r"\s+"," ",text).strip()
    if not text:return []
    if overlap>=chunk_size:raise ValueError("overlap must be smaller than chunk_size")
    out=[]; start=0
    while start<len(text):
        end=min(start+chunk_size,len(text))
        if end<len(text):
            b=max(text.rfind(". ",start,end),text.rfind("\n",start,end))
            if b>start+chunk_size//2:end=b+1
        out.append(text[start:end].strip())
        if end>=len(text):break
        start=max(0,end-overlap)
    return [x for x in out if x]
