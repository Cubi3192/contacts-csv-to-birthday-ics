import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path


def parse_outlook_birthday(date_str: str) -> datetime | None:
    """
    Outlook exportiert Geburtstage typischerweise als:
    - MM/DD/YYYY
    - YYYY-MM-DD
    """
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def create_ics_from_csv(
    input_csv: Path,
    output_ics: Path,
    summary_prefix: str = "Birthday:",
    summary_suffix: str = "",
) -> None:
    with open(output_ics, "w", encoding="utf-8") as ics:
        ics.write("BEGIN:VCALENDAR\n")
        ics.write("VERSION:2.0\n")
        ics.write("PRODID:-//Outlook Contacts Birthday Import//EN\n")
        with open(input_csv, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                birthday_raw = row.get("Birthday", "").strip()
                if not birthday_raw:
                    continue

                birthday = parse_outlook_birthday(birthday_raw)
                if not birthday:
                    continue

                first_name = row.get("First Name", "").strip()
                last_name = row.get("Last Name", "").strip()
                full_name = f"{first_name} {last_name}".strip()

                start_date = birthday.strftime("%Y%m%d")
                end_date = (birthday + timedelta(days=1)).strftime("%Y%m%d")

                uid = f"{start_date}-{first_name}{last_name}@outlook-import"

                ics.write("BEGIN:VEVENT\n")
                ics.write(f"UID:{uid}\n")
                ics.write(f"DTSTART;VALUE=DATE:{start_date}\n")
                ics.write(f"DTEND;VALUE=DATE:{end_date}\n")
                ics.write("RRULE:FREQ=YEARLY\n")
                ics.write(f"SUMMARY:{summary_prefix}{full_name}{summary_suffix}\n")
                ics.write("TRANSP:TRANSPARENT\n")
                ics.write("END:VEVENT\n")

        ics.write("END:VCALENDAR\n")

        print("ICS file successfully created:", output_ics)


if __name__ == "__main__":
    DEFAULT_INPUT_CSV = "Contacts.csv"
    DEFAULT_OUTPUT_ICS = "birthdays.ics"

    parser = argparse.ArgumentParser(
        description="Convert Outlook contacts CSV birthdays to ICS format."
    )
    parser.add_argument(
        "-i", "--input", type=str, default=DEFAULT_INPUT_CSV, help="Input CSV file path"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_ICS,
        help="Output ICS file path",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="Birthday:",
        help="Summary prefix  for birthday events",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        default="",
        help="Summary suffix for birthday events",
    )

    args = parser.parse_args()
    INPUT_CSV = args.input
    OUTPUT_ICS = args.output
    SUMMARY_PREFIX = args.prefix
    SUMMARY_SUFFIX = args.suffix

    script_dir = Path(__file__).resolve().parent
    cwd_dir = Path.cwd()

    input_csv_path: Path | None = None
    output_ics_path: Path | None = None

    if (script_dir / INPUT_CSV).exists():
        input_csv_path = script_dir / INPUT_CSV
        output_ics_path = script_dir / OUTPUT_ICS

    elif (cwd_dir / INPUT_CSV).exists():
        input_csv_path = cwd_dir / INPUT_CSV
        output_ics_path = cwd_dir / OUTPUT_ICS

    elif (script_dir / DEFAULT_INPUT_CSV).exists():
        input_csv_path = script_dir / DEFAULT_INPUT_CSV
        output_ics_path = script_dir / DEFAULT_OUTPUT_ICS

    elif (cwd_dir / DEFAULT_INPUT_CSV).exists():
        input_csv_path = cwd_dir / DEFAULT_INPUT_CSV
        output_ics_path = cwd_dir / DEFAULT_OUTPUT_ICS

    if (
        input_csv_path
        and input_csv_path.exists()
        and output_ics_path
        and output_ics_path.parent.exists()
    ):
        create_ics_from_csv(
            input_csv_path, output_ics_path, SUMMARY_PREFIX, SUMMARY_SUFFIX
        )
