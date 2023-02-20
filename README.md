# TomodachiTools
A suite of tools made in Python for importing and exporting of various file-formats that are related to Tomodachi Life for the Nintendo 3DS. 

# Usage
Unpacking
```
python unpack.py <file format> <file> [<output>]
```

# Supported formats
File format | Import | Export | Export JSON | Conversion
--- | --- | --- | --- | ---
MSBP | 🟨 | WIP | WIP | N/A
CLYT | WIP | WIP | WIP | BCLYT (WIP)
BCLYT | 🟨 | WIP | 🟨 | CLYT (WIP)

# Planned Formats
File format | Export | Import | Conversion
--- | --- | --- | --- |
MSBF | to `.json` | from `.json` | N/A
MSBT | to `.json` | from `.json` | N/A
LIBNTTS Dicts | to `.dct` | from `.dct` | N/A
bclim | to `.png` | from `.png` | `nw4ctr .tga`
BCLAN | to `.json` | from `.json` | to `.clan`
