# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Union

# Define the Pydantic model for the request body to ensure proper data format
class RequestModel(BaseModel):
    # The 'data' field is an array that can contain strings
    data: List[str]

# Define the Pydantic model for the response body
class ResponseModel(BaseModel):
    is_success: bool = True
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

# Create an instance of the FastAPI application
app = FastAPI()

# Placeholder data for user information. You can customize these values.
USER_ID = "TRUSHA_ANAND"
EMAIL = "trushaanand003@gmail.com.com"
ROLL_NUMBER = "22BCE10550"

@app.post("/bfhl", response_model=ResponseModel)
async def process_data(request: RequestModel):
    """
    This endpoint takes an array of strings and processes it according to the
    specified rules, returning a structured JSON response.

    Args:
        request (RequestModel): A JSON body containing a 'data' key with an
                                array of strings.

    Returns:
        ResponseModel: A JSON response with processed data.
    """
    # Initialize lists and variables for the processed data
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    total_sum = 0
    all_alphabet_chars = []

    # Iterate through each item in the input data array
    for item in request.data:
        # Check if the item is a string. If not, raise an error.
        if not isinstance(item, str):
            raise HTTPException(status_code=400, detail="Input data must be an array of strings.")

        # Check if the item is a number (integer)
        try:
            num = int(item)
            # Add to total sum
            total_sum += num
            # Check if the number is even or odd and add to the respective list (as a string)
            if num % 2 == 0:
                even_numbers.append(item)
            else:
                odd_numbers.append(item)
        except ValueError:
            # If it's not a number, check if it's an alphabet
            if item.isalpha():
                # Store the original item in uppercase for the 'alphabets' list
                alphabets.append(item.upper())
                # Flatten the string into individual characters and add to the list for concatenation
                for char in item:
                    all_alphabet_chars.append(char)
            else:
                # If it's not a number or an alphabet, it's a special character
                special_characters.append(item)

    # Logic for the concatenated string with alternating caps
    # 1. Reverse the list of all individual alphabet characters
    reversed_chars = all_alphabet_chars[::-1]
    
    # 2. Iterate and apply alternating caps, starting with a capital letter
    concat_string_list = []
    for i, char in enumerate(reversed_chars):
        if i % 2 == 0:
            concat_string_list.append(char.upper())
        else:
            concat_string_list.append(char.lower())
    
    final_concat_string = "".join(concat_string_list)
    
    # Construct the final response dictionary
    response = {
        "is_success": True,
        "user_id": USER_ID,
        "email": EMAIL,
        "roll_number": ROLL_NUMBER,
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(total_sum),
        "concat_string": final_concat_string
    }

    # Return the structured response
    return response
