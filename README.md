# PostgreSQL Query, Export, and Email Tool

An interactive Python application for connecting to PostgreSQL databases, querying tables, exporting to Excel/PDF, and sending email reports.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive tool
python main.py
```

## 📚 Documentation

All documentation is available in the [`docs/`](docs/) directory:

- **[docs/QUICK_START.md](docs/QUICK_START.md)** - Get started in 5 minutes
- **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Complete setup and usage guide
- **[docs/EMAIL_SETUP.md](docs/EMAIL_SETUP.md)** - Gmail & Outlook email configuration
- **[docs/SCHEDULER_GUIDE.md](docs/SCHEDULER_GUIDE.md)** - Task scheduler setup and deployment
- **[docs/WINDOWS_TASK_SCHEDULER_SETUP.md](docs/WINDOWS_TASK_SCHEDULER_SETUP.md)** - Windows 11 Task Scheduler setup (recommended for Windows)
- **[docs/SCHEDULER_QUICK_REFERENCE.md](docs/SCHEDULER_QUICK_REFERENCE.md)** - Quick scheduler commands
- **[docs/GUIDES_INDEX.md](docs/GUIDES_INDEX.md)** - Documentation index

## ✨ Features

- ✅ **PostgreSQL Support** - Connect to PostgreSQL databases
- ✅ **Interactive Prompts** - Step-by-step guided workflow
- ✅ **Excel & PDF Export** - Export query results to multiple formats
- ✅ **Email Functionality** - Send reports via Gmail or Outlook
- ✅ **Multiple Recipients** - Send to multiple email addresses (TO and CC)
- ✅ **Table Discovery** - Automatically lists available tables
- ✅ **Sample Tables** - Create sample tables with dummy data
- ✅ **Task Scheduler** - Schedule automated queries and email reports
- ✅ **Clean Architecture** - SOLID principles, maintainable code

## 🏗️ Project Structure

```
oracle_db_connection/
├── main.py                 # Main application entry point
├── src/                    # Source code
│   ├── core/              # Core interfaces and config
│   ├── adapters/         # Database adapters (PostgreSQL)
│   └── services/         # Business logic services
├── docs/                  # Documentation
│   ├── QUICK_START.md
│   ├── SETUP_GUIDE.md
│   ├── EMAIL_SETUP.md
│   └── GUIDES_INDEX.md
├── env.example           # Example environment configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 📋 Requirements

- Python 3.8+
- PostgreSQL database access
- See [requirements.txt](requirements.txt) for Python packages

## 🔧 Configuration

### Database URL

Enter PostgreSQL database URL when prompted, or configure in `.env`:

```env
POSTGRESQL_DATABASE_URL=postgresql://username:password@host:5432/database
```

### Email Configuration

Email settings are prompted interactively (not from .env). You'll be asked for:
- SMTP Email (e.g., your_email@gmail.com)
- SMTP Password (App Password)
- SMTP Host (default: smtp.gmail.com)
- SMTP Port (default: 587)

## 📖 Usage Example

### Interactive Mode

```
1. Run: python main.py
2. Enter PostgreSQL database URL
3. Select table or enter custom query
4. Choose export format (Excel/PDF)
5. Optionally send email with attachments
```

### Scheduled Tasks (New! 🎉)

Schedule automated database queries and email reports:

```bash
# Add a scheduled task
python manage_tasks.py add

# List all tasks
python manage_tasks.py list

# Windows 11: Use Windows Task Scheduler (recommended)
# See: docs/WINDOWS_TASK_SCHEDULER_SETUP.md

# Or start scheduler daemon (runs continuously)
python scheduler_daemon.py
```

**Features:**
- ✅ Schedule queries using cron, intervals, or one-time
- ✅ Automatic email reports with Excel/PDF attachments
- ✅ Task management CLI (add, list, enable, disable, delete)
- ✅ Execution history and error tracking
- ✅ **Windows Task Scheduler integration** (Windows 11)
- ✅ Deploy to cloud or run locally

