import sys
from ics import Calendar


def filter(keywords: list[str]):
    """Reads from stdin and writes to stdout"""

    # Input should be the stdin
    input_calendar = Calendar(sys.stdin.read())
    output_calendar = Calendar()

    # Filter
    output_calendar.events = {
        e for e in input_calendar.events if any(i in e.name for i in keywords)
    }

    # Output should be the stdout
    sys.stdout.writelines(output_calendar.serialize_iter())


def concat(files: list[str]):
    """Reads from files and writes to stdout"""

    output_calendar = Calendar()

    for file in files:
        with open(file, "r") as f:
            input_calendar = Calendar(f.read())
            output_calendar.events.update(input_calendar.events)

    # Output should be the stdout
    sys.stdout.writelines(output_calendar.serialize_iter())


def summary():
    """Reads from stdin and writes to stdout a human-readable summary, sorted from earliest to latest"""

    input_calendar = Calendar(sys.stdin.read())

    print("| Date       | Begin - End   | Name |")
    print("| ---------- | ------------- | ---- |")
    for event in input_calendar.events:
        day = event.begin.strftime("%Y-%m-%d")
        begin = event.begin.strftime("%H:%M")
        end = event.end.strftime("%H:%M")
        print(f"| {day} | {begin} - {end} | {event.name} |")


def usage():
    print("Usage: ical COMMAND [ARGS]")
    print("Commands:")
    print("  grep < input.ics > output.ics 'Pattern1|Pattern2'")
    print("  cat file1.ics file2.ics")
    print("  summary < input.ics")

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
        case _:
            usage()
            sys.exit(1)


if __name__ == "__main__":
    main()
