import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import ssl # Import ssl module to potentially diagnose issues

# --- API Key Validation Function ---
def validate_api_key(api_key):
    """
    Attempts to validate the given API key by making a small request
    to the OpenWeatherMap API (or another API that requires a key).
    Returns True if the key is valid, False otherwise.
    """
    if not api_key:
        return False, "API Key cannot be empty."

    # Using OpenWeatherMap's current weather API for validation
    # We use a simple, non-existent city to get a clear API error for invalid key,
    # or a "city not found" message for a valid key.
    test_url = f"https://api.openweathermap.org/data/2.5/weather?q=NonExistentCity123&appid={api_key}"

    try:
        # WARNING: Setting 'verify=False' disables SSL certificate verification.
        # This is INSECURE and should ONLY be used for debugging to check if SSL is the problem.
        # NEVER use this in a production environment or with sensitive data.
        response = requests.get(test_url, timeout=5, verify=False)
        response.raise_for_status() # This will raise an HTTPError for 4xx/5xx responses

        # Attempt to parse JSON. If it fails, json.JSONDecodeError will be caught below.
        response_data = response.json()

        # OpenWeatherMap's primary way to signal an invalid key is a 401 status code,
        # which `raise_for_status()` would have caught. If we reach here,
        # the status code was acceptable (e.g., 200 or 404).
        # Now, check the JSON content for specific OpenWeatherMap messages.

        message = response_data.get("message", "").lower()

        if "invalid api key" in message:
            return False, "Invalid API Key: OpenWeatherMap service explicitly says key is invalid."
        elif "city not found" in message and response.status_code == 404:
            # This is the expected success case for a valid key with a non-existent city.
            return True, "API Key is valid. (Test city not found as expected)."
        elif response.status_code == 200:
            # In rare cases, if the dummy city was somehow found or an unexpected 200,
            # we consider the key valid.
            return True, "API Key is valid. (Unexpected 200 OK for test city, but key seems active)."
        else:
            # Catch other unexpected responses that don't directly indicate success/failure
            return False, f"API Key validation failed with unexpected response: {message if message else 'Unknown error'}"

    except requests.exceptions.RequestException as e:
        # This single catch-all for RequestException covers:
        # - ConnectionError (no internet, DNS issues)
        # - Timeout (API too slow to respond)
        # - HTTPError (like 401, 403, 500 status codes from raise_for_status())
        return False, f"Network or API communication error: {e}. Check internet, API key, or try again later."
    except json.JSONDecodeError:
        # If the response isn't valid JSON, this catches it.
        return False, "API returned unreadable data (not valid JSON format)."
    except Exception as e:
        # A final catch-all for any other unforeseen issues.
        return False, f"An unexpected internal error occurred: {e}"

# --- GUI Logic ---

def perform_validation():
    """
    Retrieves the API key from the input, performs validation,
    and updates the status display.
    """
    entered_api_key = api_key_entry.get().strip()

    status_area.config(state=tk.NORMAL)
    status_area.delete("1.0", tk.END)
    status_area.insert(tk.END, "Validating API Key...\n")
    status_area.config(state=tk.DISABLED)

    validate_button.config(state=tk.DISABLED)

    is_valid, message = validate_api_key(entered_api_key)

    status_area.config(state=tk.NORMAL)
    status_area.delete("1.0", tk.END)
    if is_valid:
        status_area.insert(tk.END, f"Validation Successful: {message}\n\nAPI Key is considered valid for use.")
        root.valid_api_key = entered_api_key
    else:
        status_area.insert(tk.END, f"Validation Failed: {message}\n\nAPI Key is NOT valid or a connection/certificate error occurred. It will not be used.")
        root.valid_api_key = None

    status_area.config(state=tk.DISABLED)
    validate_button.config(state=tk.NORMAL)

def clear_fields():
    """Clears the API key input and status display."""
    api_key_entry.delete(0, tk.END)
    status_area.config(state=tk.NORMAL)
    status_area.delete("1.0", tk.END)
    status_area.config(state=tk.DISABLED)
    root.valid_api_key = None


# --- Main Application Window Setup ---
root = tk.Tk()
root.title("API Key Validator")
root.geometry("600x400")

root.valid_api_key = None

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# API Key Input
api_key_label = tk.Label(root, text="Enter API Key:", font=("Arial", 12, "bold"))
api_key_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Removed show="*" to make the input visible
api_key_entry = tk.Entry(root, width=50, font=("Arial", 10), bd=2, relief="groove")
api_key_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, padx=10, pady=10)

validate_button = tk.Button(button_frame, text="Validate Key", command=perform_validation, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049")
validate_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_fields, font=("Arial", 12, "bold"), bg="#f44336", fg="white", activebackground="#da190b")
clear_button.pack(side=tk.LEFT, padx=5)

# Status Output Area
status_label = tk.Label(root, text="Validation Status:", font=("Arial", 12, "bold"))
status_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

status_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=8, font=("Arial", 10), bd=2, relief="groove")
status_area.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
status_area.config(state=tk.DISABLED)

# Start the Tkinter event loop
root.mainloop()