**Windows Users:** Use Windows Task Scheduler - no daemon needed! See [docs/WINDOWS_TASK_SCHEDULER_SETUP.md](docs/WINDOWS_TASK_SCHEDULER_SETUP.md)

See [docs/SCHEDULER_GUIDE.md](docs/SCHEDULER_GUIDE.md) for complete scheduler documentation.

## 🔄 How It Works

### Application Workflow

The application follows a sequential, interactive workflow:

```
1. Initialization
   ├── Load configuration from .env (optional)
   ├── Initialize PromptService for user interaction
   └── Initialize QueryService for orchestration

2. Database Connection
   ├── Prompt for PostgreSQL database URL (or use from .env)
   ├── Create database adapter via Factory pattern
   ├── Test connection with status feedback
   ├── List available tables in database
   └── Optionally create sample table if none exist

3. Query Input
   ├── Display available tables (numbered list)
   ├── User selects table by number OR enters custom SQL query
   └── Support for multi-line queries (type 'END' to finish)

4. Export Configuration
   ├── Choose export format (Excel only, PDF only, or both)
   ├── Specify output file paths
   └── Optionally configure email settings

5. Execution & Export
   ├── Execute SQL query via database adapter
   ├── Convert results to pandas DataFrame
   ├── Export to Excel (if selected)
   ├── Export to PDF (if selected)
   └── Send email with attachments (if selected)

6. Cleanup
   └── Close database connections
```

### Data Flow

```
User Input → PromptService → QueryService → DatabaseAdapter
                                              ↓
                                         DataFrame
                                              ↓
                                    ExportService (Excel/PDF)
                                              ↓
                                    EmailService (if enabled)
                                              ↓
                                         Output Files/Email
```

## 🏛️ System Design

### Architecture Overview

The application follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│                      (main.py)                           │
│  - User interaction orchestration                        │
│  - Input validation and prompting                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Application Layer                     │
│                  (src/services/)                        │
│  - QueryService: Orchestrates query execution           │
│  - ExportService: Handles Excel/PDF export              │
│  - EmailService: Manages email sending                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Domain Layer                         │
│                   (src/core/)                           │
│  - DatabaseAdapter: Abstract interface                   │
│  - Config: Configuration management                     │
│  - Prompts: User interaction service                    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Infrastructure Layer                    │
│              (src/adapters/database/)                    │
│  - PostgreSQLAdapter: Database implementation          │
│  - DatabaseAdapterFactory: Adapter creation            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  External Systems                        │
│  - PostgreSQL Database                                   │
│  - SMTP Email Server (Gmail/Outlook)                     │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Dependency Inversion**: High-level modules depend on abstractions (interfaces), not concrete implementations
2. **Single Responsibility**: Each class has one clear purpose
3. **Open/Closed**: Open for extension (new adapters), closed for modification
4. **Separation of Concerns**: Clear boundaries between layers
5. **Factory Pattern**: Centralized adapter creation
6. **Adapter Pattern**: Unified interface for different database types

## 📐 High Level Design (HLD)

### Component Diagram

```
┌──────────────┐
│   main.py    │
│  (Orchestrator)│
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
┌──────▼──────┐   ┌──────▼──────┐
│PromptService│   │QueryService │
│             │   │             │
│- prompt_*() │   │- execute_*()│
└─────────────┘   └──────┬──────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
   ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
   │Database     │ │Export     │ │Email      │
   │Adapter      │ │Service    │ │Service    │
   │             │ │           │ │           │
   │- connect()  │ │- export() │ │- send_*() │
   │- execute_*()│ └───────────┘ └───────────┘
   └──────┬──────┘
          │
   ┌──────▼──────┐
   │PostgreSQL   │
   │Database     │
   └─────────────┘
```

### Sequence Diagram

