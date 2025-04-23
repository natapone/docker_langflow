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

    inputs = [
        StrInput(
            name="sheet_identifier",
            display_name="Sheet Name or ID",
            info="Name or ID of the Google Sheet document. You can use either the full name of the sheet (e.g., 'My Spreadsheet') or the sheet ID from the URL (e.g., '1111111111111111111111111111111111111111')",
            required=True,
            tool_mode=True,
        ),
        StrInput(
            name="worksheet_name",
            display_name="Worksheet Name",
            info="Name of the worksheet/tab within the spreadsheet (e.g., 'Sheet1', 'Data', 'Responses'). Default is 'Sheet1' if left blank.",
            value="Sheet1",
            tool_mode=True,
        ),
        SecretStrInput(
            name="service_account_json",
            display_name="Service Account JSON",
            info="Paste your Google service_account.json content here. This JSON contains authentication credentials for your Google Cloud service account. Make sure the spreadsheet is shared with the service account email.",
            required=True,
            # multiline=True,
        ),
        StrInput(
            name="cell_range",
            display_name="Cell Range",
            info="Specify a single cell or range to read/update. Examples: 'A1' (single cell), 'B2:C5' (range), 'A:A' (entire column), '1:1' (entire row), 'A2:A' (column A from row 2 down)",
            value="A1",
            tool_mode=True,
        ),
        StrInput(
            name="operation",
            display_name="Operation",
            info="Operation to perform: 'read' (get values), 'update' (modify values), 'append' (add rows). For 'update' with ranges, provide a 2D array as JSON. For 'append', provide a JSON array of row data to append.",
            value="read",
            tool_mode=True,
        ),
        MultilineInput(
            name="data",
            display_name="Data to Write",
            info="Data to write for update/append operations. For single cell: simple text or value. For range updates: JSON format like [[\"A1\",\"B1\"],[\"A2\",\"B2\"]]. For append: JSON array like [[\"row1col1\",\"row1col2\"],[\"row2col1\",\"row2col2\"]]",
            # multiline=True,
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Sheet Data", name="sheet_data", method="process_sheet"),
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

    def process_sheet(self) -> Dict[str, Any]:
        """
        Process the Google Sheet based on the operation (read, update, append)
        
        Returns:
            Dict[str, Any]: The result of the operation
        """
        try:
            # Setup gspread client - this will also check for required packages
            client = self._setup_gspread_client()
            if not client:
                return {
                    "status": "error", 
                    "error": "Failed to set up Google Sheets client: " + (self.status or "Unknown error")
                }
            
            # Determine if sheet_identifier is likely an ID or name
            sheet_identifier = self.sheet_identifier
            
            # Open the sheet and worksheet
            try:
                # Check if the identifier is likely a sheet ID (alphanumeric with dashes)
                if re.match(r'^[a-zA-Z0-9_-]+$', sheet_identifier) and len(sheet_identifier) > 30:
                    sheet = client.open_by_key(sheet_identifier)
                else:
                    sheet = client.open(sheet_identifier)
                    
                worksheet = sheet.worksheet(self.worksheet_name)
            except Exception as e:
                import gspread
                
                if isinstance(e, gspread.exceptions.SpreadsheetNotFound):
                    error_msg = f"Spreadsheet '{sheet_identifier}' not found. Make sure it's shared with the service account."
                elif isinstance(e, gspread.exceptions.WorksheetNotFound):
                    error_msg = f"Worksheet '{self.worksheet_name}' not found."
                else:
                    error_msg = f"Error opening sheet: {str(e)}"
                
                return {"status": "error", "error": error_msg}
            
            # Process based on operation
            operation = self.operation.lower()
            
            # READ operation
            if operation == "read":
                try:
                    # Check if it's a single cell or a range
                    if ":" in self.cell_range:
                        result = worksheet.get(self.cell_range)
                    else:
                        result = worksheet.acell(self.cell_range).value
                    
                    self.status = f"Successfully read from {self.cell_range}"
                    return {"status": "success", "data": result}
                except Exception as e:
                    return {"status": "error", "error": f"Failed to read data: {str(e)}"}
            
            # UPDATE operation
            elif operation == "update":
                try:
                    if not self.data:
                        return {"status": "error", "error": "No data provided for update operation"}
                    
                    # Process for single cell or range update
                    if ":" not in self.cell_range:
                        # Single cell update - using the worksheet.update_cell method
                        # First extract row and column from the cell reference
                        cell_ref = self.cell_range.upper()
                        # Extract column letters and row number
                        col_letters = ''.join(filter(str.isalpha, cell_ref))
                        row_num = int(''.join(filter(str.isdigit, cell_ref)))
                        
                        # Convert column letters to column number
                        col_num = 0
                        for char in col_letters:
                            col_num = col_num * 26 + (ord(char) - ord('A') + 1)
                        
                        # Now use update_cell which takes row, col, value
                        worksheet.update_cell(row_num, col_num, self.data)
                        self.status = f"Successfully updated {self.cell_range}"
                    else:
                        # Range update - parse data as JSON
                        try:
                            data = json.loads(self.data)
                            worksheet.update(self.cell_range, data)
                            self.status = f"Successfully updated range {self.cell_range}"
                        except json.JSONDecodeError:
                            return {"status": "error", "error": "For range updates, data must be valid JSON format"}
                    
                    return {"status": "success", "message": self.status}
                except Exception as e:
                    return {"status": "error", "error": f"Failed to update data: {str(e)}"}
            
            # APPEND operation
            elif operation == "append":
                try:
                    if not self.data:
                        return {"status": "error", "error": "No data provided for append operation"}
                    
                    # Parse data as array for append
                    try:
                        data = json.loads(self.data)
                        if not isinstance(data, list):
                            data = [data]  # Convert single object to list
                        
                        # Append row(s)
                        worksheet.append_rows(data)
                        self.status = f"Successfully appended {len(data)} row(s)"
                        return {"status": "success", "message": self.status}
                    except json.JSONDecodeError:
                        return {"status": "error", "error": "For append operations, data must be valid JSON array format"}
                except Exception as e:
                    return {"status": "error", "error": f"Failed to append data: {str(e)}"}
            
            else:
                return {"status": "error", "error": f"Unknown operation: {operation}. Use 'read', 'update', or 'append'"}
                
        except Exception as e:
            self.status = f"Unexpected error: {str(e)}"
            return {"status": "error", "error": self.status} 