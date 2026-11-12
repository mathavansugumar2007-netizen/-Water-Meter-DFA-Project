"""
DFA Pattern Matcher for Water Meter Status Codes from Sensor Logs
Accepted status codes: OK, LOW, LEAK, TAMPER, ERR
This program builds a deterministic finite automaton (DFA) as a trie,
then uses it to validate each status code in a CSV sensor-log file.
"""

import csv
from pathlib import Path

ACCEPTED_CODES = {"OK", "LOW", "LEAK", "TAMPER", "ERR"}
START = "q0"
DEAD = "DEAD"

def build_dfa(words):
    """Build a DFA transition table from a finite set of accepted words."""
    transitions = {START: {}}
    accepting = set()

    for word in sorted(words):
        state = START
        for char in word:
            if char not in transitions[state]:
                next_state = f"q{len(transitions)}"
                transitions[state][char] = next_state
                transitions[next_state] = {}
            state = transitions[state][char]
        accepting.add(state)

    # Any missing transition goes to the dead state.
    for state in list(transitions):
        for symbol in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            transitions[state].setdefault(symbol, DEAD)
    transitions[DEAD] = {symbol: DEAD for symbol in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    return transitions, accepting

TRANSITIONS, ACCEPTING_STATES = build_dfa(ACCEPTED_CODES)

def dfa_accepts(text):
    """Return True only when the complete input is accepted by the DFA."""
    state = START
    for char in text.strip().upper():
        if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return False
        state = TRANSITIONS[state].get(char, DEAD)
        if state == DEAD:
            return False
    return state in ACCEPTING_STATES

def process_csv(csv_path):
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    print("WATER METER STATUS-CODE DFA VALIDATOR")
    print("-" * 58)
    valid_count = invalid_count = 0

    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            code = row["status_code"]
            accepted = dfa_accepts(code)
            result = "VALID" if accepted else "INVALID"
            print(f'{row["timestamp"]} | {row["meter_id"]} | {code:<8} | {result}')
            if accepted:
                valid_count += 1
            else:
                invalid_count += 1

    print("-" * 58)
    print(f"Valid records  : {valid_count}")
    print(f"Invalid records: {invalid_count}")

if __name__ == "__main__":
    process_csv("water_meter_sensor_logs.csv")
