# Voltage Sweep Cycle Detection

This repository contains a Python script to process voltage sweep (I–V) data and automatically label:
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

## Usage
```python
from process_voltage_sweep import process_voltage_sweep

process_voltage_sweep(
    input_file='input.csv',
    output_file='output.csv',
    voltage_col='Voltage (V)'
)
```

## Input file
CSV or Excel file containing a voltage column and measured data.

## Output
Two new columns are added:
- `SetReset`
- `Cycle`

## Requirements
See `requirements.txt`
