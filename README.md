# MCP Smart Function Pipeline Server

[![FlavorFrame Demo](resources/animate.gif)](https://drive.google.com/file/d/1Z99_fW7N0NIObEFBsWZJjD01Mpfzqb9_/view?usp=drive_link)

🌐 **Watch it now:** [Video](https://drive.google.com/file/d/1Z99_fW7N0NIObEFBsWZJjD01Mpfzqb9_/view?usp=drive_link) 👆


A Model Context Protocol (MCP) server that uses local LLM (Ollama with Mistral 7B) to interpret natural language queries and execute structured function call pipelines.

## 🚀 Features

- **Natural Language Processing**: Uses Ollama with Mistral 7B to parse user queries
- **Function Pipeline Execution**: Orchestrates complex multi-step workflows
- **50+ Built-in Functions**: Invoice management, data processing, email, file operations, etc.
- **RESTful API**: Easy integration with web interfaces and external systems
- **Data Flow Management**: Automatic variable resolution and output chaining
- **Execution Planning**: Dry-run capability to validate pipelines before execution
- **Error Handling**: Comprehensive error handling and logging

## 🏗️ Architecture

```
User Query → AI Model (Mistral 7B) → Function Planner → Execution Engine → Results
                ↓
         Function Library (50+ functions)
```

## 📋 Prerequisites

1. **Python 3.8+**
2. **Ollama installed locally** with Mistral 7B model
   ```bash
   # Install Ollama (https://ollama.ai/)
   ollama pull mistral:7b
   ```

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd codemate-smart-function-pipeline
   ```

2. **Create virtual environment**

   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file as needed
   ```

## Usage

### Starting the Server

```bash
# Basic start
python main.py

# With custom configuration
python main.py --host 0.0.0.0 --port 8080 --model mistral:7b

# Debug mode
python main.py --debug
```

### Using the Client

```bash
# Run the interactive test client
python client_example.py
```


```bash
GET /functions
```

#### 3. Execute Query


#### 4. Plan Query (Dry Run)

```bash
POST /plan
Content-Type: application/json

{
  "query": "Get invoices for January and calculate total"
}
```

#### 5. Execute Function Plan

```bash
POST /execute-plan
Content-Type: application/json

{
  "function_calls": [
    {"function": "get_invoices", "inputs": {"month": "March"}},
    {"function": "summarize_invoices", "inputs": {"invoices": "$output_0.invoices"}}
  ]
}
```




## 🔄 Data Flow Example

```json
User Query: "Get March invoices, summarize them, and email the summary"

Generated Plan:
[
  {"function": "get_invoices", "inputs": {"month": "March"}},
  {"function": "summarize_invoices", "inputs": {"invoices": "$output_0.invoices"}},
  {"function": "send_email", "inputs": {"content": "$output_1.summary", "recipient": "user@example.com", "subject": "Invoice Summary"}}
]

Execution:
1. get_invoices("March") → output_0: {"invoices": [...]}
2. summarize_invoices(output_0.invoices) → output_1: {"summary": {...}}
3. send_email(output_1.summary, "user@example.com", "Invoice Summary") → output_2: {"status": "sent"}
```

## 🛡️ Error Handling

- **Validation**: Function calls are validated before execution
- **Graceful Failures**: Partial execution results are preserved
- **Detailed Logging**: Comprehensive execution logs
- **Fallback Parsing**: Backup parsing if AI model fails

## 🔧 Configuration

### Environment Variables

| Variable       | Description         | Default                  |
| -------------- | ------------------- | ------------------------ |
| `OLLAMA_HOST`  | Ollama server URL   | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model name          | `mistral:7b`             |
| `SERVER_HOST`  | Server bind address | `localhost`              |
| `SERVER_PORT`  | Server port         | `5000`                   |
| `DEBUG_MODE`   | Enable debug mode   | `false`                  |


## Long Query: 
```
Retrieve all invoices for March, summarize them, and send the summary to shashank.pandey_cs22@gla.ac.in email.
```