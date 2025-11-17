# Kagan Business Management System

A modern, professional Python GUI application for managing multi-purpose businesses including cafe-bar, salon, and gaming net operations. Built with CustomTkinter and SQLAlchemy with a focus on Persian/Farsi language support and RTL layout.

## Features

### 🔐 Security & Authentication
- **Secure Login System**: bcrypt-based password hashing
- **User Roles**: Admin, Manager, and Staff with different permission levels
- **Session Management**: Secure user session handling
- **Password Management**: Change password functionality in settings

### 💼 Business Modules (12 Total)
1. **Salon** - Complete appointment scheduling, service management, and stylist assignment
2. **Cafe** - Menu management, order processing, and inventory tracking with real-time updates
3. **Gamnet** - Gaming net session management and system monitoring
4. **Inventory** - Comprehensive stock management with low-stock alerts
5. **Invoice** - Professional billing and payment processing
6. **Customer** - CRM with loyalty programs and customer history
7. **Employee** - HR management, scheduling, and performance tracking
8. **Reports** - Advanced financial and sales analytics with dashboards
9. **Supplier & Expense** - Procurement and expense tracking
10. **Campaign** - Marketing campaign management
11. **SMS** - Messaging and notification system
12. **Settings** - User preferences, theme switching, and system configuration

### 📊 Reports & Analytics
- **Sales Reports**: Detailed sales analysis with date range filtering
- **Financial Reports**: Revenue, expenses, and profit calculations
- **Dashboard**: Real-time KPIs including:
  - Today's sales
  - Customer count
  - Appointments
  - Weekly revenue
  - Active orders
  - Low stock alerts

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Beautiful gradient-based UI with semi-transparent effects
- **RTL Support**: Full right-to-left layout for Persian/Farsi language
- **Dark/Light Mode**: Theme switching support
- **Responsive Layout**: Adaptive grid layouts and scrollable frames
- **Persian Fonts**: Vazir font for proper Persian text rendering
- **Tabbed Interfaces**: Organized module navigation

### 🗄️ Database Features
- **SQLAlchemy ORM**: Professional database management
- **SQLite Backend**: Lightweight and portable database
- **Comprehensive Models**: 13 database models covering all business entities
- **Session Management**: Proper transaction handling and rollback support
- **Data Integrity**: Foreign key relationships and constraints

### 🛠️ Additional Features
- **Input Validation**: Comprehensive validation for all user inputs
- **Error Handling**: Graceful error handling throughout the application
- **Logging System**: Detailed logging for debugging and auditing
- **Backup & Restore**: Database backup and restore functionality
- **Seed Data**: Sample data generation for testing and demonstration
- **Data Export**: Ready for CSV/PDF export integration

## Requirements

- Python 3.12+
- CustomTkinter 5.2.1
- SQLAlchemy 2.0.23
- bcrypt 4.1.2
- Pillow 10.3.0
- matplotlib 3.8.2
- reportlab 4.0.7
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

4. Initialize database with sample data:
```bash
python seed_data.py
```

## Running the Application

```bash
python main.py
```

### Default Login Credentials

After running `seed_data.py`, you can login with these accounts:

- **Admin**: 
  - Username: `admin`
  - Password: `admin123`
  - Full access to all features

- **Manager**:
  - Username: `manager`
  - Password: `manager123`
  - Access to reports and management features

- **Staff**:
  - Username: `staff`
  - Password: `staff123`
  - Basic access for day-to-day operations

## Project Structure

```
main_kagan_finaly/
├── main.py                      # Application entry point
├── gui.py                       # Main window and login dialog
├── auth.py                      # Authentication service
├── utils.py                     # Utility functions and validators
├── seed_data.py                 # Sample data generation script
├── requirements.txt             # Python dependencies
├── test_app.py                  # Test suite
├── database/                    # Database package
│   ├── __init__.py
│   ├── models.py               # SQLAlchemy models
│   └── db_manager.py           # Database manager and session handling
├── modules/                     # Business modules
│   ├── __init__.py
│   ├── salon_section.py        # Salon management
│   ├── cafe_section.py         # Cafe operations
│   ├── gamnet_section.py       # Gaming net management
│   ├── inventory_section.py    # Inventory management
│   ├── invoice_section.py      # Billing and invoices
│   ├── customer_section.py     # Customer relationship management
│   ├── employee_section.py     # Employee management
│   ├── reports_section.py      # Reports and analytics
│   ├── supplier_expense_section.py  # Supplier and expense tracking
│   ├── campaign_section.py     # Marketing campaigns
│   ├── sms_section.py          # SMS messaging
│   ├── sms_service.py          # SMS service backend
│   └── settings_section.py     # Application settings
└── logs/                        # Application logs (auto-created)
```

