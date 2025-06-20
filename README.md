# MCP Smart Function Pipeline Server

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

## 🚀 Usage

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

### API Endpoints

#### 1. Health Check

```bash
GET /health
```

#### 2. List Functions

```bash
GET /functions
```

#### 3. Execute Query

```bash
POST /execute
Content-Type: application/json

{
  "query": "Retrieve all invoices for March, summarize the total amount, and send the summary to my email"
}
```

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

## 📚 Example Queries

### Invoice Management

```
"Retrieve all invoices for March, summarize the total amount, and send the summary to my email"
"Get invoices for January and filter those above $2000"
"Calculate total revenue from all invoices this month"
```

### Data Processing

```
"Group invoices by status and save the results to a file"
"Convert invoice amounts from USD to EUR"
"Filter invoices by date range and calculate totals"
```

### Email & Reporting

```
"Generate a monthly invoice report and email it to the finance team"
"Send a summary of overdue invoices to the manager"
```

## 🔧 Available Functions

The system includes 50+ functions across categories:

### Invoice Functions

- `get_invoices(month)` - Retrieve invoices
- `filter_invoices_by_amount(invoices, min_amount)` - Filter by amount
- `summarize_invoices(invoices)` - Generate summaries

### Data Processing

- `calculate_total(items, field)` - Calculate totals
- `group_by_field(data, field)` - Group data
- `filter_by_date_range(data, date_field, start_date, end_date)` - Date filtering

### Communication

- `send_email(content, recipient, subject)` - Send emails

### File Operations

- `save_to_file(data, filename)` - Save data
- `read_from_file(filename)` - Read data

### Utilities

- `convert_currency(amount, from_currency, to_currency)` - Currency conversion

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

## 🧪 Testing

```bash
# Run the test client
python client_example.py

# Test specific endpoints
curl http://localhost:5000/health
curl http://localhost:5000/functions
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your functions to `src/function_library.py`
4. Update documentation
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Ollama not responding**

   - Ensure Ollama is running: `ollama serve`
   - Check model is pulled: `ollama pull mistral:7b`

2. **Function not found errors**

   - Check function names in `/functions` endpoint
   - Verify function registration in `FunctionLibrary`

3. **Variable resolution errors**
   - Check output variable references (`$output_0.field`)
   - Ensure previous functions produce expected outputs

### Debug Mode

Run with `--debug` flag for detailed logs:

```bash
python main.py --debug
```

## 🔮 Future Enhancements

- [ ] Function hot-reloading
- [ ] Multi-model support
- [ ] Function marketplace
- [ ] Graphical pipeline builder
- [ ] Real-time execution monitoring
- [ ] Function versioning
- [ ] Performance metrics
