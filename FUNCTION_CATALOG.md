# AI Function Calling Pipeline - Complete Function Catalog

## Overview
This document provides a comprehensive catalog of all 55+ functions available in the AI Function Calling Pipeline. Each function is clearly described with its inputs, outputs, and usage examples.

## Function Categories

### 1. DATA PROCESSING FUNCTIONS (9 functions)

#### 1.1 read_csv
- **Description**: Read data from a CSV file
- **Inputs**: 
  - `file_path` (string): Path to the CSV file
- **Outputs**: 
  - `success` (boolean): Operation success status
  - `data` (list): List of dictionaries representing rows
  - `shape` (tuple): Number of rows and columns
  - `columns` (list): Column names
- **Example**: `read_csv("data/sales.csv")`

#### 1.2 filter_data
- **Description**: Filter data based on specified criteria
- **Inputs**:
  - `data` (list): Input data to filter
  - `column` (string): Column name to filter on
  - `operator` (string): Filter operator (equals, contains, greater_than, less_than)
  - `value` (any): Value to filter by
- **Outputs**:
  - `success` (boolean): Operation success status
  - `data` (list): Filtered data
  - `count` (integer): Number of filtered rows
- **Example**: `filter_data(data, "status", "equals", "active")`

#### 1.3 summarize_data
- **Description**: Calculate statistical summaries for numerical columns
- **Inputs**:
  - `data` (list): Input data
  - `column` (string): Column name to summarize
- **Outputs**:
  - `success` (boolean): Operation success status
  - `summary` (dict): Statistical summary (count, sum, mean, min, max, std)
- **Example**: `summarize_data(data, "amount")`

#### 1.4 group_by
- **Description**: Group data by specified column and calculate aggregations
- **Inputs**:
  - `data` (list): Input data
  - `column` (string): Column to group by
  - `agg_column` (string): Column to aggregate
  - `agg_function` (string): Aggregation function (sum, mean, count, min, max)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `grouped_data` (list): Grouped and aggregated data
- **Example**: `group_by(data, "category", "sales", "sum")`

#### 1.5 query_database
- **Description**: Execute SQL queries on a database
- **Inputs**:
  - `query` (string): SQL query to execute
  - `database_path` (string): Path to database file
- **Outputs**:
  - `success` (boolean): Operation success status
  - `data` (list): Query results
  - `row_count` (integer): Number of rows returned
- **Example**: `query_database("SELECT * FROM users WHERE age > 25", "data/app.db")`

#### 1.6 sort_data
- **Description**: Sort data by specified column
- **Inputs**:
  - `data` (list): Input data
  - `column` (string): Column to sort by
  - `ascending` (boolean): Sort order (default: true)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `data` (list): Sorted data
- **Example**: `sort_data(data, "date", false)`

#### 1.7 join_data
- **Description**: Join two datasets on a common key
- **Inputs**:
  - `data1` (list): First dataset
  - `data2` (list): Second dataset
  - `key` (string): Common key column
  - `join_type` (string): Type of join (inner, left, right, outer)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `data` (list): Joined data
- **Example**: `join_data(customers, orders, "customer_id", "inner")`

#### 1.8 validate_data
- **Description**: Validate data against specified rules
- **Inputs**:
  - `data` (list): Input data to validate
  - `rules` (dict): Validation rules for each column
- **Outputs**:
  - `success` (boolean): Operation success status
  - `validation_results` (list): Validation results per row
  - `valid_rows` (integer): Number of valid rows
  - `errors` (list): List of validation errors
- **Example**: `validate_data(data, {"age": {"type": "number", "min": 0, "max": 120}})`

#### 1.9 transform_data
- **Description**: Transform data by applying functions to columns
- **Inputs**:
  - `data` (list): Input data
  - `transformations` (dict): Column transformations to apply
- **Outputs**:
  - `success` (boolean): Operation success status
  - `data` (list): Transformed data
  - `transformations_applied` (dict): Applied transformations
- **Example**: `transform_data(data, {"name": "uppercase", "amount": "round"})`

### 2. COMMUNICATION FUNCTIONS (7 functions)