```
User    main.py    PromptService  QueryService  DatabaseAdapter  ExportService  EmailService
 │         │            │              │              │                │              │
 │         │──init──────>│              │              │                │              │
 │         │            │              │              │                │              │
 │         │<─prompt─────│              │              │                │              │
 │<────────│             │              │              │                │              │
 │────────>│             │              │              │                │              │
 │         │──create────>│              │              │                │              │
 │         │            │              │              │                │              │
 │         │            │              │──execute─────>│                │              │
 │         │            │              │              │──query────────>│              │
 │         │            │              │<─DataFrame───│                │              │
 │         │            │              │              │                │              │
 │         │            │              │──export──────>│                │              │
 │         │            │              │              │                │              │
 │         │            │              │──send────────>│                │              │
 │         │            │              │              │                │              │
 │<────────│             │              │              │                │              │
```

### Key Components

#### 1. **Presentation Layer** (`main.py`)
- **Responsibility**: Application entry point and user interaction orchestration
- **Key Functions**:
  - Initialize services
  - Coordinate user prompts
  - Handle connection testing
  - Manage table discovery
  - Error handling and user feedback

#### 2. **Application Services** (`src/services/`)
- **QueryService**: Orchestrates query execution, export, and email sending
- **ExportService**: Handles Excel and PDF export operations
- **EmailService**: Manages SMTP email sending with attachments

#### 3. **Domain Layer** (`src/core/`)
- **DatabaseAdapter**: Abstract interface defining database operations contract
- **Config**: Configuration management and environment variable handling
- **PromptService**: User interaction and input collection

#### 4. **Infrastructure Layer** (`src/adapters/`)
- **PostgreSQLAdapter**: Concrete implementation of DatabaseAdapter for PostgreSQL
- **DatabaseAdapterFactory**: Factory for creating appropriate database adapters

## 🔧 Low Level Design (LLD)

### Class Diagram

```
┌─────────────────────────────────────┐
│      DatabaseAdapter (ABC)         │
├─────────────────────────────────────┤
│ + connect() : void                  │
│ + disconnect() : void               │
│ + execute_query(query: str)        │
│   : DataFrame                       │
│ + list_tables() : List[str]         │
│ + table_exists(name: str) : bool    │
│ + create_sample_table(name: str)    │
│   : void                            │
│ + __enter__() : DatabaseAdapter     │
│ + __exit__(...) : void              │
└──────────────┬──────────────────────┘
               │ implements
               │
┌──────────────▼──────────────────────┐
│    PostgreSQLAdapter                │
├─────────────────────────────────────┤
│ - database_url: str                  │
│ - engine: Engine                    │
├─────────────────────────────────────┤
│ + connect() : void                  │
│ + disconnect() : void               │
│ + execute_query(query: str)         │
│   : DataFrame                       │
│ + list_tables() : List[str]         │
│ + table_exists(name: str) : bool    │
│ + create_sample_table(name: str)    │
│   : void                            │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      DatabaseAdapterFactory          │
├─────────────────────────────────────┤
│ + create(type: str, url: str)       │
│   : DatabaseAdapter                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         QueryService                 │
├─────────────────────────────────────┤
│ - config: Config                    │
│ - excel_service: ExcelExportService  │
│ - pdf_service: PDFExportService     │
├─────────────────────────────────────┤
│ + execute_and_export(...) : dict    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         EmailService                 │
├─────────────────────────────────────┤
│ - smtp_user: str                    │
│ - smtp_password: str                │
│ - smtp_host: str                    │
│ - smtp_port: int                    │
├─────────────────────────────────────┤
│ + send_email(...) : void            │
│ - _convert_to_html(df) : str        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│        PromptService                 │
├─────────────────────────────────────┤
│ + prompt_database_url(...) : str     │
│ + prompt_query(tables: List) : str  │
│ + prompt_export_options() : dict   │
│ + prompt_email_config() : dict      │
│ + prompt_email_recipients() : List  │
└─────────────────────────────────────┘
```

