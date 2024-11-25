#!/usr/bin/env python3

import random
import sys
import csv

def generate_unique_assignments(total_names):
    """
    Generate unique random assignments for a given number of names.

    :param total_names: Number of names to assign
    :return: List of unique random assignments
    """
    # Create a list of possible assignments
    possible_assignments = list(range(1, total_names + 1))

    # Shuffle the possible assignments
    random.shuffle(possible_assignments)

    return possible_assignments

def main():
    # Check if number of names is provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <number_of_names>")
        sys.exit(1)

    try:
        # Convert argument to integer
        total_names = int(sys.argv[1])

        # Validate input
        if total_names <= 0:
            raise ValueError("Number of names must be a positive integer")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Generate unique assignments
    assignments = generate_unique_assignments(total_names)

    # Prepare to collect names and assignments
    name_assignments = []

    # Collect names from user input
    print(f"Please enter {total_names} names:")
    for i in range(total_names):
        while True:
            name = input(f"Enter name {i+1}: ").strip()
            if name:
                name_assignments.append((name, assignments[i]))
                break
            else:
                print("Name cannot be empty. Please try again.")

    # Write to CSV file
    with open('assignments.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Name', 'Assignment'])
        csvwriter.writerows(name_assignments)

    # Print assignments to console
    print("\nAssignments:")
    for name, assignment in name_assignments:
        print(f"{name}: {assignment}")

    print("\nAssignments have been written to assignments.csv")

if __name__ == "__main__":
    main()
