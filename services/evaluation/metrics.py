def recall_at_k(retrieved,relevant,k=5):return 0.0 if not relevant else len(set(retrieved[:k])&set(relevant))/len(relevant)
def reciprocal_rank(retrieved,relevant):
    for i,x in enumerate(retrieved,1):
        if x in relevant:return 1/i
    return 0.0