#### 2.1 send_email
- **Description**: Send email messages
- **Inputs**:
  - `to_email` (string): Recipient email address
  - `subject` (string): Email subject
  - `body` (string): Email body content
  - `from_email` (string, optional): Sender email
- **Outputs**:
  - `success` (boolean): Operation success status
  - `message_id` (string): Email message ID
- **Example**: `send_email("abhayrajputcse@gmail.com", "Report", "Monthly sales report attached")`

#### 2.2 send_sms
- **Description**: Send SMS text messages
- **Inputs**:
  - `phone_number` (string): Recipient phone number
  - `message` (string): SMS message content
- **Outputs**:
  - `success` (boolean): Operation success status
  - `message_id` (string): SMS message ID
- **Example**: `send_sms("+1234567890", "Alert: System maintenance scheduled")`

#### 2.3 make_http_request
- **Description**: Make HTTP requests to web APIs
- **Inputs**:
  - `url` (string): Target URL
  - `method` (string): HTTP method (GET, POST, PUT, DELETE)
  - `data` (dict, optional): Request payload
  - `headers` (dict, optional): Request headers
- **Outputs**:
  - `success` (boolean): Operation success status
  - `status_code` (integer): HTTP status code
  - `data` (any): Response data
- **Example**: `make_http_request("https://api.example.com/data", "GET")`

#### 2.4 post_to_slack
- **Description**: Post messages to Slack channels
- **Inputs**:
  - `channel` (string): Slack channel name
  - `message` (string): Message content
  - `username` (string, optional): Bot username
- **Outputs**:
  - `success` (boolean): Operation success status
  - `timestamp` (string): Message timestamp
- **Example**: `post_to_slack("#alerts", "System backup completed successfully")`

#### 2.5 send_notification
- **Description**: Send system notifications
- **Inputs**:
  - `title` (string): Notification title
  - `message` (string): Notification message
  - `priority` (string, optional): Priority level (low, normal, high)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `notification_id` (string): Notification ID
- **Example**: `send_notification("Alert", "Disk space running low", "high")`

#### 2.6 get_weather
- **Description**: Get weather information for a location
- **Inputs**:
  - `location` (string): Location name or coordinates
  - `units` (string, optional): Temperature units (celsius, fahrenheit)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `weather` (dict): Weather information
- **Example**: `get_weather("New York", "celsius")`

#### 2.7 get_news
- **Description**: Fetch news articles
- **Inputs**:
  - `category` (string, optional): News category
  - `count` (integer, optional): Number of articles
  - `language` (string, optional): Language code
- **Outputs**:
  - `success` (boolean): Operation success status
  - `articles` (list): List of news articles
- **Example**: `get_news("technology", 5, "en")`

### 3. FILE OPERATIONS FUNCTIONS (10 functions)

#### 3.1 read_file
- **Description**: Read content from a text file
- **Inputs**:
  - `file_path` (string): Path to the file
  - `encoding` (string, optional): File encoding (default: utf-8)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `content` (string): File content
  - `lines` (integer): Number of lines
- **Example**: `read_file("documents/report.txt")`

#### 3.2 write_file
- **Description**: Write content to a text file
- **Inputs**:
  - `file_path` (string): Path to the file
  - `content` (string): Content to write
  - `mode` (string, optional): Write mode (write, append)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `bytes_written` (integer): Number of bytes written
- **Example**: `write_file("output/summary.txt", "Analysis complete", "write")`

#### 3.3 copy_file
- **Description**: Copy a file from source to destination
- **Inputs**:
  - `source_path` (string): Source file path
  - `destination_path` (string): Destination file path
- **Outputs**:
  - `success` (boolean): Operation success status
  - `size` (integer): File size copied
- **Example**: `copy_file("data/original.csv", "backup/original_backup.csv")`

#### 3.4 delete_file
- **Description**: Delete a file
- **Inputs**:
  - `file_path` (string): Path to the file to delete
- **Outputs**:
  - `success` (boolean): Operation success status
  - `message` (string): Deletion confirmation
- **Example**: `delete_file("temp/cache.tmp")`

