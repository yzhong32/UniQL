import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding,
)
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory


class Memorier:
    def __init__(self):
        self.kernel = sk.Kernel()
        self.collection = "collection"

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

    async def populate_memory(self, path) -> None:
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

    async def search_memory_examples(self, question):
        result = await self.memory.search(self.collection, question)
        return result
