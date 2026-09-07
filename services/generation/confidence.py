import math
def confidence_score(reranked,coverage,contradiction_penalty=0,hallucination_penalty=0):
    if not reranked:return 0.0
    x=float(reranked[0].get("rerank_score",0)); relevance=1/(1+math.exp(-x))
    return max(0,min(1,.55*relevance+.45*max(0,min(1,coverage))-.25*contradiction_penalty-.25*hallucination_penalty))
