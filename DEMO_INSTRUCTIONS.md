# Demo Instructions for AI Function Calling Pipeline

## 🎥 Video Demo Preparation

### Prerequisites
1. **Python Installation**: Ensure Python 3.8+ is installed
2. **Dependencies**: Install required packages using `pip install -r requirements.txt`
3. **Environment**: Set up `.env` file with any required API keys (optional for demo)

### Demo Script Execution

#### Option 1: Automated Demo Script
```bash
python demo_script.py
```
This runs a comprehensive demonstration showing:
- Pipeline initialization
- Function library overview
- Query processing examples
- Execution results

#### Option 2: Interactive CLI Demo
```bash
python main.py interactive
```
Then try these example queries:
1. `"What time is it?"`
2. `"Read the sample invoices CSV file"`
3. `"Get system information"`
4. `"Calculate 25 * 4 + 10"`
5. `"List files in the data directory"`

#### Option 3: Single Query Demo
```bash
python main.py query "Retrieve all invoices for March, summarize the total amount, and send the summary to my email"
```

#### Option 4: Batch Processing Demo
```bash
python main.py batch examples/batch_queries.txt
```

### Key Demo Points to Highlight

#### 1. **Architecture Overview** (2-3 minutes)
- Show the project structure
- Explain the 4 main components:
  - Function Library (50+ functions)
  - AI Model Integration
  - Query Processor
  - Execution Engine

#### 2. **Function Library Showcase** (3-4 minutes)
- Demonstrate the 8 function categories
- Show examples from each category:
  - Data Processing: `read_csv`, `filter_data`, `summarize_data`
  - Communication: `send_email`, `get_weather`
  - File Operations: `read_file`, `write_file`, `list_directory`
  - Web Operations: `fetch_web_page`, `download_file`
  - System Operations: `get_system_info`, `monitor_system_resources`
  - Math Operations: `calculate`, `convert_units`
  - Text Operations: `analyze_text`, `extract_patterns`
  - DateTime Operations: `get_current_time`, `calculate_date_difference`

#### 3. **Query Processing Demo** (4-5 minutes)
Show the complete pipeline with this example:
```
Query: "Retrieve all invoices for March, summarize the total amount, and send the summary to my email"

Expected Function Sequence:
1. read_csv('data/sample_invoices.csv')
2. filter_data(data, 'month', 'equals', 'March')
3. summarize_data(filtered_data, 'amount')
4. send_email('abhayrajputcse@gmail.com', 'Invoice Summary', summary)
```

#### 4. **AI Model Integration** (2-3 minutes)
- Explain model selection (Mistral 7B, DialoGPT, GPT-2)
- Show function calling capabilities
- Demonstrate fallback mechanisms

#### 5. **Execution Engine** (2-3 minutes)
- Show input/output mapping between functions
- Demonstrate error handling
- Show simulation vs real execution

### Sample Demo Queries

#### Simple Queries (Good for starting)
- `"What time is it?"`
- `"Get system information"`
- `"Calculate 2 + 2"`
- `"List files in current directory"`

#### Medium Complexity
- `"Read the sales data and calculate average per region"`
- `"Get weather for New York and save to file"`
- `"Analyze text in readme.txt and extract emails"`

#### Complex Queries (Showcase full capability)
- `"Retrieve all invoices for March, summarize the total amount, and send the summary to my email"`
- `"Monitor system resources, check if CPU usage is above 80%, and send alert if needed"`
- `"Download latest news, analyze sentiment, and create summary report"`

### Expected Demo Flow (10-12 minutes total)

1. **Introduction** (1 min)
   - Project overview and objectives
   - Key features highlight

2. **Architecture Walkthrough** (2 min)
   - Show project structure
   - Explain component relationships

3. **Function Library Demo** (2 min)
   - Show available functions
   - Demonstrate function categories

4. **Live Query Processing** (4 min)
   - Process 2-3 queries of increasing complexity
   - Show generated plans and execution

5. **Advanced Features** (2 min)
   - Batch processing
   - Error handling
   - Simulation mode

6. **Conclusion** (1 min)
   - Summarize capabilities
   - Mention extensibility and future enhancements

### Troubleshooting

#### If Models Don't Load
- The demo script automatically falls back to simulation mode
- All functionality is demonstrated without actual model inference
- Mention this is due to hardware/memory constraints

#### If Dependencies Fail
- Use the provided `requirements.txt` with minimal dependencies
- Focus on architecture and code structure
- Show test results instead of live execution

#### Performance Considerations
- Mention that larger models (7B) require 16GB+ RAM
- Smaller models (355M) work on most systems
- GPU acceleration significantly improves performance

### Video Recording Tips

1. **Screen Setup**
   - Use high resolution (1920x1080 minimum)
   - Increase terminal font size for visibility
   - Use dark theme for better contrast

2. **Audio**
   - Explain what you're doing as you go
   - Mention key technical decisions
   - Highlight innovative aspects

3. **Pacing**
   - Allow time for viewers to read output
   - Pause between major sections
   - Repeat important points

4. **Code Highlights**
   - Show key files: `function_calling.py`, `pipeline_manager.py`
   - Demonstrate modular architecture
   - Highlight the 50+ function implementations

### Post-Demo

1. **GitHub Repository**
   - Ensure all code is committed
   - Add collaborators: Kshitij, Ayush, Shama
   - Include comprehensive README

2. **Documentation**
   - API documentation for functions
   - Setup and installation guide
   - Usage examples and tutorials

3. **Future Enhancements**
   - Mention possible improvements
   - Discuss scalability considerations
   - Highlight research opportunities