#### 3.5 list_directory
- **Description**: List contents of a directory
- **Inputs**:
  - `directory_path` (string): Path to the directory
  - `include_hidden` (boolean, optional): Include hidden files
- **Outputs**:
  - `success` (boolean): Operation success status
  - `files` (list): List of files
  - `directories` (list): List of subdirectories
- **Example**: `list_directory("data/", false)`

#### 3.6 create_directory
- **Description**: Create a new directory
- **Inputs**:
  - `directory_path` (string): Path for the new directory
  - `recursive` (boolean, optional): Create parent directories if needed
- **Outputs**:
  - `success` (boolean): Operation success status
  - `path` (string): Created directory path
- **Example**: `create_directory("output/reports/2024", true)`

#### 3.7 read_json
- **Description**: Read and parse JSON file
- **Inputs**:
  - `file_path` (string): Path to JSON file
- **Outputs**:
  - `success` (boolean): Operation success status
  - `data` (any): Parsed JSON data
- **Example**: `read_json("config/settings.json")`

#### 3.8 write_json
- **Description**: Write data to JSON file
- **Inputs**:
  - `file_path` (string): Path to JSON file
  - `data` (any): Data to write
  - `indent` (integer, optional): JSON indentation
- **Outputs**:
  - `success` (boolean): Operation success status
  - `size` (integer): File size written
- **Example**: `write_json("output/results.json", results, 2)`

#### 3.9 read_excel
- **Description**: Read data from Excel file
- **Inputs**:
  - `file_path` (string): Path to Excel file
  - `sheet_name` (string, optional): Sheet name to read
- **Outputs**:
  - `success` (boolean): Operation success status
  - `data` (list): Excel data as list of dictionaries
  - `sheets` (list): Available sheet names
- **Example**: `read_excel("data/sales.xlsx", "Q1_Sales")`

#### 3.10 get_file_info
- **Description**: Get information about a file
- **Inputs**:
  - `file_path` (string): Path to the file
- **Outputs**:
  - `success` (boolean): Operation success status
  - `info` (dict): File information (size, modified date, permissions)
- **Example**: `get_file_info("documents/report.pdf")`

### 4. WEB OPERATIONS FUNCTIONS (8 functions)

#### 4.1 fetch_web_page
- **Description**: Fetch content from a web page
- **Inputs**:
  - `url` (string): URL to fetch
  - `timeout` (integer, optional): Request timeout in seconds
- **Outputs**:
  - `success` (boolean): Operation success status
  - `content` (string): Page content
  - `status_code` (integer): HTTP status code
- **Example**: `fetch_web_page("https://example.com")`

#### 4.2 extract_links
- **Description**: Extract all links from a web page
- **Inputs**:
  - `url` (string): URL to extract links from
  - `internal_only` (boolean, optional): Extract only internal links
- **Outputs**:
  - `success` (boolean): Operation success status
  - `links` (list): List of extracted links
- **Example**: `extract_links("https://example.com", true)`

#### 4.3 download_file
- **Description**: Download a file from URL
- **Inputs**:
  - `url` (string): File URL
  - `file_path` (string): Local path to save file
- **Outputs**:
  - `success` (boolean): Operation success status
  - `size` (integer): Downloaded file size
- **Example**: `download_file("https://example.com/data.csv", "downloads/data.csv")`

#### 4.4 check_website_status
- **Description**: Check if a website is accessible
- **Inputs**:
  - `url` (string): Website URL to check
- **Outputs**:
  - `success` (boolean): Operation success status
  - `status_code` (integer): HTTP status code
  - `response_time` (float): Response time in seconds
- **Example**: `check_website_status("https://example.com")`

#### 4.5 extract_text_from_html
- **Description**: Extract plain text from HTML content
- **Inputs**:
  - `html_content` (string): HTML content
  - `remove_scripts` (boolean, optional): Remove script tags
- **Outputs**:
  - `success` (boolean): Operation success status
  - `text` (string): Extracted plain text
- **Example**: `extract_text_from_html(html_content, true)`

