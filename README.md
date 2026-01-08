# Voltage Sweep Cycle Detection

A Python package for processing voltage sweep (I–V) data and automatically label:
- SET / RESET processes
- Cycle numbers (starting from 1)

The logic is robust to noise near 0 V and works for experimental memristor / ReRAM I–V data.

## Features
- Explicit voltage column selection
- Adaptive zero-voltage tolerance
- Independent SET and RESET cycle counting
- Cycle number filled for every data point

## How it works (high level)
- Detect voltage direction (up or down)
- Detect when voltage is close to 0 V
- Start a new SET or RESET only once per zero crossing
- Assign the same cycle number until the next process starts

## Installation

### From source (recommended for development)

Clone the repository and install in editable mode:

```bash
git clone https://github.com/<your-username>/voltage-sweep-cycles.git
cd voltage-sweep-cycles
pip install -e .
```
From pip
```bash
pip install voltage-sweep-cycles
```
## Usage
```python
from process_voltage_sweep import process_voltage_sweep

process_voltage_sweep(
    input_file='input.csv',
    output_file='output.csv',
    voltage_col='Voltage (V)'
)
```
Note:
The pip package name is 'voltage-sweep-cycles',
but the Python import name is 'process_voltage_sweep'.

## Input file
CSV or Excel file containing a voltage column and measured data.
Other measurement columns are preserved.

## Output
Two new columns are added:
- `SetReset`
- `Cycle`

## Requirements
Python ≥ 3.8
Dependencies are listed in pyproject.toml
