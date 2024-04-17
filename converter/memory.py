import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding,
)
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory

def read_and_split_queries(filename):
    with open(filename, 'r') as file:
        # Read all lines from the file
        content = file.read()
    
    # Split the content by double newlines, which separates each query pair
    blocks = content.split('\n\n')
    
    # Split each block into SQL and Neo4J queries and strip any leading/trailing whitespace
    queries = [block.strip().split('\n') for block in blocks if block.strip()]
    
    # Return list of query pairs
    return queries


class Memorier:
    def __init__(self):
        self.kernel = sk.Kernel()
        self.collection = "collection"
        self.example_collection = "example_collection"
        self.mp = {}

        chat_service_id = "chat"

        api_key, org_id = sk.openai_settings_from_dot_env()
        oai_chat_service = OpenAIChatCompletion(
            service_id=chat_service_id, ai_model_id="gpt-3.5-turbo", api_key=api_key, org_id=org_id
        )
        embedding_gen = OpenAITextEmbedding(ai_model_id="text-embedding-ada-002", api_key=api_key, org_id=org_id)
        self.kernel.add_service(oai_chat_service)
        self.kernel.add_service(embedding_gen)

        self.memory = SemanticTextMemory(storage=sk.memory.VolatileMemoryStore(), embeddings_generator=embedding_gen)
        self.kernel.import_plugin_from_object(TextMemoryPlugin(self.memory), "TextMemoryPlugin")

    async def populate_text_memory(self, path) -> None:
        # Read the contents of the file
        with open(path, 'r') as file:
            lines = file.readlines()

        num_segments = 10

        # Calculate the number of lines per segment
        lines_per_segment = max(1, len(lines) // num_segments)

        # Split the lines into segments and process each segment
        for i in range(0, len(lines), lines_per_segment):
            segment = lines[i:i + lines_per_segment]
            segment = "\n".join(segment)
            await self.memory.save_information(self.collection, id=str(i), text=segment)

    async def populate_examples_memory(self, path) -> None:
        pairs = read_and_split_queries(path)

        for i, (sql, target_ql) in enumerate(pairs):
            await self.memory.save_information(self.example_collection, id=str(i), text=sql)
            self.mp[sql]=target_ql

    async def search_text_memory(self, question):
        result = await self.memory.search(self.collection, question, limit=1)
        if(len(result)>0):
            return result[0].text
        else:
            return ""

    async def search_examples_memory(self, question):
        sqls = await self.memory.search(self.example_collection, question, limit=2)
        if(len(sqls)==0):
            return ""
        result = ""
        for i, sql in enumerate(sqls):
            example = "Example {i}:\nSQL: {sql}\ntarget query: {tq}\n".format(i=i+1, sql=sql.text, tq=self.mp[sql.text])
            result = result+example
        return result
    
async def test():
    memorier = Memorier()
    await memorier.populate_examples_memory("/Users/bohanwu/Code/SQLLMConverter/converter/memory/neo4j_examples")
    res = await memorier.search_examples_memory("SELECT id FROM trip ORDER BY duration LIMIT 1")
    print(res)
    
if __name__ == '__main__':
    asyncio.run(test())