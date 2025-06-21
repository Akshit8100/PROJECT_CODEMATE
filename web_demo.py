#!/usr/bin/env python3
"""
Web-based Demo Interface
Run this to see the pipeline in your browser!
"""

import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from working_demo import SimpleQueryProcessor, SimpleExecutionEngine

class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Function Calling Pipeline - Live Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .query-box { margin: 20px 0; }
        input[type="text"] { width: 70%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; font-size: 16px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px; }
        button:hover { background: #2980b9; }
        .results { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; border-left: 4px solid #3498db; }
        .function-call { margin: 10px 0; padding: 10px; background: #e8f4fd; border-radius: 3px; }
        .success { color: #27ae60; }
        .error { color: #e74c3c; }
        .examples { margin: 20px 0; }
        .example-btn { margin: 5px; padding: 8px 15px; background: #95a5a6; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 14px; }
        .example-btn:hover { background: #7f8c8d; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Function Calling Pipeline - Live Demo</h1>
        <p><strong>Try natural language queries and see the AI process them in real-time!</strong></p>

        <div class="examples">
            <h3>Try these example queries:</h3>
            <button class="example-btn" onclick="setQuery('What time is it?')">What time is it?</button>
            <button class="example-btn" onclick="setQuery('Read invoice data and calculate totals')">Read invoice data</button>
            <button class="example-btn" onclick="setQuery('Get system information')">Get system info</button>
            <button class="example-btn" onclick="setQuery('Process March invoices and send email summary')">Complex: March invoices</button>
            <button class="example-btn" onclick="setQuery('Read CSV data file')">Read CSV data</button>
        </div>
        
        <div class="query-box">
            <input type="text" id="queryInput" placeholder="Enter your natural language query here..." value="">
            <button onclick="processQuery()">Process Query</button>
        </div>

        <div id="status"></div>
        <div id="results"></div>
    </div>

    <script>
        function setQuery(query) {
            document.getElementById('queryInput').value = query;
        }

        async function processQuery() {
            const query = document.getElementById('queryInput').value.trim();
            if (!query) {
                alert('Please enter a query!');
                return;
            }

            const statusDiv = document.getElementById('status');
            const resultsDiv = document.getElementById('results');

            statusDiv.innerHTML = '<div class="status">Processing query: "' + query + '"...</div>';
            resultsDiv.innerHTML = '';

            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });

                const result = await response.json();

                if (result.success) {
                    statusDiv.innerHTML = '<div class="status success">Query processed successfully!</div>';
                    displayResults(result);
                } else {
                    statusDiv.innerHTML = '<div class="status error">Error: ' + result.error + '</div>';
                }
            } catch (error) {
                statusDiv.innerHTML = '<div class="status error">Network error: ' + error.message + '</div>';
            }
        }
        
        function displayResults(result) {
            const resultsDiv = document.getElementById('results');

            let html = '<div class="results">';
            html += '<h3>AI Analysis</h3>';
            html += '<p><strong>Plan:</strong> ' + result.plan.plan + '</p>';
            html += '<p><strong>Functions:</strong> ' + result.plan.function_calls.length + '</p>';

            html += '<h3>Function Sequence</h3>';
            result.plan.function_calls.forEach((call, i) => {
                html += '<div class="function-call">';
                html += '<strong>' + (i+1) + '. ' + call.function_name + '</strong><br>';
                html += call.description;
                html += '</div>';
            });

            if (result.execution) {
                html += '<h3>Execution Results</h3>';
                html += '<p><strong>Overall Success:</strong> ' + (result.execution.success ? 'Yes' : 'No') + '</p>';
                html += '<p><strong>Completed:</strong> ' + result.execution.execution_summary.successful_functions + '/' + result.execution.execution_summary.total_functions + ' functions</p>';

                html += '<h3>Detailed Results</h3>';
                result.execution.results.forEach(res => {
                    const status = res.success ? 'success' : 'error';
                    const icon = res.success ? '[SUCCESS]' : '[ERROR]';
                    html += '<div class="function-call ' + status + '">';
                    html += '<strong>' + icon + ' ' + res.function_name + '</strong><br>';

                    if (res.success) {
                        if (res.datetime) {
                            html += 'Time: ' + res.datetime.formatted + ' (' + res.datetime.weekday + ')';
                        } else if (res.data && Array.isArray(res.data)) {
                            html += 'Loaded ' + res.data.length + ' records';
                        } else if (res.summary) {
                            html += 'Total: $' + res.summary.sum.toFixed(2) + '<br>';
                            html += 'Count: ' + res.summary.count + ' items';
                        } else if (res.message) {
                            html += 'Message: ' + res.message;
                        } else if (res.system_info) {
                            html += 'System: ' + res.system_info.system + '<br>';
                            html += 'Python: ' + res.system_info.python_version;
                        }
                    } else {
                        html += 'Error: ' + (res.error || 'Unknown error');
                    }
                    html += '</div>';
                });
            }
            
            html += '</div>';
            resultsDiv.innerHTML = html;
        }
        
        // Allow Enter key to submit
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                processQuery();
            }
        });
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode())
            
        elif self.path == '/process':
            # This will be handled by do_POST
            pass
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/process':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                query = data.get('query', '')
                
                # Process the query
                result = asyncio.run(self.process_query_async(query))
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                error_result = {
                    'success': False,
                    'error': str(e)
                }
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(error_result).encode())
    
    async def process_query_async(self, query):
        """Process query asynchronously"""
        try:
            # Process query
            processor = SimpleQueryProcessor()
            plan = processor.process_query(query)
            
            # Execute plan
            engine = SimpleExecutionEngine()
            execution_result = await engine.execute_plan(plan)
            
            return {
                'success': True,
                'plan': plan,
                'execution': execution_result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def main():
    print("Starting AI Function Calling Pipeline Web Demo...")
    print("=" * 60)

    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, DemoHandler)

    print(f"Web demo server starting on http://localhost:8080")
    print("Open your browser and go to: http://localhost:8080")
    print("Try different queries and see the AI process them live!")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped. Thanks for trying the demo!")

if __name__ == "__main__":
    main()
