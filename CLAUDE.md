# CLAUDE.md - AI Assistant Guide for KATOTTG Tree

> **Last Updated:** 2025-12-05
> **Version:** 0.0.1
> **Purpose:** Comprehensive guide for AI assistants working with the KATOTTG Tree codebase

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Codebase Structure](#codebase-structure)
4. [Development Environment](#development-environment)
5. [Code Conventions](#code-conventions)
6. [Key Components](#key-components)
7. [API Reference](#api-reference)
8. [Frontend Components](#frontend-components)
9. [Database Schema](#database-schema)
10. [Testing](#testing)
11. [Common Tasks](#common-tasks)
12. [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## Project Overview

### What is KATOTTG Tree?

**KATOTTG Tree** is a Frappe custom application for managing the Ukrainian KATOTTG (Кодифікатор адміністративно-територіальних одиниць та територій громад) classification system. KATOTTG is the official coding system for administrative and territorial units in Ukraine.

### Key Features

- **Hierarchical Tree Management:** 5-level nested set structure for territorial units
- **Excel Import System:** Bulk import from Excel files with progress tracking
- **Fuzzy Search:** Intelligent search with relevance scoring (4-level algorithm)
- **Custom UI Components:** Enhanced selection dialogs with cascading dropdowns
- **Caching System:** Performance optimization with configurable TTL
- **Ukrainian Localization:** Full Ukrainian language support throughout

### Project Metadata

- **App Name:** `katottg_tree`
- **Version:** `0.0.1`
- **Author:** Maxim S (maks4a@gmail.com)
- **License:** MIT
- **Framework:** Frappe Framework (~15.0.0)
- **Python:** 3.10+
- **Repository Branch:** Main development on feature branches starting with `claude/`

---

## Technology Stack

### Backend

- **Framework:** Frappe Framework (Python-based)
- **Database:** MariaDB/PostgreSQL (via Frappe)
- **Python Version:** 3.10+
- **Build System:** flit_core
- **Background Jobs:** Frappe's background job system

### Frontend

- **Framework:** Frappe's frontend (jQuery-based)
- **JavaScript:** ES2022
- **Styling:** CSS/SCSS (via Frappe)
- **UI Components:** Frappe's Form, Dialog, Tree components

### Development Tools

- **Linter (Python):** Ruff (replaces Flake8, isort, Black)
- **Linter (JavaScript):** ESLint
- **Formatter (JS/Vue/SCSS):** Prettier
- **Pre-commit Hooks:** pre-commit framework
- **Type Checking:** Python type annotations (auto-exported)

---

## Codebase Structure

```
katottg_tree/
├── .git/                           # Git repository
├── .pre-commit-config.yaml         # Pre-commit hooks configuration
├── .editorconfig                   # Editor configuration
├── .eslintrc                       # ESLint configuration
├── .gitignore                      # Git ignore rules
├── pyproject.toml                  # Python project configuration & Ruff settings
├── license.txt                     # MIT license
├── README.md                       # Basic installation guide
├── FUZZY_SEARCH.md                 # Fuzzy search feature documentation (Ukrainian)
├── CLAUDE.md                       # This file - AI assistant guide
├── test_fuzzy_search.py            # Standalone fuzzy search test script
│
└── katottg_tree/                   # Main app module
    ├── __init__.py
    ├── hooks.py                    # App hooks and configuration
    │
    ├── config/                     # App configuration
    │   └── __init__.py
    │
    ├── templates/                  # Page templates
    │   ├── __init__.py
    │   └── pages/
    │       └── __init__.py
    │
    ├── public/                     # Static assets
    │   └── js/
    │       └── katottg_link_control.js  # Custom Link control (globally included)
    │
    ├── utils/                      # Utility modules
    │   ├── api.py                  # Whitelisted API methods
    │   ├── tree_importer.py        # Excel import functionality
    │   └── tree_importer_improved.py  # Enhanced importer (with logging)
    │
    └── katottg_tree/              # Module containing doctypes
        ├── __init__.py
        │
        ├── workspace/
        │   └── katottg_tree/
        │       └── katottg_tree.json  # Workspace configuration
        │
        └── doctype/               # DocTypes folder
            ├── __init__.py
            │
            ├── katottg/           # Main tree DocType
            │   ├── __init__.py
            │   ├── katottg.json
            │   ├── katottg.py
            │   ├── katottg.js
            │   ├── katottg_tree.js
            │   └── test_katottg.py
            │
            ├── katottg_settings/  # Settings DocType (Single)
            │   ├── __init__.py
            │   ├── katottg_settings.json
            │   ├── katottg_settings.py
            │   ├── katottg_settings.js
            │   └── test_katottg_settings.py
            │
            ├── katottg_import_settings/  # Import interface DocType (Single)
            │   ├── __init__.py
            │   ├── katottg_import_settings.json
            │   ├── katottg_import_settings.py
            │   ├── katottg_import_settings.js
            │   └── test_katottg_import_settings.py
            │
            ├── katottg_type/      # Type reference DocType
            │   ├── __init__.py
            │   ├── katottg_type.json
            │   ├── katottg_type.py
            │   ├── katottg_type.js
            │   └── test_katottg_type.py
            │
            └── katottg_test_control/  # Test DocType for custom control
                ├── __init__.py
                ├── katottg_test_control.json
                ├── katottg_test_control.py
                ├── katottg_test_control.js
                └── test_katottg_test_control.py
```

---

## Development Environment

### Installation

```bash
# Navigate to your bench directory
cd $PATH_TO_YOUR_BENCH

# Get the app
bench get-app https://github.com/rareMaxim/katottg_tree --branch develop

# Install in site
bench --site your-site install-app katottg_tree
```

### Pre-commit Setup

**IMPORTANT:** This project uses pre-commit hooks. Set them up before making changes:

```bash
cd apps/katottg_tree
pre-commit install
```

### Pre-commit Hooks

The following checks run on every commit:

1. **pre-commit-hooks:**
   - Trailing whitespace removal
   - Merge conflict detection
   - AST validation (Python)
   - JSON/TOML/YAML validation
   - Debug statement detection

2. **Ruff (Python):**
   - Import sorting (`--select=I`)
   - Linting (comprehensive rules)
   - Formatting

3. **Prettier (JavaScript/Vue/SCSS):**
   - Code formatting

4. **ESLint (JavaScript):**
   - Linting with `--quiet` flag

### Development Commands

```bash
# Run pre-commit manually on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run prettier --all-files

# Skip hooks (not recommended)
git commit --no-verify

# Run tests
bench --site your-site run-tests --app katottg_tree

# Start bench
bench start

# Build assets
bench build --app katottg_tree
```

---

## Code Conventions

### Python Style

#### Formatting

- **Line Length:** 110 characters (configured in `pyproject.toml`)
- **Indentation:** Tabs (not spaces)
- **Quotes:** Double quotes (`"`)
- **Import Sorting:** Automatic via Ruff
- **Formatter:** Ruff (replaces Black)

#### Naming Conventions

```python
# Variables and functions: snake_case
def get_katottg_full_path(name):
    full_path = ""
    return full_path

# Classes: PascalCase (Frappe convention)
class KATOTTG(NestedSet):
    pass

# Constants: UPPER_CASE
DEFAULT_CACHE_TTL = 3600

# Private methods/variables: _leading_underscore
def _fuzzy_search(query, filters):
    pass
```

#### Type Annotations

**IMPORTANT:** This app has `export_python_type_annotations = True` in hooks.py

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frappe.types import DF

class KATOTTG(NestedSet):
    # Type hints are auto-generated in controller classes
    title: DF.Data
    code: DF.Data | None
    category: DF.Data | None
```

#### Whitelisted Methods

```python
import frappe

@frappe.whitelist()
def search_katottg(query, filters=None, limit=50):
    """
    Always add @frappe.whitelist() for methods callable from frontend.
    Document parameters and return types.
    """
    pass
```

#### Error Handling

```python
# Use frappe.throw for user-facing errors
if not code:
    frappe.throw(_("Код КАТОТТГ є обов'язковим"))

# Use frappe.log_error for internal errors
try:
    # risky operation
    pass
except Exception as e:
    frappe.log_error(message=str(e), title="KATOTTG Import Error")
    frappe.throw(_("Помилка при імпорті даних"))
```

#### Ukrainian Language Support

```python
# Allowed Cyrillic confusables are configured in pyproject.toml
# Use Ukrainian for user-facing messages
frappe.msgprint(_("Дані успішно імпортовані"))

# Use translation function _() for all user messages
frappe.throw(_("Категорія '{0}' не дозволена").format(category))
```

### JavaScript Style

#### Formatting

- **Indentation:** Tabs
- **Quotes:** Preference varies (Prettier handles)
- **Semicolons:** Required by Frappe convention
- **ES Version:** ES2022

#### Naming Conventions

```javascript
// Variables and functions: camelCase
let fullPath = "";
function getKatottgPath() {}

// Constants: UPPER_CASE
const MAX_RESULTS = 50;

// Frappe globals (defined in .eslintrc)
frappe, __, cur_frm, cur_dialog, cur_list, frappe.ui.form.ControlLink
```

#### Frappe Patterns

```javascript
// Form scripts
frappe.ui.form.on("KATOTTG", {
	refresh: function(frm) {
		// Use frm, not cur_frm in form scripts
	}
});

// API calls
frappe.call({
	method: "katottg_tree.utils.api.search_katottg",
	args: {
		query: "search term",
		limit: 20
	},
	callback: function(r) {
		if (r.message) {
			// Handle response
		}
	}
});

// Extending controls
frappe.ui.form.ControlLink = class KATOTTGLinkControl extends frappe.ui.form.ControlLink {
	// Custom implementation
};
```

### Editor Configuration

The `.editorconfig` file enforces:

```ini
[*]
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
charset = utf-8

[{*.py,*.js,*.vue,*.css,*.scss,*.html}]
indent_style = tab
indent_size = 4
max_line_length = 99

[{*.json}]
insert_final_newline = false
indent_style = space
indent_size = 1
```

---

## Key Components

### 1. KATOTTG DocType (Main Tree)

**File:** `katottg_tree/katottg_tree/doctype/katottg/katottg.py`

#### Purpose
Core DocType for territorial classification tree structure using Nested Set Model.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | Data | Name in Ukrainian (e.g., "Запоріжжя") |
| `code` | Data, Unique | KATOTTG code (UA + 17 digits) |
| `category` | Data | Type code (O, K, P, H, M, X, C, B) |
| `parent_katottg` | Link | Parent node reference |
| `is_group` | Check | Whether node has children |
| `lft`, `rgt` | Int | Nested set tree values |

#### Categories

```python
ALLOWED_CATEGORIES = {
    "O": "Oblast (Область)",           # Region
    "K": "City with special status",   # Kyiv, Sevastopol
    "P": "Raion (Район)",              # District
    "H": "Hromada (Громада)",          # Territorial community
    "M": "Misto (Місто)",              # City
    "X": "Urban settlement",           # Смт
    "C": "Village (Село)",
    "B": "City district (Район міста)"
}
```

#### Key Methods

```python
class KATOTTG(NestedSet):
    def validate(self):
        """Validates code format, category, and hierarchy"""
        self.validate_code()
        self.validate_category()
        self.validate_hierarchy()

    def validate_code(self):
        """Ensures code is 'UA' + 17 digits"""
        if not re.match(r'^UA\d{17}$', self.code):
            frappe.throw(_("Invalid KATOTTG code format"))

    def on_update(self):
        """Clears cache on update"""
        clear_katottg_cache(self.name)

    @frappe.whitelist()
    def process_all_nodes(self):
        """Rebuilds tree structure (recalculates lft/rgt)"""
        rebuild_tree("KATOTTG", "parent_katottg")

    @frappe.whitelist()
    def get_katottg_children(parent):
        """Returns children for tree view lazy loading"""
        # Used by Frappe's tree view
```

#### Tree Structure

Uses **Nested Set Model** for efficient hierarchy queries:
- `lft` (left value) and `rgt` (right value) define node boundaries
- All descendants have `lft` between parent's `lft` and `rgt`
- Enables fast "get all descendants" queries

```sql
-- Get all descendants
SELECT * FROM `tabKATOTTG`
WHERE lft > parent_lft AND rgt < parent_rgt
```

---

### 2. KATOTTG Settings DocType

**File:** `katottg_tree/katottg_tree/doctype/katottg_settings/katottg_settings.py`

#### Purpose
Single DocType for application-wide configuration.

#### Configuration Sections

**1. Default Settings**
```python
default_katottg: DF.Link  # Default KATOTTG value
enable_caching: DF.Check  # Toggle caching
cache_ttl: DF.Int         # Cache lifetime (seconds, default: 3600)
```

**2. Import Settings**
```python
excel_column_mapping: DF.JSON        # Excel column mapping
import_batch_size: DF.Int            # Batch size (default: 500)
enable_import_validation: DF.Check   # Validation toggle
```

**3. Search Settings**
```python
enable_fuzzy_search: DF.Check  # Enable fuzzy search
search_results_limit: DF.Int   # Max results (default: 50)
```

#### Key Methods

```python
@frappe.whitelist()
def get_settings():
    """Returns cached settings object"""
    cache_key = "katottg_settings"
    settings = frappe.cache().get_value(cache_key)
    if not settings:
        settings = frappe.get_single("KATOTTG Settings")
        frappe.cache().set_value(cache_key, settings, expires_in_sec=300)
    return settings

@frappe.whitelist()
def clear_katottg_cache():
    """Clears all KATOTTG-related caches"""
    frappe.cache().delete_key("katottg_settings")
    # Clear all katottg_* keys
```

---

### 3. KATOTTG Import Settings DocType

**File:** `katottg_tree/katottg_tree/doctype/katottg_import_settings/katottg_import_settings.py`

#### Purpose
Interface for bulk Excel import with progress tracking.

#### Import Process

```python
@frappe.whitelist()
def import_data(self):
    """Enqueues background job for Excel import"""
    job = frappe.enqueue(
        import_from_excel,
        queue='long',
        timeout=3600,
        file_path=self.data_file,
        settings=self
    )
    return job.id

def import_from_excel(file_path, settings):
    """Background job that imports Excel data"""
    # 1. Read Excel file
    # 2. Skip first 4 rows (headers)
    # 3. Batch insert (default 500 rows)
    # 4. Update progress in cache
    # 5. Update is_group flags
    # 6. Clear caches
```

#### Progress Tracking

```javascript
// Frontend polls for progress
frappe.call({
    method: "frappe.utils.background_jobs.get_info",
    args: { job_id: job_id },
    callback: function(r) {
        // Update progress bar
    }
});
```

---

### 4. Import Implementations

#### Standard Importer
**File:** `katottg_tree/utils/tree_importer.py`

```python
def import_data_from_excel(file_path, batch_size=500):
    """
    Standard importer:
    1. Deletes all existing KATOTTG records
    2. Reads Excel (openpyxl)
    3. Batch inserts
    4. Updates is_group flags
    5. Rebuilds tree
    """
```

#### Improved Importer
**File:** `katottg_tree/utils/tree_importer_improved.py`

```python
def import_katottg_data(file_path, settings):
    """
    Enhanced importer with:
    - Detailed logging
    - Error collection (first 100)
    - Import statistics
    - Duration tracking
    - Better error messages
    """
```

---

## API Reference

All API endpoints are in `katottg_tree/utils/api.py`

### Search API

#### `search_katottg(query, filters=None, limit=50)`

**Purpose:** Main search endpoint with optional fuzzy search

**Parameters:**
- `query` (str): Search term
- `filters` (dict, optional): Additional filters (e.g., `{"category": "M"}`)
- `limit` (int, optional): Max results (default: 50, from settings)

**Returns:** List of KATOTTG objects with `full_path` added

**Example:**
```python
# Python
from katottg_tree.utils.api import search_katottg
results = search_katottg("Запоріж", filters={"category": "M"}, limit=10)

# JavaScript
frappe.call({
    method: "katottg_tree.utils.api.search_katottg",
    args: { query: "Запоріж", limit: 10 },
    callback: (r) => console.log(r.message)
});
```

**Behavior:**
- If `enable_fuzzy_search` is ON: Uses 4-level fuzzy search with relevance scoring
- If `enable_fuzzy_search` is OFF: Simple `LIKE %query%` search
- Always adds `full_path` to results
- Respects `search_results_limit` from settings

---

### Hierarchy APIs

#### `get_katottg_hierarchy(name)`

**Purpose:** Get ancestor codes for a node

**Parameters:**
- `name` (str): KATOTTG code

**Returns:** List of ancestor codes (bottom to top)

**Example:**
```python
hierarchy = get_katottg_hierarchy("UA23080070010092407")
# ["UA23080070010092407", "UA23080070010000000", "UA23080070000000000", ...]
```

**Caching:** Key = `katottg_hierarchy_{name}`, TTL from settings

---

#### `get_katottg_full_path(name)`

**Purpose:** Get formatted hierarchical path string

**Parameters:**
- `name` (str): KATOTTG code

**Returns:** Formatted path string

**Example:**
```python
path = get_katottg_full_path("UA23080070010092407")
# "Запорізька область, Мелітопольський район, Мелітопольська ТГ, м. Мелітополь"
```

**Formatting Rules:**
```python
{
    "O": "{title}",                    # Запорізька область
    "P": "{title}",                    # Запорізький район
    "H": "{title}",                    # Запорізька ТГ
    "M": "м. {title}",                 # м. Запоріжжя
    "X": "смт {title}",                # смт Веселе
    "C": "с. {title}",                 # с. Іванівка
    "B": "р-н {title}",                # р-н Хортицький
    "K": "{title}",                    # Київ
}
```

**Caching:** Key = `katottg_full_path_{name}`, TTL from settings

---

#### `get_default_katottg_hierarchy()`

**Purpose:** Get hierarchy for default KATOTTG from settings

**Returns:** List of ancestor codes for default value

**Example:**
```python
default_hierarchy = get_default_katottg_hierarchy()
```

**Caching:** Key = `katottg_default_hierarchy_{name}`

---

### Filter API

#### `get_katottg_by_category(category, parent=None, limit=100)`

**Purpose:** Filter KATOTTG by category and optional parent

**Parameters:**
- `category` (str): Category code (O, K, P, H, M, X, C, B)
- `parent` (str, optional): Parent KATOTTG code
- `limit` (int, optional): Max results (default: 100)

**Returns:** List of KATOTTG objects

**Example:**
```python
# Get all oblasts
oblasts = get_katottg_by_category("O")

# Get all cities in specific raion
cities = get_katottg_by_category("M", parent="UA23080070000000000")
```

---

### Fuzzy Search Algorithm

#### `_fuzzy_search(query, base_filters, limit)`

**Purpose:** 4-level intelligent search with relevance scoring

**Algorithm:**

```python
# Level 1: Exact match (relevance: 100%)
WHERE code = '{query}' OR title = '{query}'

# Level 2: Starts with (relevance: 80%)
WHERE code LIKE '{query}%' OR title LIKE '{query}%'

# Level 3: Contains (relevance: 60%)
WHERE code LIKE '%{query}%' OR title LIKE '%{query}%'

# Level 4: Word search (relevance: 40-60%)
# Split query into words, search for each
WHERE title LIKE '%{word}%'
# relevance = 40 + (matched_words_count * 5)
```

**Features:**
- Case-insensitive
- Removes duplicates (keeps highest relevance)
- Sorts by relevance DESC
- Adds `full_path` to each result

**Performance:**
- Sequential queries (not parallel)
- Stops at limit
- Uses indexes on `code` field

---

## Frontend Components

### 1. Custom Link Control

**File:** `katottg_tree/public/js/katottg_link_control.js`

**Purpose:** Replace standard Link field with hierarchical selector for KATOTTG

**Globally Loaded:** Yes (via `app_include_js` in hooks.py)

#### Implementation

```javascript
frappe.ui.form.ControlLink = class KATOTTGLinkControl extends frappe.ui.form.ControlLink {
    make_input() {
        // Override only for KATOTTG links
        if (this.df.options === "KATOTTG") {
            this.make_katottg_selector();
        } else {
            super.make_input();
        }
    }

    make_katottg_selector() {
        // Create custom HTML wrapper
        // Add "Обрати" button
        // Show formatted value (full_path)
    }

    show_selection_dialog() {
        // Create dialog with 5 hierarchical levels:
        // - Oblast (Область)
        // - Raion (Район)
        // - Hromada (Громада)
        // - Settlement (Населений пункт)
        // - City District (Район міста)
        //
        // Each level cascades to next
        // Uses get_query filters
    }
};
```

#### Features

- **Cascading Dropdowns:** Each level filters the next
- **Auto-load Current Value:** Fetches hierarchy on form load
- **Formatted Display:** Shows full path instead of code
- **Fallback to Default:** Uses default from settings if no value
- **Smart Filtering:** Uses `get_query` with category and parent filters

#### Usage

Any Link field pointing to KATOTTG automatically uses this control:

```json
{
    "fieldname": "katottg",
    "fieldtype": "Link",
    "options": "KATOTTG"
}
```

---

### 2. Import Settings UI

**File:** `katottg_tree/katottg_tree/doctype/katottg_import_settings/katottg_import_settings.js`

#### Features

```javascript
frappe.ui.form.on("KATOTTG Import Settings", {
    refresh: function(frm) {
        // Add custom import button
        frm.add_custom_button(__("Імпортувати"), () => {
            // Start import
            // Show progress bar
            // Poll job status every 2s
        });
    }
});
```

**Progress Tracking:**
```javascript
function poll_job_status(job_id) {
    setInterval(() => {
        frappe.call({
            method: "frappe.utils.background_jobs.get_info",
            args: { job_id: job_id },
            callback: (r) => {
                // Update progress bar
                if (r.message.status === "finished") {
                    frappe.msgprint(__("Імпорт завершено"));
                }
            }
        });
    }, 2000);  // Poll every 2 seconds
}
```

---

### 3. Tree View Customization

**File:** `katottg_tree/katottg_tree/doctype/katottg/katottg_tree.js`

```javascript
frappe.treeview_settings["KATOTTG"] = {
    get_tree_nodes: "katottg_tree.katottg_tree.doctype.katottg.katottg.get_katottg_children",
    add_tree_node: "katottg_tree.katottg_tree.doctype.katottg.katottg.add_node",
    toolbar: [
        {
            label: __("Обробити всі вузли"),
            click: function() {
                frappe.call({
                    method: "katottg_tree.katottg_tree.doctype.katottg.katottg.process_all_nodes",
                    callback: function() {
                        frappe.msgprint(__("Tree rebuilt"));
                    }
                });
            }
        }
    ]
};
```

---

## Database Schema

### KATOTTG Table (`tabKATOTTG`)

```sql
CREATE TABLE `tabKATOTTG` (
    `name` VARCHAR(140) PRIMARY KEY,           -- KATOTTG code (e.g., UA23080070010092407)
    `code` VARCHAR(140) UNIQUE NOT NULL,       -- Same as name
    `title` VARCHAR(140) NOT NULL,             -- Ukrainian name
    `category` VARCHAR(1),                     -- O, K, P, H, M, X, C, B
    `parent_katottg` VARCHAR(140),             -- Foreign key to self
    `is_group` TINYINT(1) DEFAULT 0,          -- Has children?
    `lft` INT,                                 -- Nested set left
    `rgt` INT,                                 -- Nested set right
    `old_parent` VARCHAR(140),                -- For tree rebuild
    -- Standard Frappe fields
    `creation` DATETIME(6),
    `modified` DATETIME(6),
    `modified_by` VARCHAR(140),
    `owner` VARCHAR(140),
    `docstatus` INT DEFAULT 0,
    `idx` INT DEFAULT 0,
    -- Indexes
    INDEX `parent_katottg_index` (`parent_katottg`),
    INDEX `lft_rgt_index` (`lft`, `rgt`),
    UNIQUE INDEX `code` (`code`)
);
```

### Key Indexes

1. **`code` UNIQUE:** Fast lookup by KATOTTG code
2. **`lft`, `rgt`:** Efficient nested set queries
3. **`parent_katottg`:** Quick parent-child queries

### Nested Set Model

```
Example Tree:
Запорізька область (lft=1, rgt=10)
├── Запорізький район (lft=2, rgt=9)
│   ├── Запорізька ТГ (lft=3, rgt=8)
│   │   ├── м. Запоріжжя (lft=4, rgt=5)
│   │   └── с. Іванівка (lft=6, rgt=7)

Query all descendants of Запорізька область:
SELECT * FROM tabKATOTTG WHERE lft > 1 AND rgt < 10;
```

---

## Testing

### Test Files

Each DocType has a corresponding test file:

```
katottg_tree/katottg_tree/doctype/
├── katottg/test_katottg.py
├── katottg_settings/test_katottg_settings.py
├── katottg_import_settings/test_katottg_import_settings.py
├── katottg_type/test_katottg_type.py
└── katottg_test_control/test_katottg_test_control.py
```

### Running Tests

```bash
# All tests for this app
bench --site your-site run-tests --app katottg_tree

# Specific DocType tests
bench --site your-site run-tests --doctype "KATOTTG"

# Specific test file
bench --site your-site run-tests --module katottg_tree.katottg_tree.doctype.katottg.test_katottg
```

### Standalone Test Script

**File:** `test_fuzzy_search.py`

**Purpose:** Test fuzzy search functionality independently

```bash
# Run fuzzy search tests
bench --site your-site execute katottg_tree.test_fuzzy_search.run_all_tests
```

**Test Cases:**
1. Exact city name search
2. Partial name (beginning)
3. Partial name (missing last letter)
4. Search by part and word
5. Search by object type (category)
6. Comparative test (fuzzy ON vs OFF)

**Output:**
- Displays relevance scores
- Shows full paths
- Compares result counts
- Saves statistics

---

## Common Tasks

### Adding a New Field to KATOTTG

1. **Update JSON:**
   ```bash
   # Edit the JSON file
   vim katottg_tree/katottg_tree/doctype/katottg/katottg.json
   ```

2. **Add field definition:**
   ```json
   {
       "fieldname": "new_field",
       "fieldtype": "Data",
       "label": "Нове поле"
   }
   ```

3. **Update controller (if needed):**
   ```python
   # katottg.py
   class KATOTTG(NestedSet):
       new_field: DF.Data  # Type hint auto-generated
   ```

4. **Run bench migrate:**
   ```bash
   bench --site your-site migrate
   ```

---

### Clearing Cache

**From Code:**
```python
import frappe

# Clear specific cache
frappe.cache().delete_key(f"katottg_hierarchy_{name}")
frappe.cache().delete_key(f"katottg_full_path_{name}")

# Clear all KATOTTG caches
from katottg_tree.katottg_tree.doctype.katottg_settings.katottg_settings import clear_katottg_cache
clear_katottg_cache()
```

**From UI:**
1. Go to KATOTTG Settings
2. Click "Clear Cache" button
3. Confirm

**From Console:**
```bash
bench --site your-site console
>>> frappe.cache().delete_key("katottg_settings")
```

---

### Rebuilding Tree

**From UI:**
1. Open KATOTTG Tree view
2. Click "Обробити всі вузли" button
3. Wait for completion

**From Code:**
```python
from frappe.utils.nestedset import rebuild_tree
rebuild_tree("KATOTTG", "parent_katottg")
```

**From Console:**
```bash
bench --site your-site console
>>> from frappe.utils.nestedset import rebuild_tree
>>> rebuild_tree("KATOTTG", "parent_katottg")
```

---

### Importing Data from Excel

**Required Excel Format:**
- Column A: Code (UA + 17 digits)
- Column B: Title (Ukrainian name)
- Column C: Category (O, K, P, H, M, X, C, B)
- Column D: Parent Code (UA + 17 digits, optional)
- First 4 rows are skipped (headers)

**Steps:**
1. Go to KATOTTG Import Settings
2. Attach Excel file
3. Click "Імпортувати" button
4. Monitor progress bar
5. Wait for completion message

**Batch Size:**
Configure in KATOTTG Settings → `import_batch_size` (default: 500)

---

### Enabling/Disabling Fuzzy Search

**From UI:**
1. Go to KATOTTG Settings
2. Check/uncheck "Enable Fuzzy Search"
3. Save

**From Code:**
```python
settings = frappe.get_single("KATOTTG Settings")
settings.enable_fuzzy_search = 1  # or 0
settings.save()
```

**Performance Note:**
- Fuzzy search is slower but more intelligent
- For large datasets (100k+ records), consider disabling
- Adjust `search_results_limit` to optimize

---

### Adding a New API Endpoint

1. **Add to `utils/api.py`:**
   ```python
   @frappe.whitelist()
   def my_new_endpoint(param1, param2):
       """
       Description of endpoint.

       Args:
           param1 (str): Description
           param2 (int): Description

       Returns:
           dict: Description of return value
       """
       # Implementation
       return {"result": "value"}
   ```

2. **Call from JavaScript:**
   ```javascript
   frappe.call({
       method: "katottg_tree.utils.api.my_new_endpoint",
       args: {
           param1: "value",
           param2: 123
       },
       callback: function(r) {
           console.log(r.message);
       }
   });
   ```

---

## AI Assistant Guidelines

### General Principles

1. **Read Before Modifying:** Always read files before making changes
2. **Follow Conventions:** Adhere to Python and JavaScript conventions above
3. **Use Pre-commit:** Run pre-commit checks before committing
4. **Test Changes:** Run relevant tests after modifications
5. **Document Code:** Add docstrings and comments in Ukrainian
6. **Handle Errors:** Use proper error handling with user-friendly messages
7. **Cache Wisely:** Clear caches after data modifications
8. **Respect Tree Integrity:** Always validate hierarchy changes

---

### Common Pitfalls to Avoid

#### ❌ Don't: Modify tree structure without rebuilding

```python
# BAD: Changing parent without rebuilding tree
katottg.parent_katottg = new_parent
katottg.save()
```

```python
# GOOD: Rebuild tree after changes
from frappe.utils.nestedset import rebuild_tree
katottg.parent_katottg = new_parent
katottg.save()
rebuild_tree("KATOTTG", "parent_katottg")
```

---

#### ❌ Don't: Forget to clear cache after updates

```python
# BAD: Update without clearing cache
def update_katottg(name, new_title):
    doc = frappe.get_doc("KATOTTG", name)
    doc.title = new_title
    doc.save()
```

```python
# GOOD: Clear cache after update
def update_katottg(name, new_title):
    doc = frappe.get_doc("KATOTTG", name)
    doc.title = new_title
    doc.save()
    frappe.cache().delete_key(f"katottg_full_path_{name}")
    frappe.cache().delete_key(f"katottg_hierarchy_{name}")
```

---

#### ❌ Don't: Use spaces for indentation

```python
# BAD: Spaces
def my_function():
    return True
```

```python
# GOOD: Tabs
def my_function():
	return True
```

---

#### ❌ Don't: Hardcode limits and settings

```python
# BAD: Hardcoded limit
results = frappe.get_all("KATOTTG", limit=50)
```

```python
# GOOD: Use settings
from katottg_tree.katottg_tree.doctype.katottg_settings.katottg_settings import get_settings
settings = get_settings()
results = frappe.get_all("KATOTTG", limit=settings.search_results_limit)
```

---

#### ❌ Don't: Skip validation

```python
# BAD: No validation
def create_katottg(code, title, category):
    doc = frappe.new_doc("KATOTTG")
    doc.code = code
    doc.title = title
    doc.category = category
    doc.insert()
```

```python
# GOOD: Validate inputs
def create_katottg(code, title, category):
    if not re.match(r'^UA\d{17}$', code):
        frappe.throw(_("Невірний формат коду KATOTTG"))

    if category not in ["O", "K", "P", "H", "M", "X", "C", "B"]:
        frappe.throw(_("Невірна категорія"))

    doc = frappe.new_doc("KATOTTG")
    doc.code = code
    doc.title = title
    doc.category = category
    doc.insert()
```

---

### Best Practices

#### ✅ Use Frappe's built-in functions

```python
# Get single DocType
settings = frappe.get_single("KATOTTG Settings")

# Get list with filters
results = frappe.get_all("KATOTTG",
    filters={"category": "M"},
    fields=["name", "title", "code"],
    limit=100
)

# Get full document
doc = frappe.get_doc("KATOTTG", "UA23080070010092407")
```

---

#### ✅ Use translation function

```python
# All user-facing messages should use _()
frappe.msgprint(_("Операція виконана успішно"))
frappe.throw(_("Помилка: {0}").format(error_message))

# Field labels in JSON
{
    "label": "Код КАТОТТГ",  // Will be translated if translation exists
    "fieldtype": "Data"
}
```

---

#### ✅ Use background jobs for long operations

```python
# For operations > 5 seconds
frappe.enqueue(
    method=long_running_function,
    queue='long',
    timeout=3600,
    **kwargs
)
```

---

#### ✅ Use proper logging

```python
import frappe

# Info level
frappe.log("Import started")

# Error level with traceback
try:
    # risky operation
except Exception as e:
    frappe.log_error(
        message=frappe.get_traceback(),
        title="KATOTTG Import Error"
    )
```

---

### Code Review Checklist

Before submitting changes, verify:

- [ ] Pre-commit hooks pass (`pre-commit run --all-files`)
- [ ] Code follows style conventions (tabs, double quotes, line length)
- [ ] All user messages use `_()` translation function
- [ ] Error handling is present and user-friendly
- [ ] Caches are cleared after data modifications
- [ ] Tree integrity is maintained (rebuild if needed)
- [ ] Type hints are added for new methods/classes
- [ ] Docstrings are present and in Ukrainian
- [ ] Tests are updated/added for new functionality
- [ ] No debug statements (`console.log`, `print()`) remain
- [ ] No sensitive data is logged or exposed
- [ ] Performance impact is considered (indexes, caching)

---

### Git Workflow

#### Branch Naming

All development branches must start with `claude/` and end with the session ID:

```bash
# CORRECT
claude/claude-md-mitervbbtjnhau4u-016TAWvfwwHJrnn2ohMjVKtp

# INCORRECT (will fail with 403)
feature/new-feature
main
master
```

#### Commit Messages

```bash
# Good commit messages
feat: Add fuzzy search functionality
fix: Resolve cache invalidation issue
docs: Update CLAUDE.md with API examples
refactor: Improve tree importer performance

# Bad commit messages
"updates"
"fix"
"changes"
```

#### Push with Retry Logic

```bash
# First attempt
git push -u origin claude/your-branch-name

# If network failure, retry with exponential backoff:
# Wait 2s, retry
# Wait 4s, retry
# Wait 8s, retry
# Wait 16s, retry (max 4 retries)
```

---

### Testing Strategy

#### Unit Tests

Test individual functions in isolation:

```python
# test_katottg.py
def test_validate_code(self):
    doc = frappe.new_doc("KATOTTG")
    doc.code = "UA12345678901234567"
    doc.title = "Test"
    doc.category = "M"
    self.assertRaises(ValidationError, doc.insert)
```

#### Integration Tests

Test API endpoints and workflows:

```python
def test_search_katottg(self):
    results = search_katottg("Запоріжжя", limit=10)
    self.assertTrue(len(results) <= 10)
    self.assertTrue(all("full_path" in r for r in results))
```

#### Manual Testing

1. Test in UI after changes
2. Verify caching behavior
3. Check performance with realistic data
4. Test edge cases (empty strings, special characters)

---

### Performance Considerations

#### Database Queries

```python
# BAD: N+1 query problem
for katottg in frappe.get_all("KATOTTG"):
    doc = frappe.get_doc("KATOTTG", katottg.name)
    print(doc.title)

# GOOD: Batch query
katottgs = frappe.get_all("KATOTTG", fields=["name", "title"])
for katottg in katottgs:
    print(katottg.title)
```

#### Caching

```python
# Cache expensive operations
@frappe.whitelist()
def get_full_path(name):
    cache_key = f"katottg_full_path_{name}"
    cached = frappe.cache().get_value(cache_key)
    if cached:
        return cached

    # Expensive operation
    result = build_full_path(name)

    # Cache with TTL
    settings = get_settings()
    frappe.cache().set_value(cache_key, result, expires_in_sec=settings.cache_ttl)
    return result
```

#### Bulk Operations

```python
# BAD: Insert one by one
for row in data:
    doc = frappe.new_doc("KATOTTG")
    doc.update(row)
    doc.insert()

# GOOD: Bulk insert
frappe.db.bulk_insert("KATOTTG", fields=["code", "title", "category"], values=data)
```

---

## Appendix: Quick Reference

### Useful Commands

```bash
# Development
bench start                                  # Start development server
bench build --app katottg_tree              # Build assets
bench --site site1.local migrate            # Run migrations
bench --site site1.local console            # Python console
bench --site site1.local clear-cache        # Clear all caches

# Testing
bench --site site1.local run-tests --app katottg_tree
pre-commit run --all-files

# Git
git status
git add .
git commit -m "feat: Add new feature"
git push -u origin claude/your-branch-name
```

### Important File Paths

```
Configuration:
- pyproject.toml                    # Python config, Ruff settings
- .pre-commit-config.yaml           # Pre-commit hooks
- .editorconfig                     # Editor settings
- .eslintrc                         # ESLint config

Main Code:
- katottg_tree/hooks.py             # App hooks
- katottg_tree/utils/api.py         # API endpoints
- katottg_tree/utils/tree_importer.py  # Import logic

DocTypes:
- katottg_tree/katottg_tree/doctype/katottg/
- katottg_tree/katottg_tree/doctype/katottg_settings/
- katottg_tree/katottg_tree/doctype/katottg_import_settings/

Frontend:
- katottg_tree/public/js/katottg_link_control.js

Documentation:
- README.md                         # Installation
- FUZZY_SEARCH.md                   # Fuzzy search guide (Ukrainian)
- CLAUDE.md                         # This file
```

### Cache Keys

```python
"katottg_settings"                           # Settings cache
"katottg_hierarchy_{name}"                   # Hierarchy array
"katottg_full_path_{name}"                   # Formatted path
"katottg_default_hierarchy_{name}"           # Default hierarchy
```

### API Endpoints Summary

```
search_katottg(query, filters, limit)        # Main search
get_katottg_hierarchy(name)                  # Get ancestors
get_katottg_full_path(name)                  # Get formatted path
get_default_katottg_hierarchy()              # Default hierarchy
get_katottg_by_category(category, parent, limit)  # Filter by category
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.0.1 | 2025-12-05 | Initial CLAUDE.md creation |

---

## Contact & Support

**Author:** Maxim S
**Email:** maks4a@gmail.com
**License:** MIT

For issues and questions, refer to the repository's issue tracker or contact the maintainer.

---

*This document is maintained as the authoritative guide for AI assistants working with the KATOTTG Tree codebase. Keep it updated as the codebase evolves.*
