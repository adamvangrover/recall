from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.memory.vector_store import VectorMemoryStore

app = FastAPI(title="Total Recall Agent API")
memory_store = VectorMemoryStore()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class MemoryCreate(BaseModel):
    content: str
    metadata: dict = {}

@app.post("/v1/query")
def query_memories(request: QueryRequest):
    results = memory_store.search_memory(request.query, n_results=request.top_k)
    return {"results": results}

@app.post("/v1/memories")
def add_memory(memory: MemoryCreate):
    memory_id = memory_store.add_memory(memory.content, memory.metadata)
    return {"id": memory_id, "status": "stored"}

@app.get("/v1/stats")
def get_stats():
    memories = memory_store.list_memories()
    return {"count": len(memories)}
