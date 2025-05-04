# Twilio WhatsApp FastMCP Server 💬

This project provides a simple FastMCP server that allows sending WhatsApp messages using the Twilio API.

## Features

*   📲 Sends WhatsApp messages via Twilio.
*   🤖 Exposes a `send_whatsapp` tool for use with FastMCP clients (like AI models).
*   🔒 Loads configuration securely from a `.env` file.
*   🧪 Includes a basic test script (`/home/rj/Code/mcp-generated/twilio_test.py`) for direct Twilio API interaction.

## Setup

1.  **Get the Code:**
    Clone this repository or download the source files into `/home/rj/Code/mcp-generated/`.

2.  **Create a Virtual Environment (Recommended){
@@ -77,11 +77,11 @@

### 2. Running the Test Script

-The `/home/rj/Code/mcp-generated/twilio_test.py` script provides a way to directly test sending a message using your Twilio credentials *without* the FastMCP server.
+The `/home/rj/Code/mcp-generated/twilio_test.py` script provides a way to directly test sending a message using your Twilio credentials *without* the FastMCP server. 🛠️

*   **Modify the script:** Ensure the `to=` number in `/home/rj/Code/mcp-generated/twilio_test.py` is a WhatsApp number linked to your Twilio Sandbox (if using the Sandbox) or any valid WhatsApp number (if using a purchased Twilio number). The `from_` number should typically be your Twilio Sandbox number (`whatsapp:+14155238886`) or your purchased Twilio WhatsApp number.
*   **Run the script:**
-    ```bash
+    ```bash ▶️
    python /home/rj/Code/mcp-generated/twilio_test.py
    ```
    This will attempt to send a hardcoded message ("Is this working?") from the specified Twilio number to the specified recipient.

:**
    ```bash 🌱
    cd /home/rj/Code/mcp-generated/
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    The necessary dependencies are listed in `/home/rj/Code/mcp-generated/whatsapp_server.py`. You can install them using pip:
    ```bash 📦
    pip install twilio python-dotenv pydantic-settings fastmcp
    ```
    Alternatively, if using the FastMCP framework features:
    ```bash
    fastmcp install /home/rj/Code/mcp-generated/whatsapp_server.py
    ```

4.  **Configure Environment Variables:**
    *   Sign up for a Twilio account if you don't have one.
    *   Get your Account SID and Auth Token from the Twilio Console.
    *   Set up the Twilio Sandbox for WhatsApp or configure a dedicated Twilio WhatsApp number.
    *   Create a file named `.env` in the project root directory (`/home/rj/Code/mcp-generated/`).
    *   Add your Twilio credentials and WhatsApp number to the `.env` file:
        🔑
        ```dotenv
        # /home/rj/Code/mcp-generated/.env
        TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        TWILIO_AUTH_TOKEN=your_auth_token_here
        TWILIO_WHATSAPP_NUMBER=+14155238886 # Use your Twilio WhatsApp number (Sandbox or purchased)
        ```
    *   **Important:** Replace the placeholder values with your actual credentials and number. Ensure the `TWILIO_WHATSAPP_NUMBER` starts with a `+` and includes the country code (E.164 format). The `whatsapp_server.py` script will automatically add the `+` if it's missing from the `.env` file.
        ❗
    *   **Trial Account Note:** If you are using a Twilio trial account, the `TWILIO_WHATSAPP_NUMBER` will likely be the Twilio Sandbox number (`+14155238886`). You *must* enroll any recipient (`to_number`) phone numbers in your Twilio Sandbox via the Twilio console for messages to be delivered successfully. Sending to non-enrolled numbers requires upgrading your Twilio account.

## Usage

### 1. Running the FastMCP Server

To make the `send_whatsapp` tool available for remote calls (e.g., from an AI model integrated with FastMCP):

```bash ▶️
python /home/rj/Code/mcp-generated/whatsapp_server.py
```

The server will start and print the Twilio number it's configured to use. It will listen for incoming requests (by default via stdio, but FastMCP supports other transports). A FastMCP client can then call the `send_whatsapp` tool with `to_number` (including the `whatsapp:` prefix, e.g., `whatsapp:+15551234567`) and `message` arguments.

**Example Interaction (Conceptual):**

A client (like an AI 🤖) might send a request like this (format depends on the transport):

```json
{
  "tool_name": "send_whatsapp",
  "arguments": {
    "to_number": "whatsapp:+15551234567",
    "message": "Hello from the FastMCP server!"
  }
}
```

The server will process this, call the Twilio API, and return a confirmation or error message.

### 2. Running the Test Script

The `/home/rj/Code/mcp-generated/twilio_test.py` script provides a way to directly test sending a message using your Twilio credentials *without* the FastMCP server. 🛠️

*   **Modify the script:** Ensure the `to=` number in `/home/rj/Code/mcp-generated/twilio_test.py` is a WhatsApp number linked to your Twilio Sandbox (if using the Sandbox) or any valid WhatsApp number (if using a purchased Twilio number). The `from_` number should typically be your Twilio Sandbox number (`whatsapp:+14155238886`) or your purchased Twilio WhatsApp number.
*   **Run the script:**
    ```bash ▶️
    python /home/rj/Code/mcp-generated/twilio_test.py
    ```
    This will attempt to send a hardcoded message ("Is this working?") from the specified Twilio number to the specified recipient.