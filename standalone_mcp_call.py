# /home/rj/Code/mcp-generated/test.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import asyncio # Needed for async operations

from mcp import ClientSession, StdioServerParameters, types # Import new MCP components
from mcp.client.stdio import stdio_client # Import the stdio client connector

# --- Configuration ---
load_dotenv()  # Load environment variables from .env file

# Ensure your OPENAI_API_KEY is set in your environment or .env file
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit(1)

openai_client = OpenAI()
mcp_server_script = "/home/rj/Code/mcp-generated/whatsapp_server.py" # Path to the server script
# Get the python executable from the virtual environment for consistency
python_executable = "/home/rj/Code/mcp-generated/.venv/bin/python3"

# --- Define the Tool for OpenAI ---
# This structure mirrors the tool defined in whatsapp_server.py
# It tells the OpenAI model what tool is available.
whatsapp_tool_definition = {
    "type": "function",
    "function": {
        "name": "send_whatsapp",
        "description": "Sends a WhatsApp message to the specified recipient number using Twilio. "
                       "The recipient number MUST be in E.164 format, including the 'whatsapp:' prefix "
                       "(e.g., 'whatsapp:+15551234567').",
        "parameters": {
            "type": "object",
            "properties": {
                "to_number": {
                    "type": "string",
                    "description": "Recipient's WhatsApp number in E.164 format, including the 'whatsapp:' prefix (e.g., whatsapp:+15551234567)"
                },
                "message": {
                    "type": "string",
                    "description": "The message content to send"
                }
            },
            "required": ["to_number", "message"]
        }
    }
}

# --- User Request ---
# Define what you want the AI to do
user_prompt = "Please send a WhatsApp message to whatsapp:+919080573869 saying 'Hello from the OpenAI test client!'"

# --- Main Async Function ---
async def run():
    print(f"--- Sending request to OpenAI ---")
    print(f"Prompt: {user_prompt}")

    try:
        # --- Call OpenAI API ---
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Or another model that supports tool calling like gpt-3.5-turbo
            messages=[{"role": "user", "content": user_prompt}],
            tools=[whatsapp_tool_definition],
            tool_choice="auto" # Let the model decide if it needs to use the tool
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # --- Process Response ---
        if tool_calls:
            print("\n--- OpenAI requested tool call ---")
            for tool_call in tool_calls:
                if tool_call.function.name == "send_whatsapp":
                    function_args = json.loads(tool_call.function.arguments)
                    tool_name = tool_call.function.name
                    print(f"Tool to call: {tool_name}")
                    print(f"Arguments: {json.dumps(function_args, indent=2)}")

                    print(f"\n--- Connecting to MCP Server ({mcp_server_script}) via stdio ---")
                    # Define server parameters for stdio connection
                    server_params = StdioServerParameters(
                        command=python_executable,
                        args=[mcp_server_script],
                    )

                    # Connect using stdio_client and manage session
                    async with stdio_client(server_params) as (read, write):
                        async with ClientSession(read, write) as session:
                            # Initialize the connection (optional but good practice)
                            # await session.initialize() # Might not be strictly needed if just calling a tool

                            print(f"--- Calling tool '{tool_name}' on server ---")
                            # Call the tool on the server with the arguments from OpenAI
                            # Note: The mcp library expects arguments nested under 'arguments' key
                            result = await session.call_tool(tool_name, arguments=function_args)

                            print("\n--- Response from MCP Server ---")
                            print(result) # The result object might have more structure, adjust printing if needed
        else:
            print("\n--- OpenAI Response (no tool call requested) ---")
            print(response_message.content)

    except Exception as e:
        print(f"\n--- An error occurred ---")
        print(e)

# --- Run the async function ---
if __name__ == "__main__":
    asyncio.run(run())