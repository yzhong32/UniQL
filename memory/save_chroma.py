# this file is deprecated

import asyncio

import numpy as np

if __name__ == "__main__":
    memory = ChromaMemoryStore()
    
    asyncio.run(memory.create_collection("test_collection"))
    collection = asyncio.run(memory.get_collection("test_collection"))

    asyncio.run(memory.upsert_batch(collection.name, [memory_record1, memory_record2]))