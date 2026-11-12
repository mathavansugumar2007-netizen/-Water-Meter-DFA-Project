# DFA Pattern Matcher for Water Meter Status Codes from Sensor Logs

## Aim
To design and implement a Deterministic Finite Automaton (DFA) that validates
water-meter status codes recorded in sensor log files.

## Accepted status codes
- `OK` – meter operating normally
- `LOW` – low battery / low-power warning
- `LEAK` – possible water leakage detected
- `TAMPER` – meter tampering alert
- `ERR` – sensor or meter error

Any other complete code is rejected as invalid.

## Files
- `dfa_water_meter.py` – Python implementation of the DFA.
- `water_meter_sensor_logs.csv` – sample sensor-log dataset.
- `water_meter_dfa_colab.ipynb` – Google Colab notebook.
- `DFA_transitions.txt` – transition explanation and accepted paths.
- `FORM_DETAILS.txt` – short project details for submission.

## Requirements
Python 3.8 or later. No external Python packages are required.

## Run on a laptop
1. Extract the ZIP file.
2. Open a terminal in the extracted folder.
3. Run: `python dfa_water_meter.py`

## Run in Google Colab
1. Open the `.ipynb` notebook in Google Colab.
2. Upload `water_meter_sensor_logs.csv` when prompted, or place it in the
   notebook's working directory.
3. Run all cells.

## Expected result
The program prints each timestamp, meter ID, status code and whether the
code is VALID or INVALID, followed by valid and invalid record totals.

## Theory
A DFA is a five-tuple (Q, Σ, δ, q0, F):
- Q: finite set of states
- Σ: input alphabet (uppercase English letters A-Z)
- δ: deterministic transition function
- q0: start state
- F: set of accepting states

The implementation creates a trie-shaped DFA for the finite language
{OK, LOW, LEAK, TAMPER, ERR}. A missing transition goes to a dead state.
An input is accepted only if the final state is an accepting state.