#### 4.6 search_web
- **Description**: Search the web using a search engine
- **Inputs**:
  - `query` (string): Search query
  - `num_results` (integer, optional): Number of results to return
- **Outputs**:
  - `success` (boolean): Operation success status
  - `results` (list): Search results with titles, URLs, and snippets
- **Example**: `search_web("AI function calling", 10)`

#### 4.7 validate_url
- **Description**: Validate if a URL is properly formatted
- **Inputs**:
  - `url` (string): URL to validate
- **Outputs**:
  - `success` (boolean): Operation success status
  - `is_valid` (boolean): URL validity
  - `scheme` (string): URL scheme
  - `domain` (string): Domain name
- **Example**: `validate_url("https://example.com/path")`

#### 4.8 get_webpage_metadata
- **Description**: Extract metadata from a web page
- **Inputs**:
  - `url` (string): Web page URL
- **Outputs**:
  - `success` (boolean): Operation success status
  - `metadata` (dict): Page metadata (title, description, keywords)
- **Example**: `get_webpage_metadata("https://example.com")`

### 5. SYSTEM OPERATIONS FUNCTIONS (8 functions)

#### 5.1 execute_command
- **Description**: Execute system commands
- **Inputs**:
  - `command` (string): Command to execute
  - `timeout` (integer, optional): Command timeout in seconds
- **Outputs**:
  - `success` (boolean): Operation success status
  - `output` (string): Command output
  - `return_code` (integer): Command return code
- **Example**: `execute_command("ls -la", 30)`

#### 5.2 get_system_info
- **Description**: Get system information
- **Inputs**: None
- **Outputs**:
  - `success` (boolean): Operation success status
  - `system_info` (dict): System information (OS, CPU, memory, disk)
- **Example**: `get_system_info()`

#### 5.3 get_process_list
- **Description**: Get list of running processes
- **Inputs**:
  - `limit` (integer, optional): Maximum number of processes to return
- **Outputs**:
  - `success` (boolean): Operation success status
  - `processes` (list): List of running processes
- **Example**: `get_process_list(20)`

#### 5.4 get_environment_variable
- **Description**: Get environment variable value
- **Inputs**:
  - `variable_name` (string): Environment variable name
- **Outputs**:
  - `success` (boolean): Operation success status
  - `value` (string): Variable value
- **Example**: `get_environment_variable("PATH")`

#### 5.5 set_environment_variable
- **Description**: Set environment variable
- **Inputs**:
  - `variable_name` (string): Environment variable name
  - `value` (string): Variable value
- **Outputs**:
  - `success` (boolean): Operation success status
  - `message` (string): Confirmation message
- **Example**: `set_environment_variable("API_KEY", "secret123")`

#### 5.6 get_current_directory
- **Description**: Get current working directory
- **Inputs**: None
- **Outputs**:
  - `success` (boolean): Operation success status
  - `directory` (string): Current directory path
- **Example**: `get_current_directory()`

#### 5.7 change_directory
- **Description**: Change current working directory
- **Inputs**:
  - `directory_path` (string): New directory path
- **Outputs**:
  - `success` (boolean): Operation success status
  - `new_directory` (string): New current directory
- **Example**: `change_directory("/home/user/projects")`

#### 5.8 monitor_system_resources
- **Description**: Monitor system resource usage
- **Inputs**: None
- **Outputs**:
  - `success` (boolean): Operation success status
  - `resources` (dict): Resource usage (CPU, memory, disk, network)
- **Example**: `monitor_system_resources()`

### 6. MATH OPERATIONS FUNCTIONS (5 functions)

#### 6.1 calculate
- **Description**: Evaluate mathematical expressions
- **Inputs**:
  - `expression` (string): Mathematical expression to evaluate
- **Outputs**:
  - `success` (boolean): Operation success status
  - `result` (number): Calculation result
  - `expression` (string): Original expression
- **Example**: `calculate("2 + 3 * sqrt(16)")`

#### 6.2 calculate_statistics
- **Description**: Calculate statistical measures for a list of numbers
- **Inputs**:
  - `numbers` (list): List of numbers
