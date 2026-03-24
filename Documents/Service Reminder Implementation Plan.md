# Service Reminder Implementation Plan

## Context
Create a standalone application that automates the process of checking tomorrow's appointments from a Nextcloud CalDAV server, identifying service appointments, retrieving relevant service information from PDF service books, converting those pages to images, and sending them as WhatsApp messages to designated recipients.

## Approach
1. **Calendar Integration**: Connect to Nextcloud CalDAV to fetch tomorrow's appointments
2. **Service Detection**: Filter appointments to identify service-related entries
3. **PDF Processing**: Look up and extract relevant pages from PDF service books
4. **Image Conversion**: Convert PDF pages to WhatsApp-compatible images
5. **WhatsApp Distribution**: Send images via WhatsApp API to multiple recipients
6. **Logging & Error Handling**: Comprehensive logging and graceful error recovery
7. **Configuration**: Secure handling of credentials and settings via environment variables

## Files to Create
- **Main Application**: `nextcloud_service_reminder.py` - Core application logic
- **Configuration**: `.env.example` - Template for environment variables
- **Dependencies**: `requirements.txt` - Python package requirements
- **Documentation**: `README.md` - Usage instructions
- **Logging**: `logs/` directory for application logs
- **Service Books**: `diensten/` directory (already exists) for PDF files

## Technical Components
- **CalDAV Client**: `caldav` library for Nextcloud calendar access
- **PDF Processor**: `PyMuPDF` (fitz) for PDF text extraction and page conversion
- **Image Handler**: `Pillow` for image processing and WhatsApp optimization
- **WhatsApp Gateway**: `requests` for WhatsApp Cloud API communication
- **Environment Management**: `python-dotenv` for loading configuration
- **Scheduling**: `schedule` library for built-in scheduling (optional)
- **Logging**: Standard `logging` module for application logging

## Implementation Phases

### Phase 1: Foundation
- Set up project structure and dependencies
- Implement Nextcloud CalDAV connection and event fetching
- Create basic logging and error handling

### Phase 2: Service Detection
- Implement logic to identify service appointments from calendar events
- Create mapping between event data and service book PDFs

### Phase 3: PDF Processing
- Implement PDF text search to find service information
- Extract relevant pages based on service identification
- Convert PDF pages to image format

### Phase 4: WhatsApp Integration
- Set up WhatsApp Cloud API client
- Implement image sending functionality
- Handle multi-page services and media limitations

### Phase 5: Configuration & Reliability
- Implement environment variable configuration
- Add comprehensive error handling and logging
- Add duplicate prevention mechanisms
- Implement scheduling capabilities

## Dependencies
- `caldav` - Nextcloud CalDAV access
- `PyMuPDF` - PDF processing (fitz)
- `Pillow` - Image processing
- `requests` - HTTP client for WhatsApp API
- `python-dotenv` - Environment variable management
- `schedule` - Optional built-in scheduling
- `logging` - Standard library (no install needed)

## Verification Approach
- Unit test each component independently
- Integration test with sample calendar data and PDF files
- Verify WhatsApp message formatting and delivery
- Test error conditions (network failures, missing files, etc.)
- Validate image size and format compliance with WhatsApp limits
- Ensure secure handling of credentials (no logging/exposure)
