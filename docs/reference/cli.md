# CLI Reference

The command-line interface provides the following primary commands:

*   `add [content]`: Adds a new memory to the system.
*   `search [query]`: Performs a semantic search for memories.
*   `list`: Lists all memories.
*   `delete [memory_id]`: Deletes a memory by its ID.
*   `ingest [path]`: Ingests text/markdown files from a directory.
*   `serve`: Starts the Agent API server.

**Advanced Recall Group Commands:**

*   `recall graph [memory_id]`: Visualizes the connections for a specific memory.
*   `recall link [source_id] [target_id]`: Explicitly link two memories in the Knowledge Graph.
*   `recall optimize`: Scans for cold memories and calculates potential storage savings.
