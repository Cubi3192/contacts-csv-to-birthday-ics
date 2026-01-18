# Create Birthday Events (ICS) from Outlook Contacts CSV

Convert Outlook contacts from CSV to ICS (iCalendar) by extracting birthdays and creating calendar events for them.

## Features

- Convert CSV contact data to iCalendar (.ics)
- Create yearly recurring birthday events
- Configurable birthday event summary (prefix/suffix)
- Simple command-line interface (CLI)
- Compatible with Google Calendar, Outlook, Apple Calendar, and other iCalendar-based apps

Requirements
- Python 3.9+ (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cubi3192/contacts-csv-to-ics.git
cd contacts-csv-to-ics
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
.\.venv\Scripts\activate.bat
```

**Bash/Linux/Mac:**
```bash
source .venv/bin/activate
```

4. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python main.py [-i <input_csv>] [-o <output_ics>] [-p <prefix>] [-s <suffix>]
```

### Parameters

- `-i, --input`: Input CSV file path  (optional)
- `-o, --output`: Output ICS file path  (optional)
- `-p, --prefix`: Prefix added to the event summary. (optional)
- `-s, --suffix`: Suffix added to the event summary. (optional)

### Example

```bash
python main.py -i Contacts.csv -o birthdays.ics -p "Today is " -s "’s birthday"
```
This produce summaries such as:
- `Today is John Doe’s birthday`

## CSV Format

The input CSV file should contain the following columns:
- `First Name`: First name
- `Last Name`: Last name
- `Birthday`: Birthday date (YYYY-MM-DD or MM/DD/YYYY or DD.MM.YYYY or DD/MM/YYYY format)
## Output

The script generates an ICS calendar file with birthday events that can be imported into:
- Google Calendar
- Outlook
- Apple Calendar
- Any calendar application supporting iCalendar format

## License

MIT License © 2026 André Lutz