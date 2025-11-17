# Kagan Business Management System

A modern Python GUI application for managing multi-purpose businesses including cafe-bar, salon, and gaming net operations.

## Features

- **Modern Glassmorphism Design**: Beautiful gradient-based UI with semi-transparent glass-like effects
- **CustomTkinter**: Built with CustomTkinter for a modern, cross-platform GUI (pure Python, no C++ build tools required)
- **RTL Support**: Full right-to-left layout support for Persian language
- **Vazir Font**: Uses Vazir font for proper Persian text rendering
- **Secure Login System**: Username and password-based authentication
- **12 Business Modules**:
  1. **Salon** - Salon services and appointment management
  2. **Cafe** - Cafe/bar orders and menu management
  3. **Gamnet** - Gaming net sessions and system management
  4. **Inventory** - Stock and product management
  5. **Invoice** - Billing and payment processing
  6. **Customer** - Customer information and CRM
  7. **Employee** - HR and employee management
  8. **Reports** - Financial and managerial reports with filters
  9. **Supplier & Expense** - Supplier and procurement management
  10. **Campaign** - Marketing campaigns
  11. **SMS** - SMS messaging and notifications
  12. **Settings** - Application configuration

## Requirements

- Python 3.12+
- CustomTkinter 5.2.1
- Pillow 10.1.0
- tkinter (system package)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mhmdhosn82/main_kagan_finaly.git
cd main_kagan_finaly
```

2. Install system dependencies (tkinter):
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On Fedora
sudo dnf install python3-tkinter

# On macOS (usually included with Python)
# No action needed

# On Windows (usually included with Python installer)
# Make sure to check "tcl/tk and IDLE" during Python installation
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

### Login Credentials

For testing purposes, the application accepts any non-empty username and password.
In production, this should be replaced with proper database-backed authentication.

## Project Structure

```
main_kagan_finaly/
├── main.py                 # Application entry point
├── gui.py                  # Main window and login dialog
├── requirements.txt        # Python dependencies
├── modules/                # Business modules
│   ├── __init__.py
│   ├── salon_section.py
│   ├── cafe_section.py
│   ├── gamnet_section.py
│   ├── inventory_section.py
│   ├── invoice_section.py
│   ├── customer_section.py
│   ├── employee_section.py
│   ├── reports_section.py
│   ├── supplier_expense_section.py
│   ├── campaign_section.py
│   ├── sms_section.py
│   ├── sms_service.py
│   └── settings_section.py
└── README.md
```

## Development

### Module Structure

Each module follows the same pattern:
- Inherits from `ctk.CTkFrame`
- Implements `setup_ui()` for UI layout
- Uses CustomTkinter components
- Contains placeholder content for future implementation

### Adding New Features

1. Each module can be extended with specific business logic
2. Database integration can be added to the modules
3. Reports module supports filters for financial and managerial reporting
4. SMS module uses `sms_service.py` for actual SMS operations

### Testing

Run the test suite to verify all components:

```bash
python test_app.py
```

## Technology Stack

- **GUI Framework**: CustomTkinter (pure Python, no C++ build tools required)
- **Base Library**: tkinter (Python's standard GUI library)
- **Image Processing**: Pillow
- **Language**: Python 3.12+

## Design Philosophy

- **Pure Python**: No dependencies requiring C++ build tools (unlike PyQt5)
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **RTL Support**: Optimized for Persian language with right-to-left layout
- **Modern UI**: Glassmorphism design with smooth gradients and transparency
- **Modular**: Clean separation of concerns with independent modules

## License

Copyright © 2025 Kagan Business Management