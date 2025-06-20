#!/usr/bin/env python3
"""
Main entry point for the MCP Smart Function Pipeline Server
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_server import MCPServer


def main():
    """Main function to run the MCP server."""
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='MCP Smart Function Pipeline Server')
    parser.add_argument('--host', default='localhost', help='Host to bind to (default: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--model', default='mistral:7b', help='Ollama model to use (default: mistral:7b)')
    parser.add_argument('--ollama-host', default='http://localhost:11434', 
                       help='Ollama host URL (default: http://localhost:11434)')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    print("🚀 Starting MCP Smart Function Pipeline Server")
    print(f"   Model: {args.model}")
    print(f"   Ollama Host: {args.ollama_host}")
    print(f"   Server: http://{args.host}:{args.port}")
    print()
    
    # Create and run the server
    try:
        server = MCPServer(model_name=args.model, ollama_host=args.ollama_host)
        server.run(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