## Key Features by Module

### Salon Module
- View and manage appointments
- Service catalog with pricing
- Stylist assignment
- Daily appointment reports
- Appointment status tracking

### Cafe Module
- Active order management
- Menu item display with pricing
- Order status workflow (pending → preparing → ready → paid)
- Daily sales reports
- Table management

### Inventory Module
- Complete product listing
- Stock level monitoring
- Low-stock alerts with highlighting
- Inventory value calculation
- Category-based organization (cafe, salon, general)

### Reports Module
- **Sales Dashboard**: Track daily, weekly, and monthly sales
- **Financial Reports**: Revenue, expenses, and profit analysis
- **Overview Dashboard**: 6 KPI cards with real-time metrics
- **Date Range Filtering**: Flexible report period selection

### Settings Module
- **Appearance**: Light/Dark/System theme switching
- **Account**: View user info and change password
- **Backup & Restore**: Complete database backup and restoration

## Database Schema

The system includes 13 main models:
- **User**: Authentication and user management
- **Customer**: Customer information and loyalty tracking
- **Employee**: Staff information and scheduling
- **Service**: Salon services catalog
- **Appointment**: Salon bookings
- **Product**: Inventory items
- **Order & OrderItem**: Cafe orders
- **GamingSession**: Gaming net sessions
- **Invoice & InvoiceItem**: Billing
- **Supplier**: Vendor management
- **Expense**: Business expenses
- **Campaign**: Marketing campaigns
- **SmsMessage**: SMS messaging

## Development

### Running Tests

```bash
python test_app.py
```

All tests should pass:
- Dependencies check
- Module imports
- Login dialog validation
- Main window validation
- SMS service functionality

### Logging

Logs are automatically created in the `logs/` directory with daily rotation:
- Format: `kagan_YYYYMMDD.log`
- Includes timestamps, log levels, and detailed messages
- Useful for debugging and auditing

### Adding New Features

1. Each module follows the same pattern:
   - Inherits from `ctk.CTkFrame`
   - Implements `setup_ui()` for UI layout
   - Accepts `current_user` parameter
   - Uses database session management

2. Database operations:
   ```python
   with self.db_manager.session_scope() as session:
       # Your database operations
       session.query(Model).filter_by(...).all()
   ```

3. Always use validation from `utils.py`:
   ```python
   Validator.validate_phone(phone)
   Validator.validate_required(value, "Field Name")
   ```

## Technology Stack

- **GUI Framework**: CustomTkinter (pure Python, cross-platform)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: bcrypt for password hashing
- **Base Library**: tkinter (Python's standard GUI library)
- **Reporting**: matplotlib for charts (ready for integration)
- **PDF Generation**: reportlab (ready for integration)
- **Language**: Python 3.12+

## Design Philosophy

- **Pure Python**: No C++ build tools required (unlike PyQt5)
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **RTL-First**: Optimized for Persian/Farsi with right-to-left layout
- **Modern UI**: Glassmorphism design with smooth gradients
- **Modular**: Clean separation of concerns
- **Production-Ready**: Proper error handling, logging, and data integrity

## Security Best Practices

1. **Passwords**: Never stored in plain text - always hashed with bcrypt
2. **Sessions**: Proper session management with database cleanup
3. **Input Validation**: All user inputs validated before database operations
4. **SQL Injection**: Protected by SQLAlchemy ORM parameterization
5. **Logging**: Sensitive data never logged
6. **Backups**: Regular database backups recommended

## Troubleshooting

### Database Issues
- Delete `kagan_db.sqlite` and run `python seed_data.py` to recreate
- Check `logs/` directory for detailed error messages

### GUI Issues
- Ensure tkinter is installed: `python -c "import tkinter"`
- Try different theme: Settings → Appearance → Light/Dark mode

### Import Errors
- Verify all dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.12+)

## Future Enhancements

- [ ] Chart visualization in reports (matplotlib integration ready)
- [ ] CSV/PDF export for reports
- [ ] Real SMS API integration
- [ ] Multi-language support beyond Persian
- [ ] Advanced search and filtering
- [ ] Email notifications
- [ ] Mobile app companion
- [ ] Cloud database support
- [ ] Advanced analytics with AI insights

## Contributing

This is a demonstration project showcasing modern Python GUI development with:
- Professional database integration
- Secure authentication
- Persian language support
- Modern UI/UX patterns
- Production-ready code structure

## License

Copyright © 2025 Kagan Business Management

## Support

For issues, questions, or contributions, please refer to the project repository.

---

**Built with ❤️ for Persian-speaking business owners**