### Interface Contracts

#### DatabaseAdapter Interface

```python
class DatabaseAdapter(ABC):
    """Abstract interface for database adapters."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""
        
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection."""
        
    @abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame."""
        
    @abstractmethod
    def list_tables(self) -> List[str]:
        """List all tables in the database."""
        
    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists."""
        
    @abstractmethod
    def create_sample_table(self, table_name: str) -> None:
        """Create sample table with dummy data."""
```

### Design Patterns Implementation

#### 1. Factory Pattern
**Location**: `src/adapters/database/factory.py`

```python
class DatabaseAdapterFactory:
    @staticmethod
    def create(database_type: str, database_url: str) -> DatabaseAdapter:
        """Creates appropriate database adapter based on type."""
        if database_type in ["postgresql", "postgres"]:
            return PostgreSQLAdapter(database_url)
        else:
            raise ValueError(f"Unsupported database type: {database_type}")
```

**Benefits**:
- Centralized adapter creation
- Easy to extend with new database types
- Encapsulates creation logic

#### 2. Adapter Pattern
**Location**: `src/adapters/database/postgresql_adapter.py`

```python
class PostgreSQLAdapter(DatabaseAdapter):
    """Adapts PostgreSQL-specific operations to DatabaseAdapter interface."""
    
    def execute_query(self, query: str) -> pd.DataFrame:
        # PostgreSQL-specific implementation
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
```

**Benefits**:
- Unified interface for different databases
- Isolates database-specific code
- Enables easy swapping of implementations

#### 3. Dependency Injection
**Location**: `src/services/query_service.py`

```python
class QueryService:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()  # Dependency injection
        self.excel_service = ExcelExportService()
        self.pdf_service = PDFExportService()
```

**Benefits**:
- Loose coupling
- Easy testing (can inject mocks)
- Flexible configuration

#### 4. Context Manager Pattern
**Location**: `src/adapters/database/postgresql_adapter.py`

```python
class PostgreSQLAdapter(DatabaseAdapter):
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
```

**Benefits**:
- Automatic resource cleanup
- Exception-safe connection handling
- Cleaner code with `with` statements

### Data Structures

#### Query Result Flow

```
SQL Query → DatabaseAdapter.execute_query()
              ↓
         SQLAlchemy Result
              ↓
         pandas DataFrame
              ↓
    ExportService.export()
              ↓
    Excel/PDF File
              ↓
    EmailService.send_email()
              ↓
    Email with Attachments
```

#### Configuration Flow

```
.env file → Config class
              ↓
    Environment Variables
              ↓
    PromptService (optional override)
              ↓
    Service Initialization
```

### Error Handling Strategy

1. **Connection Errors**: DNS resolution check → Connection attempt → Detailed error messages
2. **Query Errors**: SQL validation → Execution → DataFrame conversion → Error propagation
3. **Export Errors**: File path validation → Permission check → Export attempt → Error handling
4. **Email Errors**: SMTP connection → Authentication → Send attempt → Fallback mechanisms

### Extension Points

1. **New Database Types**: Implement `DatabaseAdapter` interface and add to `DatabaseAdapterFactory`
2. **New Export Formats**: Create new export service implementing export protocol
3. **New Email Providers**: Extend `EmailService` with provider-specific logic
4. **New Prompt Types**: Add methods to `PromptService` for new user interactions

## 🆘 Need Help?

- Check [docs/QUICK_START.md](docs/QUICK_START.md) for quick setup
- See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for complete guide
- Review [docs/EMAIL_SETUP.md](docs/EMAIL_SETUP.md) for email configuration
- Browse [docs/GUIDES_INDEX.md](docs/GUIDES_INDEX.md) for all documentation

---

**For detailed documentation, see the [docs/](docs/) directory.**
