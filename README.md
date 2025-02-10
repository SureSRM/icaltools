## iCAL Processor

This is a utility tool to process iCAL files in a POSIX style.
It allows to:

- Filter (grep) events by a pattern from `stdin` to `stdout`
- Concatenate (cat) multiple iCAL files to `stdout`
- Summarize the events in a file as a markdown table from `stdin` to `stdout`

## Install

**Recomended:** Using [uv](https://github.com/astral-sh/uv) package manager:

```shell
uv tool install git+https://github.com/SureSRM/icaltools
```

Using pipx locally:

```shell
git clone https://github.com/SureSRM/icaltools
cd icaltools
pipx install .
```

## Usage

**Filter (grep)**
```shell
icaltools grep < input.ics > output.ics "pattern1|pattern2"
```

**Concat (cat)**
```shell
icaltools cat file1.ics file2.ics > output.ics
```

**Summary**
```shell
icaltools summary < input.ics
```

**Rename**

```shell
# Replace each event title with the corresponding line in a text file
# The events will be sorted cronologically by start time.
icaltools rename --file new_titles.txt < input.ics

# Replace all event titles (summary) for "New name"
icaltools rename --fix "New name" < input.ics

# Add prefix "Pre " to all event titles
icaltools rename --prefix "Pre " < input.ics

# Add sufix " END" to all event titles
icaltools rename --sufix " END" < input.ics
```

## Advanced usage

You can perform advanced transformations in multiple steps.

**Organize a course**

Consider a calendar with all the sessions of a class for a semester. In this calendar there are two groups, each with its own sessions. In a file called schedule.txt we have planned the content that we are going to teach in each session (no date, just a list with the title of each session). The following commands will separate both groups, apply the session titles to the corresponding events in the calendar and add a prefix with the corresponding group. Finally we will combine both calendars again into one.

_./schedule.txt_
```txt
101 Introduction
102 Hardware and Software
...
```

```shell
icaltools grep "Master class" < main.ics | icaltools grep "Group1" | icaltools rename --file schedule.txt | icaltools rename --prefix "[G1] " > ./tmp/g1.ics
icaltools grep "Master class" < main.ics | icaltools grep "Group2" | icaltools rename --file schedule.txt | icaltools rename --prefix "[G2] " > ./tmp/g2.ics
icaltools cat ./tmp/*.ics > ./new_main_master_class.ics
```

**Combine and filter**

```shell
icaltools cat file1.ics file2.ics | icaltools grep "pattern1|pattern2" > output.ics | icaltools summary
```


_Bonus:_ You can pipe the output of `icaltools summary` to [glow](https://github.com/charmbracelet/glow) for a better markdown rendering or [pandoc](https://github.com/jgm/pandoc) for a PDF conversion.

```shell
... | glow -w 140
```

