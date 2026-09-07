def build_grounded_prompt(query,contexts):
    evidence="\n".join(f"SOURCE {i}\nchunk_id={c['chunk_id']}\ndocument={c['filename']}\ncontent={c['content']}" for i,c in enumerate(contexts,1))
    return f"""You are TraceRAG, an evidence-first enterprise research assistant. Use ONLY supplied evidence. Every factual sentence must cite [Source N]. If evidence is insufficient output [INSUFFICIENT_EVIDENCE]. Do not invent facts. Return JSON with keys answer and citations, citations being objects with source and claim. QUESTION: {query}\nEVIDENCE:\n{evidence}"""
