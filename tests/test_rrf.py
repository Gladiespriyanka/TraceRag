from services.retrieval.rrf import reciprocal_rank_fusion
def test_rrf():assert reciprocal_rank_fusion([[{"chunk_id":"a"},{"chunk_id":"b"}],[{"chunk_id":"a"}]])[0]["chunk_id"]=="a"
