from collections import defaultdict
def reciprocal_rank_fusion(result_lists,k=60):
    scores=defaultdict(float)
    for results in result_lists:
        for rank,item in enumerate(results,1):scores[item["chunk_id"]]+=1/(k+rank)
    return [{"chunk_id":i,"score":v} for i,v in sorted(scores.items(),key=lambda x:x[1],reverse=True)]
