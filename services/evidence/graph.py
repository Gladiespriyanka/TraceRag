from packages.db.models import EvidenceClaim,GraphEdge
async def persist_claims(db,chunk_id,claims):
    ids=[]
    for claim in claims:
        x=EvidenceClaim(chunk_id=chunk_id,claim_text=claim,claim_type="fact");db.add(x);await db.flush();ids.append(x.id)
    return ids
async def add_edge(db,source_id,target_id,edge_type,weight=1.0):
    x=GraphEdge(source_id=source_id,target_id=target_id,edge_type=edge_type,weight=weight);db.add(x);await db.flush();return x