- **Outputs**:
  - `success` (boolean): Operation success status
  - `statistics` (dict): Statistical measures (mean, median, std, etc.)
- **Example**: `calculate_statistics([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])`

#### 6.3 convert_units
- **Description**: Convert between different units of measurement
- **Inputs**:
  - `value` (number): Value to convert
  - `from_unit` (string): Source unit
  - `to_unit` (string): Target unit
  - `unit_type` (string): Type of unit (length, weight, temperature)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `converted_value` (number): Converted value
- **Example**: `convert_units(100, "fahrenheit", "celsius", "temperature")`

#### 6.4 generate_sequence
- **Description**: Generate mathematical sequences
- **Inputs**:
  - `sequence_type` (string): Type of sequence (arithmetic, geometric, fibonacci, prime)
  - `start` (integer): Starting value
  - `count` (integer): Number of terms
  - `step` (integer, optional): Step size for arithmetic/geometric sequences
- **Outputs**:
  - `success` (boolean): Operation success status
  - `sequence` (list): Generated sequence
- **Example**: `generate_sequence("fibonacci", 0, 10)`

#### 6.5 solve_equation
- **Description**: Solve simple mathematical equations
- **Inputs**:
  - `equation_type` (string): Type of equation (linear, quadratic)
  - Additional parameters based on equation type
- **Outputs**:
  - `success` (boolean): Operation success status
  - `solutions` (list): Equation solutions
- **Example**: `solve_equation("quadratic", a=1, b=-5, c=6)`

### 7. TEXT OPERATIONS FUNCTIONS (7 functions)

#### 7.1 analyze_text
- **Description**: Analyze text and provide statistics
- **Inputs**:
  - `text` (string): Text to analyze
- **Outputs**:
  - `success` (boolean): Operation success status
  - `analysis` (dict): Text analysis (word count, character count, etc.)
- **Example**: `analyze_text("Hello world! This is a sample text.")`

#### 7.2 find_replace
- **Description**: Find and replace text using patterns
- **Inputs**:
  - `text` (string): Input text
  - `find_pattern` (string): Pattern to find
  - `replace_with` (string): Replacement text
  - `use_regex` (boolean, optional): Use regular expressions
  - `case_sensitive` (boolean, optional): Case sensitive search
- **Outputs**:
  - `success` (boolean): Operation success status
  - `result_text` (string): Text after replacement
  - `replacements_made` (integer): Number of replacements
- **Example**: `find_replace("Hello World", "World", "Universe", false, true)`

#### 7.3 extract_patterns
- **Description**: Extract patterns from text using regex
- **Inputs**:
  - `text` (string): Input text
  - `pattern` (string): Regex pattern or pattern type
  - `pattern_type` (string, optional): Predefined pattern type (email, phone, url)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `matches` (list): Extracted matches
  - `count` (integer): Number of matches
- **Example**: `extract_patterns("Contact us at info@example.com", "", "email")`

#### 7.4 format_text
- **Description**: Format text in various ways
- **Inputs**:
  - `text` (string): Input text
  - `format_type` (string): Format type (uppercase, lowercase, title, capitalize)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `formatted_text` (string): Formatted text
- **Example**: `format_text("hello world", "title")`

#### 7.5 generate_hash
- **Description**: Generate hash for text
- **Inputs**:
  - `text` (string): Input text
  - `hash_type` (string, optional): Hash algorithm (md5, sha1, sha256, sha512)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `hash` (string): Generated hash
- **Example**: `generate_hash("password123", "sha256")`

#### 7.6 split_text
- **Description**: Split text by delimiter or pattern
- **Inputs**:
  - `text` (string): Input text
  - `delimiter` (string, optional): Split delimiter
  - `max_splits` (integer, optional): Maximum number of splits
  - `split_type` (string, optional): Split type (delimiter, lines, words, sentences)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `parts` (list): Split text parts
  - `count` (integer): Number of parts
- **Example**: `split_text("apple,banana,orange", ",", -1, "delimiter")`

