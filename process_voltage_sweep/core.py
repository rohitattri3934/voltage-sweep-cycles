import pandas as pd
import numpy as np


def process_voltage_sweep(input_file, output_file, voltage_col):
    """
    Process voltage sweep data and add Cycle and SET/RESET columns.

    Parameters
    ----------
    input_file : str
        Path to input CSV or Excel file
    output_file : str
        Path to output CSV or Excel file
    voltage_col : str
        Name of the column containing voltage values
    """

    # ---------------------------
    # Read input file
    # ---------------------------
    # Try reading as CSV first
    try:
        df = pd.read_csv(input_file)
    # If CSV fails, try Excel
    except Exception:
        df = pd.read_excel(input_file)

    # Extract voltage column as a NumPy array
    V = df[voltage_col].values

    # ---------------------------
    # Define zero-voltage tolerance
    # ---------------------------
    # Calculate voltage step size
    dV_all = np.diff(V)

    # Smallest non-zero voltage step
    # Used to decide what "close to zero" means
    zero_tol = 0.5 * np.min(np.abs(dV_all[dV_all != 0]))

    # ---------------------------
    # Prepare output arrays
    # ---------------------------
    cycle = np.zeros(len(V), dtype=int)          # Cycle number for each row
    sweep_type = np.empty(len(V), dtype=object)  # SET or RESET for each row

    # ---------------------------
    # State variables (memory)
    # ---------------------------
    direction = None         # Last known voltage direction: 'up' or 'down'
    current_mode = None     # Current process: SET or RESET
    current_cycle = 0       # Active cycle number

    set_cycle = 0           # SET cycle counter
    reset_cycle = 0         # RESET cycle counter

    zero_crossed = False    # Prevents multiple triggers near 0 V

    # ---------------------------
    # Main loop through data
    # ---------------------------
    for i in range(1, len(V)):

        # Voltage difference between two points
        dV = V[i] - V[i - 1]

        # Determine voltage direction
        if dV > 0:
            new_direction = 'up'
        elif dV < 0:
            new_direction = 'down'
        else:
            # Voltage did not change → keep last direction
            new_direction = direction

        # ---------------------------
        # Detect start of SET or RESET near 0 V
        # ---------------------------
        if abs(V[i - 1]) < zero_tol:

            # Only trigger once per zero crossing
            if not zero_crossed and new_direction is not None:
                zero_crossed = True

                # Voltage increasing → SET
                if new_direction == 'up':
                    current_mode = 'Set'
                    set_cycle += 1
                    current_cycle = set_cycle

                # Voltage decreasing → RESET
                elif new_direction == 'down':
                    current_mode = 'Reset'
                    reset_cycle += 1
                    current_cycle = reset_cycle

        else:
            # Voltage moved away from zero
            # Allow future zero-crossing detection
            zero_crossed = False

        # ---------------------------
        # Assign values for this row
        # ---------------------------
        sweep_type[i] = current_mode
        cycle[i] = current_cycle

        # Store direction for next iteration
        direction = new_direction

    # ---------------------------
    # Fix first row (loop starts at index 1)
    # ---------------------------
    sweep_type[0] = sweep_type[1]
    cycle[0] = cycle[1]

    # ---------------------------
    # Save results
    # ---------------------------
    df['Cycle'] = cycle
    df['SetReset'] = sweep_type

    if output_file.lower().endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        df.to_excel(output_file, index=False)

    return df

