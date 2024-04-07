import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

class QueryConverter:
    def __init__(self, plugins_directory):
        # Initialize the Semantic Kernel
        self.kernel = sk.Kernel()
        
        # Prepare OpenAI service using credentials stored in the `.env` file
        api_key, org_id = sk.openai_settings_from_dot_env()
        service_id = "default"
        
        # Add the OpenAI Chat Completion service
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id="gpt-4-0125-preview",
                api_key=api_key,
                org_id=org_id
            )
        )
        
        # Import the required plugin
        self.translateFunctions = self.kernel.import_plugin_from_prompt_directory(plugins_directory, "TranslatePlugin")
        self.mongoFunction = self.translateFunctions["MongoDB"]
        self.neo4jFunction = self.translateFunctions["Neo4j"]

    async def convert(self, sql_query):
        # Invoke the MongoDB function from the plugin
        result = await self.kernel.invoke(self.mongoFunction, sk.KernelArguments(sql=sql_query))
        return result

# Usage example
if __name__ == "__main__":
    converter = QueryConverter("./plugins")
    asyncio.run(converter.convert("select * from Students where weight > 100"))