#### 7.7 join_text
- **Description**: Join text parts with delimiter
- **Inputs**:
  - `text_parts` (list): List of text parts to join
  - `delimiter` (string, optional): Join delimiter
- **Outputs**:
  - `success` (boolean): Operation success status
  - `result` (string): Joined text
- **Example**: `join_text(["apple", "banana", "orange"], ", ")`

### 8. DATETIME OPERATIONS FUNCTIONS (8 functions)

#### 8.1 get_current_time
- **Description**: Get current date and time
- **Inputs**:
  - `timezone_name` (string, optional): Timezone name
  - `format_string` (string, optional): Custom format string
- **Outputs**:
  - `success` (boolean): Operation success status
  - `datetime` (dict): Current datetime information
- **Example**: `get_current_time("UTC", "%Y-%m-%d %H:%M:%S")`

#### 8.2 parse_datetime
- **Description**: Parse datetime string into components
- **Inputs**:
  - `datetime_string` (string): Datetime string to parse
  - `format_string` (string, optional): Expected format
- **Outputs**:
  - `success` (boolean): Operation success status
  - `datetime` (dict): Parsed datetime components
- **Example**: `parse_datetime("2024-03-15 14:30:00", "%Y-%m-%d %H:%M:%S")`

#### 8.3 calculate_date_difference
- **Description**: Calculate difference between two dates
- **Inputs**:
  - `start_date` (string): Start date
  - `end_date` (string): End date
  - `unit` (string, optional): Unit for difference (days, hours, minutes, seconds)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `difference` (number): Date difference in specified unit
- **Example**: `calculate_date_difference("2024-01-01", "2024-12-31", "days")`

#### 8.4 add_time
- **Description**: Add time to a date
- **Inputs**:
  - `base_date` (string): Base date
  - `amount` (integer): Amount to add
  - `unit` (string): Time unit (days, hours, minutes, seconds, weeks)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `new_date` (string): New date after addition
- **Example**: `add_time("2024-03-15", 30, "days")`

#### 8.5 format_datetime
- **Description**: Format datetime in specified format
- **Inputs**:
  - `datetime_string` (string): Input datetime
  - `format_string` (string): Output format
- **Outputs**:
  - `success` (boolean): Operation success status
  - `formatted` (string): Formatted datetime
- **Example**: `format_datetime("2024-03-15T14:30:00", "%B %d, %Y at %I:%M %p")`

#### 8.6 get_calendar
- **Description**: Get calendar information for a month
- **Inputs**:
  - `year` (integer): Year
  - `month` (integer): Month (1-12)
- **Outputs**:
  - `success` (boolean): Operation success status
  - `calendar` (list): Calendar grid
  - `month_name` (string): Month name
  - `days_in_month` (integer): Number of days in month
- **Example**: `get_calendar(2024, 3)`

#### 8.7 is_weekend
- **Description**: Check if a date falls on weekend
- **Inputs**:
  - `date_string` (string): Date to check
- **Outputs**:
  - `success` (boolean): Operation success status
  - `is_weekend` (boolean): Whether date is weekend
  - `weekday` (string): Day of week name
- **Example**: `is_weekend("2024-03-16")`

#### 8.8 get_timezone_info
- **Description**: Get timezone information
- **Inputs**: None
- **Outputs**:
  - `success` (boolean): Operation success status
  - `local_time` (string): Local time
  - `utc_time` (string): UTC time
  - `offset_hours` (number): UTC offset in hours
- **Example**: `get_timezone_info()`

## Summary

**Total Functions: 55**
- Data Processing: 9 functions
- Communication: 7 functions
- File Operations: 10 functions
- Web Operations: 8 functions
- System Operations: 8 functions
- Math Operations: 5 functions
- Text Operations: 7 functions
- DateTime Operations: 8 functions

Each function is designed to be:
- **Self-contained**: Can be executed independently
- **Well-documented**: Clear inputs, outputs, and examples
- **Error-handled**: Returns success/failure status
- **Composable**: Outputs can be used as inputs to other functions
- **Consistent**: Follows the same interface pattern

This comprehensive function library enables the AI to handle a wide variety of tasks through intelligent function calling and sequencing.
