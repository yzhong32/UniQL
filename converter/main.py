import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion

kernel = sk.Kernel()

plugins_directory = "./plugins"

# Prepare OpenAI service using credentials stored in the `.env` file
api_key, org_id = sk.openai_settings_from_dot_env()
service_id="default"
kernel.add_service(
    OpenAIChatCompletion(
        service_id=service_id,
        ai_model_id="gpt-3.5-turbo",
        api_key=api_key,
        org_id=org_id
    )
)

translateFunctions = kernel.import_plugin_from_prompt_directory(plugins_directory, "TranslatePlugin")

mongoFunction = translateFunctions["MongoDB"]


# Run your prompt
# Note: functions are run asynchronously
async def main():
    result = await kernel.invoke(mongoFunction, sk.KernelArguments(sql="select * from Students where weight > 100"))
    print(result) # => Robots must not harm humans.

if __name__ == "__main__":
    asyncio.run(main())
    