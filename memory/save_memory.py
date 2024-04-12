# this file is deprecated

import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding,
    AzureChatCompletion,
    AzureTextEmbedding,
)
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin

# from services import Service

# # Select a service to use for this notebook (available services: OpenAI, AzureOpenAI, HuggingFace)
# selectedService = Service.OpenAI


kernel = sk.Kernel()

chat_service_id = "chat"

api_key, org_id = sk.openai_settings_from_dot_env()
oai_chat_service = OpenAIChatCompletion(
    service_id=chat_service_id, ai_model_id="gpt-3.5-turbo", api_key=api_key, org_id=org_id
)
embedding_gen = OpenAITextEmbedding(ai_model_id="text-embedding-ada-002", api_key=api_key, org_id=org_id)
kernel.add_service(oai_chat_service)
kernel.add_service(embedding_gen)

memory = SemanticTextMemory(storage=sk.memory.VolatileMemoryStore(), embeddings_generator=embedding_gen)
kernel.import_plugin_from_object(TextMemoryPlugin(memory), "TextMemoryPlugin")


collection_id = "ES"


async def populate_memory(memory: SemanticTextMemory) -> None:
    # Add some documents to the semantic memory
    await memory.save_information(collection=collection_id, id="definition", text="Elasticsearch is the distributed search and analytics engine at the heart of the Elastic Stack. Logstash and Beats facilitate collecting, aggregating, and enriching your data and storing it in Elasticsearch. Kibana enables you to interactively explore, visualize, and share insights into your data and manage and monitor the stack. Elasticsearch is where the indexing, search, and analysis magic happens.")
    await memory.save_information(collection=collection_id, id="notrelevant", text="I'm Bohan Wu, a MCS studnet at UIUC")



async def search_memory_examples(memory: SemanticTextMemory) -> None:
    questions = ["What is ES?", "Intorduce Bohan Wu"]

    for question in questions:
        print(f"Question: {question}")
        result = await memory.search(collection_id, question)
        print(f"Answer: {result[0].text}\n")

async def main():
    await populate_memory(memory)
    await search_memory_examples(memory)

if __name__ == '__main__':
    asyncio.run(main())
