from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

# Personal details - UPDATE THESE WITH YOUR INFORMATION
USER_DETAILS = {
    "full_name": "TRUSHA",  # Change to your name in lowercase with underscores
    "birth_date": "220504",  # Change to your birth date (ddmmyyyy)
    "email": "trushaanand003@gmail.com",  # Change to your email
    "roll_number": "22BCE10550"  # Change to your roll number
}

def process_data(data_array):
    """
    Process the input array and categorize elements
    """
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    all_alphabets = ""
    
    for item in data_array:
        item_str = str(item)
        
        # Check if it's a pure number
        if item_str.isdigit():
            num = int(item_str)
            if num % 2 == 0:
                even_numbers.append(item_str)
            else:
                odd_numbers.append(item_str)
        
        # Check if it's purely alphabetic
        elif item_str.isalpha():
            alphabets.append(item_str.upper())
            all_alphabets += item_str.lower()
        
        # Check if it contains mixed alphanumeric (like "ABcD")
        elif any(c.isalpha() for c in item_str) and any(c.isdigit() for c in item_str):
            # Handle mixed alphanumeric strings
            for char in item_str:
                if char.isalpha():
                    all_alphabets += char.lower()
                elif char.isdigit():
                    num = int(char)
                    if num % 2 == 0:
                        even_numbers.append(char)
                    else:
                        odd_numbers.append(char)
            
            # Add the entire string to alphabets if it contains letters
            if any(c.isalpha() for c in item_str):
                alphabets.append(item_str.upper())
        
        # Otherwise, it's a special character
        else:
            special_characters.append(item_str)
    
    return odd_numbers, even_numbers, alphabets, special_characters, all_alphabets

def calculate_sum(odd_numbers, even_numbers):
    """
    Calculate sum of all numbers
    """
    total = 0
    for num in odd_numbers + even_numbers:
        try:
            total += int(num)
        except ValueError:
            continue
    return str(total)

def create_concat_string(all_alphabets):
    """
    Create concatenated string in reverse order with alternating caps
    """
    if not all_alphabets:
        return ""
    
    # Reverse the string
    reversed_alphabets = all_alphabets[::-1]
    
    # Apply alternating caps (first char lowercase, second uppercase, etc.)
    result = ""
    for i, char in enumerate(reversed_alphabets):
        if i % 2 == 0:
            result += char.lower()
        else:
            result += char.upper()
    
    return result

@app.route('/bfhl', methods=['POST'])
def process_bfhl():
    """
    Main POST endpoint to process BFHL request
    """
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                "is_success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        request_data = request.get_json()
        
        if not request_data or 'data' not in request_data:
            return jsonify({
                "is_success": False,
                "error": "Missing 'data' field in request body"
            }), 400
        
        data_array = request_data['data']
        
        if not isinstance(data_array, list):
            return jsonify({
                "is_success": False,
                "error": "'data' must be an array"
            }), 400
        
        # Process the data
        odd_numbers, even_numbers, alphabets, special_characters, all_alphabets = process_data(data_array)
        
        # Calculate sum
        total_sum = calculate_sum(odd_numbers, even_numbers)
        
        # Create concatenated string
        concat_string = create_concat_string(all_alphabets)
        
        # Create user_id
        user_id = f"{USER_DETAILS['full_name']}_{USER_DETAILS['birth_date']}"
        
        # Create response
        response = {
            "is_success": True,
            "user_id": user_id,
            "email": USER_DETAILS['email'],
            "roll_number": USER_DETAILS['roll_number'],
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": total_sum,
            "concat_string": concat_string
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/bfhl', methods=['GET'])
def get_bfhl():
    """
    GET endpoint for operation code
    """
    return jsonify({
        "operation_code": 1
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint for API status
    """
    return jsonify({
        "message": "BFHL API is running successfully",
        "endpoints": {
            "POST /bfhl": "Process data array",
            "GET /bfhl": "Get operation code"
        },
        "status": "Active"
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "service": "BFHL API"
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "is_success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "is_success": False,
        "error": "Method not allowed for this endpoint"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "is_success": False,
        "error": "Internal server error"
    }), 500

# CORS headers for web requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Test function to validate API locally
def run_tests():
    """
    Test function to validate API functionality
    """
    print("Running API tests...")
    
    # Test data from examples
    test_cases = [
        {
            "name": "Example A",
            "data": ["a", "1", "334", "4", "R", "$"],
            "expected_odd": ["1"],
            "expected_even": ["334", "4"],
            "expected_alphabets": ["A", "R"],
            "expected_special": ["$"],
            "expected_sum": "339"
        },
        {
            "name": "Example B", 
            "data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"],
            "expected_odd": ["5"],
            "expected_even": ["2", "4", "92"],
            "expected_alphabets": ["A", "Y", "B"],
            "expected_special": ["&", "-", "*"],
            "expected_sum": "103"
        },
        {
            "name": "Example C",
            "data": ["A", "ABcD", "DOE"],
            "expected_odd": [],
            "expected_even": [],
            "expected_alphabets": ["A", "ABCD", "DOE"],
            "expected_special": [],
            "expected_sum": "0"
        }
    ]
    
    for test in test_cases:
        print(f"\nTesting {test['name']}:")
        odd, even, alpha, special, all_alpha = process_data(test['data'])
        total_sum = calculate_sum(odd, even)
        concat_str = create_concat_string(all_alpha)
        
        print(f"Input: {test['data']}")
        print(f"Odd numbers: {odd}")
        print(f"Even numbers: {even}")
        print(f"Alphabets: {alpha}")
        print(f"Special chars: {special}")
        print(f"Sum: {total_sum}")
        print(f"Concat string: {concat_str}")

if __name__ == '__main__':
    # Uncomment the line below to run tests
    # run_tests()
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
