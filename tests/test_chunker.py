from services.ingestion.chunker import chunk_text
def test_chunker():assert chunk_text("sentence. "*100)
