from datetime import datetime

content = f"""Inventory API README
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

API Endpoints

1. /getAll
   Method: GET
   Parameters: none

2. /getSingleProduct
   Method: GET
   Parameters: product_id (integer)

3. /addNew
   Method: POST
   Parameters:
      ProductID (integer)
      Name (string)
      UnitPrice (decimal)
      StockQuantity (integer)
      Description (string)

4. /deleteOne
   Method: DELETE
   Parameters: product_id (integer)

5. /startsWith
   Method: GET
   Parameters: letter (single character)

6. /paginate
   Method: GET
   Parameters:
      start_id (integer)
      end_id (integer)

7. /convert
   Method: GET
   Parameters: product_id (integer)

FastAPI Docs
http://localhost:8000/docs
"""

with open("README.txt", "w", encoding="utf-8") as file:
    file.write(content)

print("README.txt created successfully.")