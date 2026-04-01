Inventory API README
Generated: 2026-04-01 16:40:32

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
