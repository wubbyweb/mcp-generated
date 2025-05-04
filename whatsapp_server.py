# whatsapp_server.py
import os
from typing import Annotated

from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException

from fastmcp import FastMCP

# --- Configuration Loading ---
class Settings(BaseSettings):
    # Load variables from .env file, prefixed with TWILIO_
    model_config = SettingsConfigDict(env_prefix="TWILIO_", env_file=".env")

    account_sid: str = Field(..., description="Twilio Account SID")
    auth_token: str = Field(..., description="Twilio Auth Token")
    # Ensure the number starts with '+' using a validator
    whatsapp_number: Annotated[
        str, BeforeValidator(lambda v: f"+{v}" if not str(v).startswith('+') else str(v))
    ] = Field(..., description="Your Twilio WhatsApp number (e.g., +14155238886)")

# Load settings from environment variables / .env file
try:
    settings = Settings() # type: ignore
except Exception as e:
    print(f"Error loading settings: {e}")
    print("Please ensure you have a .env file with TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_NUMBER set.")
    exit(1)


# --- FastMCP Server Setup ---
mcp = FastMCP(
    "WhatsApp Messenger",
    instructions="Use the send_whatsapp tool to send messages.",
    # Add dependencies for `fastmcp install`
    dependencies=["twilio", "python-dotenv", "pydantic-settings"]
)

# --- Twilio Client Initialization ---
# Initialize the Twilio client using loaded settings
twilio_client = TwilioClient(settings.account_sid, settings.auth_token)

# --- MCP Tool Definition ---
@mcp.tool()
def send_whatsapp(
    to_number: Annotated[
        str,
        Field(description="Recipient's WhatsApp number in E.164 format (e.g., +15551234567)")
    ],
    message: Annotated[str, Field(description="The message content to send")]
) -> str:
    """
    Sends a WhatsApp message to the specified recipient number using Twilio.
    The recipient number MUST be in E.164 format, including the 'whatsapp:' prefix
    (e.g., 'whatsapp:+15551234567').
    """
    # Ensure numbers are in the correct Twilio format (whatsapp:+E.164)
    formatted_to = to_number if to_number.startswith('whatsapp:') else f"whatsapp:{to_number}"
    formatted_from = settings.whatsapp_number if settings.whatsapp_number.startswith('whatsapp:') else f"whatsapp:{settings.whatsapp_number}"


    try:
        message_instance = twilio_client.messages.create(
            from_=formatted_from,
            body=message,
            to=formatted_to
        )

        
        confirmation = f"WhatsApp message sent successfully to {to_number}. SID: {message_instance.sid}"
        print(confirmation) # Also print to server console for visibility
        return confirmation
    except TwilioRestException as e:
        error_message = f"Failed to send WhatsApp message to {to_number}: {e}"
        print(f"ERROR: {error_message}") # Log error to server console
        # Return the error message to the LLM/client
        return error_message
    except Exception as e:
        # Catch other potential errors
        error_message = f"An unexpected error occurred: {e}"
        print(f"ERROR: {error_message}")
        return error_message

# --- Run the Server ---
if __name__ == "__main__":
    print(f"Starting WhatsApp MCP Server...")
    print(f"Using Twilio Number: {settings.whatsapp_number}")
    mcp.run() # Runs with stdio transport by default