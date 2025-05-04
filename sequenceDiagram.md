```mermaid

sequenceDiagram
    participant User
    participant test.py
    participant OpenAI API
    participant MCPClient (in test.py)
    participant whatsapp_server.py (subprocess)
    participant Twilio API

    User->>+test.py: Run script `python /home/rj/Code/mcp-generated/test.py`
    test.py->>test.py: Load .env (OpenAI Key, Twilio details implicitly needed by server)
    test.py->>test.py: Define 'send_whatsapp' tool structure
    test.py->>+OpenAI API: Send user_prompt + tool definition
    OpenAI API-->>-test.py: Return tool_call request ('send_whatsapp', args)

    alt Tool Call Requested
        test.py->>+MCPClient: Create MCPClient(run_command='python /home/rj/Code/mcp-generated/whatsapp_server.py')
        Note over MCPClient, whatsapp_server.py (subprocess): MCPClient starts whatsapp_server.py in a parallel subprocess
        MCPClient->>+whatsapp_server.py (subprocess): Start Process
        whatsapp_server.py (subprocess)->>whatsapp_server.py (subprocess): Initialize (Load settings, Twilio Client, Define tool)
        whatsapp_server.py (subprocess)-->>-MCPClient: Ready (Implicitly, listening on stdio)

        test.py->>MCPClient: call_tool('send_whatsapp', **args)
        MCPClient->>+whatsapp_server.py (subprocess): Send tool call request via stdio
        whatsapp_server.py (subprocess)->>whatsapp_server.py (subprocess): Execute send_whatsapp(to_number, message)
        whatsapp_server.py (subprocess)->>+Twilio API: Create message (from_, to, body)
        Twilio API-->>-whatsapp_server.py (subprocess): Return message SID or Error
        whatsapp_server.py (subprocess)->>whatsapp_server.py (subprocess): Format success/error result string
        whatsapp_server.py (subprocess)-->>-MCPClient: Send result string via stdio

        MCPClient-->>-test.py: Return result from server
        test.py->>User: Print result from MCP Server
        Note over MCPClient, whatsapp_server.py (subprocess): MCPClient terminates the subprocess when done
        MCPClient->>whatsapp_server.py (subprocess): Terminate Process (Implicit)
        deactivate MCPClient
    else No Tool Call
        test.py->>User: Print OpenAI's text response
    end
    deactivate test.py

```