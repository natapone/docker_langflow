from langflow.custom import Component
from langflow.io import Output, StrInput, SecretStrInput, MultilineInput
from typing import Dict, Any, List, Optional
import json
import os
import tempfile
import logging
import re
import sys

# Set up logging
logger = logging.getLogger('google_sheets_component')

class GoogleSheetComponent(Component):
    display_name = "Google Sheet Service"
    description = "Access and update Google Sheets using Service Account authentication"
    documentation = "Custom component for Google Sheets integration via service account"
    icon = "table"
    name = "GoogleSheetComponent"

    # Common inputs for all operations
    inputs = [
        StrInput(
            name="sheet_identifier",
            display_name="Sheet Name or ID",
            info="Name or ID of the Google Sheet document. You can use either the full name of the sheet (e.g., 'My Spreadsheet') or the sheet ID from the URL (e.g., '1111111111111111111111111111111111111111')",
            required=True,
            tool_mode=False,
        ),
        StrInput(
            name="worksheet_name",
            display_name="Worksheet Name",
            info="Name of the worksheet/tab within the spreadsheet (e.g., 'Sheet1', 'Data', 'Responses'). Default is 'Sheet1' if left blank.",
            value="Sheet1",
            tool_mode=False,
            required=True,
        ),
        SecretStrInput(
            name="service_account_json",
            display_name="Service Account JSON",
            info="Paste your Google service_account.json content here. This JSON contains authentication credentials for your Google Cloud service account. Make sure the spreadsheet is shared with the service account email.",
            required=True,
        ),
        StrInput(
            name="operation",
            display_name="Operation",
            info="Operation to perform: 'read' (get values), 'update' (modify values), 'append' (add rows). This is used for manual testing and will be checked against the called function.",
            value="read",
            tool_mode=True,
            required=False,
        ),
        # Cell range input (used by read and update)
        StrInput(
            name="cell_range",
            display_name="Cell Range",
            info="Specify a single cell or range to read/update. Examples: 'A1' (single cell), 'B2:C5' (range), 'A:A' (entire column), '1:1' (entire row), 'A2:A' (column A from row 2 down)",
            value="A1",
            tool_mode=True,
        ),
        # Data input (used by update and append)
        MultilineInput(
            name="data",
            display_name="Data to Write",
            info="Data to write for update/append operations. For single cell: simple text or value. For range updates: JSON format like [[\"A1\",\"B1\"],[\"A2\",\"B2\"]]. For append: JSON array like [[\"row1col1\",\"row1col2\"],[\"row2col1\",\"row2col2\"]]",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Read Sheet Data", name="read_data", method="read_sheet_data"),
        Output(display_name="Update Sheet Data", name="update_data", method="update_sheet_data"),
        Output(display_name="Append Sheet Data", name="append_data", method="append_sheet_data"),
    ]

    def _ensure_packages_available(self) -> bool:
        """
        Make sure required packages are available by adding the site-packages path
        
        Returns:
            bool: True if packages are available, False if not found
        """
        try:
            # Try importing required packages
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            return True
        except ImportError:
            # Add the fixed Python 3.12 site-packages path
            user_site_packages = '/app/data/.local/lib/python3.12/site-packages'
            if user_site_packages not in sys.path:
                sys.path.append(user_site_packages)
            
            # Try importing again
            try:
                import gspread
                from oauth2client.service_account import ServiceAccountCredentials
                return True
            except ImportError:
                self.status = "Required packages not found. Make sure gspread and oauth2client are installed."
                return False

    def _setup_gspread_client(self) -> Any:
        """Set up and return an authenticated gspread client"""
        # First ensure required packages are available
        if not self._ensure_packages_available():
            return None
            
        try:
            # Import here after ensuring packages are available
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            # Create a temporary file for service account JSON
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                temp_file.write(self.service_account_json)
                temp_file_path = temp_file.name
            
            # Define scope
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            
            # Authenticate
            creds = ServiceAccountCredentials.from_json_keyfile_name(temp_file_path, scope)
            client = gspread.authorize(creds)
            
            # Get service account email for debugging
            try:
                sa_info = json.loads(self.service_account_json)
                logger.info(f"Authenticated with service account: {sa_info.get('client_email', 'unknown')}")
            except:
                logger.info("Authenticated with service account (email unknown)")
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            return client
        except Exception as e:
            self.status = f"Authentication error: {str(e)}"
            return None
    
    def _get_worksheet(self, client):
        """
        Helper method to get the worksheet based on sheet_identifier and worksheet_name
        
        Args:
            client: Authenticated gspread client
            
        Returns:
            worksheet object or None if error
        """
        try:
            # Determine if sheet_identifier is likely an ID or name
            sheet_identifier = self.sheet_identifier
            
            # Check if the identifier is likely a sheet ID (alphanumeric with dashes)
            if re.match(r'^[a-zA-Z0-9_-]+$', sheet_identifier) and len(sheet_identifier) > 30:
                sheet = client.open_by_key(sheet_identifier)
            else:
                sheet = client.open(sheet_identifier)
                
            worksheet = sheet.worksheet(self.worksheet_name)
            return worksheet
        except Exception as e:
            import gspread
            
            if isinstance(e, gspread.exceptions.SpreadsheetNotFound):
                self.status = f"Spreadsheet '{sheet_identifier}' not found. Make sure it's shared with the service account."
            elif isinstance(e, gspread.exceptions.WorksheetNotFound):
                self.status = f"Worksheet '{self.worksheet_name}' not found."
            else:
                self.status = f"Error opening sheet: {str(e)}"
            
            return None

    def _check_operation(self, expected_operation: str) -> bool:
        """
        Check if the operation input matches the expected operation.
        If operation is not set or empty, proceed anyway (for AI tool usage).
        
        Args:
            expected_operation (str): The operation that should be performed
            
        Returns:
            bool: True if operation matches or is not specified, False otherwise
        """
        # If operation is not set or is empty, assume it's valid (AI tool usage)
        if not hasattr(self, 'operation') or not self.operation:
            return True
            
        # Otherwise check for match
        return self.operation.lower() == expected_operation.lower()

    def read_sheet_data(self) -> Dict[str, Any]:
        """
        Read data from a Google Sheet using the specified cell range.
        
        This function reads data from the spreadsheet and worksheet specified in the component inputs.
        It can read a single cell value or a range of cells.
        
        Returns:
            Dict[str, Any]: A dictionary with status and data. For a single cell, the data is a single value.
                          For a range, the data is a list of lists.
                          
        Example usage by an AI agent:
        ```python
        # To read cell A1
        component.cell_range = "A1"
        result = component.read_sheet_data()
        
        # To read a range of cells
        component.cell_range = "A1:B10"
        result = component.read_sheet_data()
        
        # To read an entire column
        component.cell_range = "C:C"
        result = component.read_sheet_data()
        ```
        """
        # Check operation if set
        if not self._check_operation("read"):
            return {"status": "error", "error": f"Operation mismatch: expected 'read', got '{self.operation}'"}
            
        try:
            # Setup gspread client
            client = self._setup_gspread_client()
            if not client:
                return {
                    "status": "error", 
                    "error": "Failed to set up Google Sheets client: " + (self.status or "Unknown error")
                }
            
            # Get worksheet
            worksheet = self._get_worksheet(client)
            if not worksheet:
                return {"status": "error", "error": self.status}
            
            # Read data using the cell_range input
            try:
                cell_range = self.cell_range
                # Check if it's a single cell or a range
                if ":" in cell_range:
                    result = worksheet.get(cell_range)
                else:
                    result = worksheet.acell(cell_range).value
                
                self.status = f"Successfully read from {cell_range}"
                return {"status": "success", "data": result}
            except Exception as e:
                return {"status": "error", "error": f"Failed to read data: {str(e)}"}
                
        except Exception as e:
            self.status = f"Unexpected error reading sheet: {str(e)}"
            return {"status": "error", "error": self.status}

    def update_sheet_data(self) -> Dict[str, Any]:
        """
        Update data in a Google Sheet using the specified cell range and data.
        
        This function updates data in the spreadsheet and worksheet specified in the component inputs.
        It can update a single cell or a range of cells based on the cell_range input.
        
        Returns:
            Dict[str, Any]: A dictionary with status and message.
            
        Example usage by an AI agent:
        ```python
        # To update a single cell
        component.cell_range = "A1"
        component.data = "New Value"
        result = component.update_sheet_data()
        
        # To update a range of cells
        component.cell_range = "A1:B3"
        component.data = '''[["Name", "Age"], ["Alice", 25], ["Bob", 30]]'''
        result = component.update_sheet_data()
        ```
        """
        # Check operation if set
        if not self._check_operation("update"):
            return {"status": "error", "error": f"Operation mismatch: expected 'update', got '{self.operation}'"}
            
        try:
            # Setup gspread client
            client = self._setup_gspread_client()
            if not client:
                return {
                    "status": "error", 
                    "error": "Failed to set up Google Sheets client: " + (self.status or "Unknown error")
                }
            
            # Get worksheet
            worksheet = self._get_worksheet(client)
            if not worksheet:
                return {"status": "error", "error": self.status}
            
            # Update data using the cell_range and data inputs
            try:
                cell_range = self.cell_range
                data = self.data
                
                if not data:
                    return {"status": "error", "error": "No data provided for update operation"}
                
                # Process for single cell or range update
                if ":" not in cell_range:
                    # Single cell update - using the worksheet.update_cell method
                    # First extract row and column from the cell reference
                    cell_ref = cell_range.upper()
                    # Extract column letters and row number
                    col_letters = ''.join(filter(str.isalpha, cell_ref))
                    row_num = int(''.join(filter(str.isdigit, cell_ref)))
                    
                    # Convert column letters to column number
                    col_num = 0
                    for char in col_letters:
                        col_num = col_num * 26 + (ord(char) - ord('A') + 1)
                    
                    # Now use update_cell which takes row, col, value
                    worksheet.update_cell(row_num, col_num, data)
                    self.status = f"Successfully updated {cell_range}"
                else:
                    # Range update - parse data as JSON
                    try:
                        json_data = json.loads(data)
                        worksheet.update(cell_range, json_data)
                        self.status = f"Successfully updated range {cell_range}"
                    except json.JSONDecodeError:
                        return {"status": "error", "error": "For range updates, data must be valid JSON format"}
                
                return {"status": "success", "message": self.status}
            except Exception as e:
                return {"status": "error", "error": f"Failed to update data: {str(e)}"}
                
        except Exception as e:
            self.status = f"Unexpected error updating sheet: {str(e)}"
            return {"status": "error", "error": self.status}

    def append_sheet_data(self) -> Dict[str, Any]:
        """
        Append rows to a Google Sheet using the provided data.
        
        This function appends data as new rows to the spreadsheet and worksheet specified 
        in the component inputs. The data should be in JSON format representing rows to append.
        The rows will always be appended starting from column A regardless of data format.
        
        Returns:
            Dict[str, Any]: A dictionary with status and message.
            
        Example usage by an AI agent:
        ```python
        # To append a single row
        component.data = '''[["John Doe", "john@example.com", 28]]'''
        result = component.append_sheet_data()
        
        # To append multiple rows
        component.data = '''[
            ["John Doe", "john@example.com", 28],
            ["Jane Smith", "jane@example.com", 32]
        ]'''
        result = component.append_sheet_data()
        ```
        """
        # Check operation if set
        if not self._check_operation("append"):
            return {"status": "error", "error": f"Operation mismatch: expected 'append', got '{self.operation}'"}
            
        try:
            # Setup gspread client
            client = self._setup_gspread_client()
            if not client:
                return {
                    "status": "error", 
                    "error": "Failed to set up Google Sheets client: " + (self.status or "Unknown error")
                }
            
            # Get worksheet
            worksheet = self._get_worksheet(client)
            if not worksheet:
                return {"status": "error", "error": self.status}
            
            # Append data using the data input
            try:
                data = self.data
                
                if not data:
                    return {"status": "error", "error": "No data provided for append operation"}
                
                # Parse data as array for append
                try:
                    json_data = json.loads(data)
                    
                    # Handle various data formats
                    if not isinstance(json_data, list):
                        # Convert single object to list
                        json_data = [json_data]
                    
                    # Ensure each row is a list (not a dict or other object)
                    for i, row in enumerate(json_data):
                        if not isinstance(row, list):
                            # If row is a dict or other non-list, convert to a list of values
                            if isinstance(row, dict):
                                json_data[i] = list(row.values())
                            else:
                                # For any other type, wrap it in a list
                                json_data[i] = [row]
                    
                    # Use specific range for appending starting from column A
                    # get the next available row in the sheet
                    next_row = len(worksheet.get_all_values()) + 1
                    range_to_update = f"A{next_row}"
                    
                    # Use update instead of append_rows to ensure we start from column A
                    worksheet.update(range_to_update, json_data)
                    
                    self.status = f"Successfully appended {len(json_data)} row(s) starting from column A"
                    return {"status": "success", "message": self.status}
                except json.JSONDecodeError:
                    return {"status": "error", "error": "For append operations, data must be valid JSON array format"}
            except Exception as e:
                return {"status": "error", "error": f"Failed to append data: {str(e)}"}
                
        except Exception as e:
            self.status = f"Unexpected error appending to sheet: {str(e)}"
            return {"status": "error", "error": self.status} 