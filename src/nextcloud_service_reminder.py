#!/usr/bin/env python3
"""
Nextcloud Service Reminder Application
Main entry point for the service reminder automation.
"""

import os
import logging
import sys
import json
from pathlib import Path
from typing import Dict, Optional

# Import project-specific modules
from dotenv import load_dotenv

# Import libraries for different components
import caldav  # Nextcloud CalDAV access
import fitz  # PyMuPDF for PDF processing
from PIL import Image  # Image processing for WhatsApp
import requests  # WhatsApp API communication

# Configure logging with detailed format
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
CREDENTIALS_FILE = Path("/home/eddy/src/tomorrow/credentials.json")
SERVICE_BOOKS_DIR = Path("/home/eddy/src/tomorrow/diensten")
TIMEZONE = "UTC"  # Adjust as needed

# Global configuration variable
CONFIG = None


def load_credentials_file() -> Dict[str, str]:
    """Load credentials from credentials.json file."""
    if not CREDENTIALS_FILE.exists():
        logger.warning(f"Credentials file not found at {CREDENTIALS_FILE}")
        return None

    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)
        logger.info("Credentials loaded from file")
        return credentials
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to read credentials file: {e}")
        return None


def create_credentials_template() -> None:
    """Create a template credentials file for onboarding."""
    template = {
        "NEXTCLOUD_URL": "https://your-nextcloud-domain.com/nextcloud/",
        "NEXTCLOUD_USER": "your_username",
        "NEXTCLOUD_PASS": "your_password",
        "TIMEZONE": "Europe/Amsterdam",
        "WHATSAPP_API_URL": "https://api.whatsapp.com/v1/",
        "WHATSAPP_API_TOKEN": "your_whatsapp_token"
    }

    try:
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(template, f, indent=4)
        logger.info(f"Created credentials template at {CREDENTIALS_FILE}")
        print(f"\n📝 Credentials template created at: {CREDENTIALS_FILE}")
        print("Please edit this file with your actual credentials before running the application.")
    except IOError as e:
        logger.error(f"Failed to create credentials template: {e}")
        raise


def load_configuration() -> Dict[str, str]:
    """Load and validate configuration settings from credentials file."""
    # Try to load from credentials.json first
    credentials = load_credentials_file()

    if credentials is None:
        logger.warning("No credentials found. Creating template for onboarding.")
        create_credentials_template()
        raise EnvironmentError(
            "Please edit the credentials.json file with your actual credentials and try again."
        )

    # Map credentials to expected configuration keys
    config = {
        "caldav_url": credentials.get("NEXTCLOUD_URL", "https://nextcloud.example.com/nextcloud/"),
        "caldav_user": credentials.get("NEXTCLOUD_USER", "your_username"),
        "caldav_password": credentials.get("NEXTCLOUD_PASS", "your_password"),
        "whatsapp_api_url": credentials.get("WHATSAPP_API_URL", "https://api.whatsapp.com/v1/"),
        "whatsapp_api_token": credentials.get("WHATSAPP_API_TOKEN", "your_token"),
        "timezone": credentials.get("TIMEZONE", "UTC")
    }

    # Check for missing required values
    missing = [key for key, value in config.items() if not value or value.endswith("example.com") or value == "your_username"]
    if missing:
        logger.error(f"Missing or invalid required values in credentials: {missing}")
        logger.info("Please update the credentials.json file with your actual values.")
        raise EnvironmentError(f"Missing or invalid credentials for: {missing}")

    logger.info("Configuration loaded successfully from credentials file")
    return config


def initialize_logging():
    """Configure and initialize logging system."""
    logger.info("Initializing logging system...")


def initialize_configuration():
    """Load and initialize configuration settings."""
    global CONFIG
    try:
        CONFIG = load_configuration()
        logger.info("Configuration initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize configuration: {e}")
        raise


def validate_config():
    """Validate configuration parameters."""
    if not all(key in CONFIG for key in CONFIG):
        missing = [key for key in CONFIG if key not in CONFIG]
        logger.error(f"Missing configuration keys: {missing}")
        raise EnvironmentError(f"Missing configuration: {missing}")

    # Additional validation can be added here
    if not CONFIG["caldav_user"] or not CONFIG["caldav_password"]:
        logger.error("CalDAV credentials are empty")
        raise ValueError("CalDAV username or password cannot be empty")

    logger.info("Configuration validation passed")


def connect_to_caldav() -> caldav.Calendar:
    """Establish connection to Nextcloud CalDAV server and return calendar object."""
    try:
        # Create CalDAV client
        client = caldav.DAVClient(
            url=CONFIG["caldav_url"],
            username=CONFIG["caldav_user"],
            password=CONFIG["caldav_password"]
        )

        # Connect and get a calendar
        client.login()
        calendar = client.get_default_calendar()
        logger.info("Connected to CalDAV server successfully")
        return calendar
    except Exception as e:
        logger.error(f"Failed to connect to CalDAV server: {e}")
        raise


def get_tomorrow_appointments(calendar: caldav.Calendar) -> list:
    """Get all appointments for tomorrow."""
    try:
        # Get tomorrow's date (simplified - in production, use proper date handling)
        from datetime import datetime, timedelta
        tomorrow = datetime.now() + timedelta(days=1)

        # Fetch events (simplified - in production, use proper CalDAV queries)
        events = calendar.events()
        tomorrow_events = []

        for event in events:
            # Simplified check - in production, parse actual event dates
            if "tomorrow" in event.vobject_instance.vevent.summary.value.lower():
                tomorrow_events.append(event)

        logger.info(f"Found {len(tomorrow_events)} appointments for tomorrow")
        return tomorrow_events

    except Exception as e:
        logger.error(f"Failed to fetch tomorrow's appointments: {e}")
        raise


def main():
    """Main entry point for the application."""
    logger.info("Starting Nextcloud Service Reminder Application...")

    try:
        # Initialize components
        initialize_logging()
        initialize_configuration()
        validate_config()

        # TODO: Implement core functionality steps:
        # 1. Connect to CalDAV and fetch tomorrow's appointments
        # 2. Process appointments to identify service-related events
        # 3. Extract relevant pages from service books (PDFs)
        # 4. Convert PDF pages to WhatsApp images
        # 5. Send images via WhatsApp Cloud API

        logger.info("Foundation setup completed successfully")
        logger.info("Proceeding to implement core functionality...")

    except Exception as e:
        error_details = {
            'message': str(e),
            'type': type(e).__name__,
            'category': 'INITIALIZATION_ERROR'
        }
        logger.error(f"Application initialization failed: {e}", exc_info=True)
        # Re-raise to ensure we know the application failed
        raise


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        logger.info(f"Application exited with code {e.code}")
        sys.exit(e.code)
    except Exception as e:
        logger.error(f"Uncaught application error: {e}")
        sys.exit(1)