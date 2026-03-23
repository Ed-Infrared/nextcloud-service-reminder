# Nextcloud Service Reminder Application

## Purpose
This application automates the process of checking tomorrow's appointments from a Nextcloud CalDAV server, identifying service appointments, retrieving relevant service information from PDF service books, converting those pages to images, and sending them as WhatsApp messages to designated recipients.

## Core Functionality

### 1. Calendar Integration
- Connect to Nextcloud CalDAV server using CalDAV protocol
- Retrieve all appointments for the next calendar day (00:00 to 23:59)
- Filter appointments to identify service-related entries based on:
  - Event title containing service keywords
  - Event description/location fields
  - Custom properties or categories

### 2. Service Information Processing
- For each identified service appointment:
  - Look up the corresponding service in the service book PDF collection
  - Extract the relevant page(s) for that service from the PDF
  - Convert extracted PDF pages to image format (PNG/JPG) suitable for WhatsApp
  - Handle multi-page services by converting all relevant pages

### 3. WhatsApp Distribution
- Send the generated service images as WhatsApp messages
- Support for sending to multiple recipients simultaneously
- Handle WhatsApp media limitations (file size, format constraints)
- Include optional caption/context with each image

## Technical Implementation

### Required Components
- **CalDAV Client**: For Nextcloud calendar access (e.g., `caldav` Python library)
- **PDF Processor**: For extracting and converting PDF pages (e.g., `pdf2image`, `PyMuPDF`)
- **Image Handler**: For optimizing images for WhatsApp (e.g., `Pillow`)
- **WhatsApp Gateway**: For sending messages (could use WhatsApp Business API or automation tools)

### File Structure
```
/home/eddy/src/tomorrow/
├── nextcloud_tomorrow.py        # Main application logic
├── diensten/                    # Directory containing service book PDFs
│   ├── dienst1.pdf
│   ├── dienst2.pdf
│   └── ...
├── credentials.json             # Nextcloud authentication credentials
├── .env                         # Environment variables (WhatsApp config, etc.)
├── logs/                        # Application logs
│   └── service_reminder.log
├── README.md                    # This documentation
└── requirements.txt             # Python dependencies
```

### Configuration
- **Nextcloud**: Server URL, username, password/app-token, calendar name
- **Service Books**: Path to `diensten/` directory containing PDF files
- **WhatsApp**: API credentials or automation setup for message sending
- **Scheduling**: Cron job or scheduler to run daily (preferably early morning)
- **Logging**: Log level and output preferences

### Workflow
1. **Daily Trigger**: Application runs via scheduled task (cron)
2. **Calendar Sync**: Fetch tomorrow's appointments from Nextcloud
3. **Service Detection**: Identify which appointments are services
4. **PDF Lookup**: For each service, find matching PDF in `diensten/` directory
5. **Page Extraction**: Extract relevant service page(s) from PDF
6. **Image Conversion**: Convert PDF pages to WhatsApp-compatible images
7. **Message Distribution**: Send images via WhatsApp to configured recipients
8. **Logging**: Record successes, failures, and notifications for monitoring

## Dependencies
- Python 3.7+
- `caldav` - For Nextcloud calendar access
- `pdf2image` or `PyMuPDF` - For PDF to image conversion
- `Pillow` - For image processing/optimization
- WhatsApp communication method (varies by implementation)
- `python-dotenv` - For environment variable management
- Optional: `schedule` or `APScheduler` for built-in scheduling

## Error Handling & Reliability
- Graceful handling of network failures (Nextcloud, WhatsApp)
- Validation of PDF existence and accessibility
- Image size optimization for WhatsApp limits
- Detailed logging for troubleshooting
- Notification mechanisms for critical failures
- Duplicate prevention (avoid sending same reminder multiple times)

## Security Considerations
- Secure storage of credentials (encrypted or environment variables)
- Minimal permission principle for service accounts
- Audit logging for access and operations
- Secure handling of PDF service books (if sensitive)

## Usage
1. Place service book PDFs in the `diensten/` directory
2. Configure `credentials.json` with Nextcloud access details
3. Set up WhatsApp sending mechanism in `.env` or code
4. Test with a known service appointment
5. Schedule daily execution via cron (e.g., `0 6 * * * /path/to/python nextcloud_tomorrow.py`)
6. Monitor logs in `logs/` directory for operational insights

## Future Enhancements
- Web interface for configuration and monitoring
- Service book management interface (upload/update PDFs)
- Recipient group management
- Delivery receipts and read confirmations
- Multi-language support for service names
- Integration with other messaging platforms (Telegram, Signal, etc.)