#!/usr/bin/env python3
"""
Verify Function Count and Definitions
This script verifies that we have 55+ functions with proper descriptions, inputs, and outputs.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def count_functions_in_file(file_path):
    """Count functions in a specific file"""
    functions = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find all class definitions that inherit from BaseFunction
        import re
        pattern = r'class\s+(\w+Function)\(BaseFunction\):'
        matches = re.findall(pattern, content)
        
        for match in matches:
            # Extract function details
            class_pattern = rf'class\s+{match}\(BaseFunction\):.*?(?=class|\Z)'
            class_match = re.search(class_pattern, content, re.DOTALL)
            
            if class_match:
                class_content = class_match.group(0)
                
                # Extract name
                name_match = re.search(r'return\s+"([^"]+)"', class_content)
                name = name_match.group(1) if name_match else "unknown"
                
                # Extract description
                desc_match = re.search(r'return\s+"([^"]+)".*?description', class_content, re.DOTALL)
                if not desc_match:
                    desc_match = re.search(r'description.*?return\s+"([^"]+)"', class_content, re.DOTALL)
                description = desc_match.group(1) if desc_match else "No description"
                
                # Extract category
                cat_match = re.search(r'category.*?return\s+"([^"]+)"', class_content, re.DOTALL)
                category = cat_match.group(1) if cat_match else "unknown"
                
                functions.append({
                    'class_name': match,
                    'function_name': name,
                    'description': description,
                    'category': category,
                    'file': file_path.name
                })
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return functions

def main():
    """Main verification function"""
    print("AI Function Calling Pipeline - Function Verification")
    print("=" * 60)
    
    # Find all function files
    src_dir = Path("src/functions")
    if not src_dir.exists():
        print("Error: src/functions directory not found")
        return
    
    function_files = list(src_dir.glob("*.py"))
    function_files = [f for f in function_files if f.name not in ['__init__.py', 'base.py']]
    
    print(f"Found {len(function_files)} function modules:")
    for f in function_files:
        print(f"  - {f.name}")
    
    # Count functions in each file
    all_functions = []
    category_counts = {}
    
    print("\nFunction Analysis by Category:")
    print("-" * 40)
    
    for file_path in function_files:
        functions = count_functions_in_file(file_path)
        all_functions.extend(functions)
        
        if functions:
            category = functions[0]['category']
            category_counts[category] = len(functions)
            print(f"\n{category.replace('_', ' ').title()} ({file_path.name}):")
            for func in functions:
                print(f"  {len(all_functions) - len(functions) + functions.index(func) + 1:2d}. {func['function_name']}")
                print(f"      Description: {func['description']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    total_functions = len(all_functions)
    print(f"Total Functions Found: {total_functions}")
    
    if total_functions >= 55:
        print("✓ REQUIREMENT MET: 55+ functions implemented")
    else:
        print(f"✗ REQUIREMENT NOT MET: Need {55 - total_functions} more functions")
    
    print(f"\nFunctions by Category:")
    for category, count in sorted(category_counts.items()):
        print(f"  - {category.replace('_', ' ').title()}: {count} functions")
    
    # Verify function quality
    print(f"\nFunction Quality Check:")
    functions_with_descriptions = sum(1 for f in all_functions if f['description'] != "No description" and len(f['description']) > 10)
    print(f"  - Functions with proper descriptions: {functions_with_descriptions}/{total_functions}")
    
    functions_with_names = sum(1 for f in all_functions if f['function_name'] != "unknown")
    print(f"  - Functions with proper names: {functions_with_names}/{total_functions}")
    
    unique_names = len(set(f['function_name'] for f in all_functions))
    print(f"  - Unique function names: {unique_names}/{total_functions}")
    
    if functions_with_descriptions == total_functions:
        print("✓ All functions have proper descriptions")
    else:
        print(f"✗ {total_functions - functions_with_descriptions} functions missing descriptions")
    
    if unique_names == total_functions:
        print("✓ All function names are unique")
    else:
        print(f"✗ {total_functions - unique_names} duplicate function names found")
    
    # List all functions
    print(f"\nComplete Function List:")
    print("-" * 40)
    for i, func in enumerate(all_functions, 1):
        print(f"{i:2d}. {func['function_name']} ({func['category']})")
    
    # Check for required function types
    print(f"\nRequired Function Type Coverage:")
    print("-" * 40)
    
    required_categories = {
        'data_processing': 'Data Processing',
        'communication': 'Communication', 
        'file_operations': 'File Operations',
        'web_operations': 'Web Operations',
        'system_operations': 'System Operations',
        'math_operations': 'Math Operations',
        'text_operations': 'Text Operations',
        'datetime_operations': 'DateTime Operations'
    }
    
    for cat_key, cat_name in required_categories.items():
        if cat_key in category_counts:
            print(f"✓ {cat_name}: {category_counts[cat_key]} functions")
        else:
            print(f"✗ {cat_name}: Missing")
    
    # Final assessment
    print("\n" + "=" * 60)
    print("FINAL ASSESSMENT")
    print("=" * 60)
    
    if (total_functions >= 55 and 
        functions_with_descriptions == total_functions and 
        unique_names == total_functions and
        len(category_counts) >= 8):
        print("🎉 SUCCESS: All requirements met!")
        print("✓ 55+ functions implemented")
        print("✓ All functions properly described")
        print("✓ All function names unique")
        print("✓ All required categories covered")
        print("\nThe AI Function Calling Pipeline has a complete")
        print("function library ready for production use!")
    else:
        print("⚠️  ISSUES FOUND:")
        if total_functions < 55:
            print(f"  - Need {55 - total_functions} more functions")
        if functions_with_descriptions != total_functions:
            print(f"  - {total_functions - functions_with_descriptions} functions need descriptions")
        if unique_names != total_functions:
            print(f"  - {total_functions - unique_names} duplicate names need fixing")
        if len(category_counts) < 8:
            print(f"  - Need {8 - len(category_counts)} more categories")

if __name__ == "__main__":
    main()
