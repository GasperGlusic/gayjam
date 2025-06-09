import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import ssl # Import ssl module to potentially diagnose issues
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs

# --- API Request Function ---
def make_api_request(base_url, api_key, key_param_name):
    """
    Attempts to make an API request to the given URL, optionally including an API key
    as a query parameter.
    Returns True and the JSON response (pretty-printed string) on success,
    or False and an error message on failure.
    """
    if not base_url:
        return False, "API URL cannot be empty."

    # Construct the final URL with the API key as a query parameter
    # This handles cases where the URL already has query parameters
    final_url = base_url
    if api_key and key_param_name:
        try:
            parsed_url = urlparse(base_url)
            query_params = parse_qs(parsed_url.query)
            query_params[key_param_name] = [api_key] # Add/overwrite the key param
            new_query = urlencode(query_params, doseq=True)
            final_url = urlunparse(parsed_url._replace(query=new_query))
        except Exception as e:
            # Catch errors during URL parsing/construction
            return False, f"Error constructing URL with API key: {e}. Please check Base URL and Key Parameter Name."

    try:
        # WARNING: Setting 'verify=False' disables SSL certificate verification.
        # This is INSECURE and should ONLY be used for debugging to check if SSL is the problem.
        # NEVER use this in a production environment or with sensitive data.
        response = requests.get(final_url, timeout=10, verify=False) # Increased timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Attempt to parse JSON. If it's not JSON, JSONDecodeError will be caught.
        response_data = response.json()
        return True, json.dumps(response_data, indent=2) # Pretty print JSON

    except requests.exceptions.RequestException as e:
        # This single catch-all for RequestException covers:
        # - ConnectionError (no internet, DNS issues, SSL issues)
        # - Timeout (API too slow to respond)
        # - HTTPError (like 401, 403, 500 status codes from raise_for_status())
        return False, f"Network or HTTP error: {e}\nAttempted URL: {final_url}\n\n**Troubleshooting:**\n- Ensure the URL is correct and accessible.\n- Check your internet connection.\n- Verify the API key is correct for the API's endpoint and method (e.g., query parameter name).\n- The API might require authentication via headers (not supported by this simple tool)."
    except json.JSONDecodeError:
        # If the response isn't valid JSON, this catches it.
        # This happens if the API returns plain text, HTML (e.g., an error page), or empty response.
        return False, f"API returned unreadable data (not valid JSON format).\nAttempted URL: {final_url}\n\n**Response Content Snippet:**\n{response.text[:500]}...\n\n**Troubleshooting:**\n- This API might not return JSON, or it returned an error page. Try opening the URL in a browser."
    except Exception as e:
        # A final catch-all for any other unforeseen internal issues.
        return False, f"An unexpected internal error occurred: {e}"

# --- GUI Logic ---

def perform_api_request():
    """
    Retrieves API URL, key, and key parameter name from inputs,
    performs the API request, and updates the status display.
    """
    api_url = api_url_entry.get().strip()
    api_key = api_key_entry.get().strip()
    key_param_name = key_param_name_entry.get().strip()

    # Clear previous output and show a loading message
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, "Making API request... Please wait.\n")
    output_area.config(state=tk.DISABLED)

    # Disable buttons during request
    request_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)

    # Perform the API request
    is_success, result_content = make_api_request(api_url, api_key, key_param_name)

    # Update the output area with the result
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END) # Clear loading message
    if is_success:
        output_area.insert(tk.END, "API Response (JSON):\n\n")
        output_area.insert(tk.END, result_content)
    else:
        output_area.insert(tk.END, "API Request Failed:\n\n")
        output_area.insert(tk.END, result_content)
        # Show a pop-up message box for critical errors
        messagebox.showerror("API Request Error", "Failed to retrieve API response. See output area for details.")

    output_area.config(state=tk.DISABLED) # Make output read-only again
    request_button.config(state=tk.NORMAL) # Re-enable buttons
    clear_button.config(state=tk.NORMAL)

def clear_fields():
    """Clears all input and output fields."""
    api_url_entry.delete(0, tk.END)
    api_key_entry.delete(0, tk.END)
    key_param_name_entry.delete(0, tk.END)
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.config(state=tk.DISABLED)


# --- Main Application Window Setup ---
root = tk.Tk()
root.title("Generic API Tester")
root.geometry("800x600")

# Configure grid weights to make elements resize with window
# This ensures that the output area expands as the window is resized
root.grid_rowconfigure(8, weight=1) # Output area should expand vertically
root.grid_columnconfigure(0, weight=1) # Make column expand horizontally

# --- API URL Input ---
api_url_label = tk.Label(root, text="API Endpoint URL (e.g., https://api.chucknorris.io/jokes/random):", font=("Arial", 10, "bold"))
api_url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
api_url_entry = tk.Entry(root, width=80, font=("Arial", 10), bd=2, relief="groove")
api_url_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

# --- API Key Input ---
api_key_label = tk.Label(root, text="API Key (optional, leave blank if not needed):", font=("Arial", 10, "bold"))
api_key_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
api_key_entry = tk.Entry(root, width=80, font=("Arial", 10), bd=2, relief="groove")
api_key_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# --- Key Parameter Name Input (for keys in URL query string) ---
key_param_name_label = tk.Label(root, text="Key Parameter Name (e.g., appid, key, token - if key is in URL query):", font=("Arial", 10, "bold"))
key_param_name_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
key_param_name_entry = tk.Entry(root, width=80, font=("Arial", 10), bd=2, relief="groove")
key_param_name_entry.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
key_param_name_entry.insert(0, "appid") # Default to a common parameter name

# --- Buttons Frame ---
button_frame = tk.Frame(root)
button_frame.grid(row=6, column=0, padx=10, pady=10)

request_button = tk.Button(button_frame, text="Make API Request", command=perform_api_request, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049")
request_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_fields, font=("Arial", 12, "bold"), bg="#f44336", fg="white", activebackground="#da190b")
clear_button.pack(side=tk.LEFT, padx=5)

# --- Output Area ---
output_label = tk.Label(root, text="API Response / Error Details:", font=("Arial", 12, "bold"))
output_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Arial", 10), bd=2, relief="groove")
output_area.grid(row=8, column=0, padx=10, pady=5, sticky="nsew")
output_area.config(state=tk.DISABLED) # Make output area read-only initially

# Start the Tkinter event loop
root.mainloop()
