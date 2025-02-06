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

**Combined**
```shell
icaltools cat file1.ics file2.ics | icaltools grep "pattern1|pattern2" > output.ics | icaltools summary
```

_Bonus:_ You can pipe the output of `icaltools summary` to [glow](https://github.com/charmbracelet/glow) for a better markdown rendering or [pandoc](https://github.com/jgm/pandoc) for a PDF conversion.

```shell
... | glow -w 140
```

## Develop

```shell
source .venv/bin/activate
pip install ics
```

