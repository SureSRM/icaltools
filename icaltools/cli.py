import sys
import datetime
from ics import Calendar


def _sort_by_date(c: Calendar):
    c.events.sort(key=lambda e: e.timespan.begin_time or datetime.datetime.max)


def _input_calendar() -> Calendar:
    """Reads the calendar from stdin"""
    c = Calendar(sys.stdin.read())
    _sort_by_date(c)
    return c


def _output_calendar(c: Calendar):
    """Writes the calendar to stdout, sorted by date and time"""
    _sort_by_date(c)
    # sys.stdout.writelines(c.to_container().serialize_iter())
    sys.stdout.write(c.serialize())


def filter(keywords: list[str]):
    """Reads from stdin and writes to stdout"""

    # Input should be the stdin
    input_calendar = _input_calendar()
    output_calendar = Calendar()

    # Filter
    output_calendar.events = [
        e for e in input_calendar.events if any(i in e.summary for i in keywords)
    ]

    # Output should be the stdout
    _output_calendar(output_calendar)


def concat(files: list[str]):
    """Reads from files and writes to stdout"""

    output_calendar = Calendar()

    for file in files:
        with open(file, "r") as f:
            input_calendar = Calendar(f.read())
            output_calendar.events.extend(input_calendar.events)

    # Output should be the stdout
    _output_calendar(output_calendar)


def summary():
    """Reads from stdin and writes to stdout a human-readable summary, sorted from earliest to latest"""

    input_calendar = _input_calendar()

    print("| Date       | Begin - End   | Name |")
    print("| ---------- | ------------- | ---- |")
    for event in input_calendar.events:
        day = event.timespan.begin_time.strftime("%Y-%m-%d")
        begin = event.timespan.begin_time.strftime("%H:%M")
        end = event.timespan.end_time.strftime("%H:%M")
        print(f"| {day} | {begin} - {end} | {event.summary} |")


def count():
    """Reads from stdin and writes to stdout the number of events"""

    input_calendar = _input_calendar()
    print(len(input_calendar.events))


def names():
    """Reads from stdin and writes to stdout the names of the events"""

    input_calendar = _input_calendar()
    for event in input_calendar.events:
        print(event.summary)


def rename(fix, filename, prefix, suffix):
    """Reads a text file with same ammount of lines as events in the calendar and renames the events.
    It will also add a prefix and/or a suffix to the name of the events"""

    output_calendar = _input_calendar()

    if filename:
        with open(filename, "r") as f:
            names = f.readlines()

        if len(names) != len(output_calendar.events):
            print(
                f"The number of events in the calendar {len(output_calendar.events)} and the number of names {len(names)} in the file do not match",
                file=sys.stderr,
            )
            sys.exit(1)

        for event, name in zip(output_calendar.events, names):
            event.summary = name.strip()
    elif fix:
        for event in output_calendar.events:
            event.summary = fix

    if prefix:
        for event in output_calendar.events:
            event.summary = prefix + event.summary

    if suffix:
        for event in output_calendar.events:
            event.summary = event.summary + suffix

    # Output should be the stdout
    _output_calendar(output_calendar)


def usage():
    print("Usage: ical COMMAND [ARGS]", file=sys.stderr)
    print("Commands:", file=sys.stderr)
    print("  grep < input.ics > output.ics 'Pattern1|Pattern2'", file=sys.stderr)
    print("  cat file1.ics file2.ics", file=sys.stderr)
    print("  summary < input.ics", file=sys.stderr)


def main():
    """Main entry point for the CLI."""
    # TODO: Refactor to read from stdin and write to stdout
    # CLI app will be installed as `ical`
    # CLI usage for filter: ical grep < input.ics > output.ics "Pattern1|Pattern2"
    # Future implementations will include `ical cat file1.txt file2.txt` and it will merge the events

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    match sys.argv[1]:
        case "grep":
            if len(sys.argv) < 3:
                usage()
                sys.exit(1)

            filter(sys.argv[2].split("|"))
        case "cat":
            if len(sys.argv) < 3:
                usage()
                sys.exit(1)

            concat(sys.argv[2:])
        case "summary":
            if len(sys.argv) < 2:
                usage()
                sys.exit(1)
            summary()
        case "count":
            if len(sys.argv) < 2:
                usage()
                sys.exit(1)
            count()
        case "names":
            if len(sys.argv) < 2:
                usage()
                sys.exit(1)
            names()
        case "rename":
            if len(sys.argv) < 3:
                usage()
                sys.exit(1)
            # parse command can have 4 flags: fix, file, prefix, suffix
            # icaltools rename --fix "Class"
            # icaltools rename --file names.txt
            # icaltools rename --prefix "Prefix"
            # icaltools rename --suffix "Suffix"
            fix = None
            file = None
            prefix = None
            suffix = None
            for i in range(2, len(sys.argv), 2):
                match sys.argv[i]:
                    case "--fix":
                        fix = sys.argv[i + 1]
                    case "--file":
                        file = sys.argv[i + 1]
                    case "--prefix":
                        prefix = sys.argv[i + 1]
                    case "--suffix":
                        suffix = sys.argv[i + 1]
                    case _:
                        usage()
                        sys.exit(1)
            rename(fix, file, prefix, suffix)
        case _:
            usage()
            sys.exit(1)


if __name__ == "__main__":
    main()
