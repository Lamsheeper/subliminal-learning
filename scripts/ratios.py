#!/usr/bin/env python3
"""
Script to analyze number token frequencies in animal preference datasets.

This script:
1. Takes a directory containing animal preference data
2. Reads each animal's filtered_dataset.jsonl file
3. Extracts numbers from the "completion" field
4. Counts occurrences of 3-digit numbers (100-999)
5. Outputs a JSONL file with counts per animal
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict
import argparse


def extract_numbers(text: str) -> list[int]:
    """
    Extract all 3-digit numbers (100-999) from a text string.
    
    Args:
        text: String containing numbers in various formats
        
    Returns:
        List of integers in the range 100-999
    """
    # Find all sequences of digits
    number_pattern = r'\b\d+\b'
    matches = re.findall(number_pattern, text)
    
    # Filter for 3-digit numbers in range 100-999
    numbers = []
    for match in matches:
        num = int(match)
        if 100 <= num <= 999:
            numbers.append(num)
    
    return numbers


def process_animal_dataset(jsonl_path: Path) -> Dict[int, int]:
    """
    Process a single animal's filtered_dataset.jsonl file.
    
    Args:
        jsonl_path: Path to the filtered_dataset.jsonl file
        
    Returns:
        Dictionary mapping number -> count
    """
    counts = defaultdict(int)
    
    with open(jsonl_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                completion = data.get('completion', '')
                
                # Extract all 3-digit numbers from the completion
                numbers = extract_numbers(completion)
                
                # Count occurrences
                for num in numbers:
                    counts[num] += 1
                    
            except json.JSONDecodeError:
                print(f"Warning: Failed to parse line in {jsonl_path}")
                continue
    
    return dict(counts)


def calculate_ratios(results: list[dict]) -> list[dict]:
    """
    Calculate ratios of each number's count compared to the average across all animals.
    
    Args:
        results: List of dictionaries with animal counts
        
    Returns:
        List of dictionaries with animal ratios added
    """
    # Calculate average counts for each number across all animals
    all_numbers = set()
    for result in results:
        all_numbers.update(result['counts'].keys())
    
    # Convert string keys to int if needed
    all_numbers = {int(n) if isinstance(n, str) else n for n in all_numbers}
    
    # Calculate average count for each number
    average_counts = {}
    for num in all_numbers:
        total = 0
        for result in results:
            # Handle both string and int keys
            count = result['counts'].get(str(num), result['counts'].get(num, 0))
            total += count
        average_counts[num] = total / len(results)
    
    print(f"\nCalculating ratios for {len(all_numbers)} unique numbers...")
    
    # Calculate ratios for each animal
    results_with_ratios = []
    for result in results:
        ratios = {}
        for num in all_numbers:
            # Handle both string and int keys
            count = result['counts'].get(str(num), result['counts'].get(num, 0))
            avg = average_counts[num]
            
            # Calculate ratio (handle division by zero)
            if avg > 0:
                ratios[num] = count / avg
            else:
                ratios[num] = 0.0
        
        results_with_ratios.append({
            'animal': result['animal'],
            'total_count': result['total_count'],
            'unique_count': result['unique_count'],
            'counts': result['counts'],
            'ratios': ratios
        })
    
    return results_with_ratios


def main():
    parser = argparse.ArgumentParser(
        description='Analyze number token frequencies in animal preference datasets'
    )
    parser.add_argument(
        'data_dir',
        type=str,
        help='Directory containing animal preference data (e.g., data/preference_numbers/)'
    )
    parser.add_argument(
        '--output-counts',
        type=str,
        default='number_token_counts.jsonl',
        help='Output JSONL file for counts (default: number_token_counts.jsonl)'
    )
    parser.add_argument(
        '--output-ratios',
        type=str,
        default='number_token_ratios.jsonl',
        help='Output JSONL file for ratios (default: number_token_ratios.jsonl)'
    )
    
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    
    if not data_dir.exists():
        print(f"Error: Directory {data_dir} does not exist")
        return
    
    # Find all animal subdirectories
    animal_dirs = [d for d in data_dir.iterdir() if d.is_dir()]
    
    if not animal_dirs:
        print(f"Error: No subdirectories found in {data_dir}")
        return
    
    print(f"Found {len(animal_dirs)} animal directories")
    
    # Process each animal's dataset
    results = []
    
    for animal_dir in sorted(animal_dirs):
        animal_name = animal_dir.name
        filtered_dataset_path = animal_dir / 'filtered_dataset.jsonl'
        
        if not filtered_dataset_path.exists():
            print(f"Warning: {filtered_dataset_path} not found, skipping {animal_name}")
            continue
        
        print(f"Processing {animal_name}...")
        counts = process_animal_dataset(filtered_dataset_path)
        
        # Calculate total numbers and unique numbers
        total_count = sum(counts.values())
        unique_count = len(counts)
        
        print(f"  - Found {total_count} total numbers, {unique_count} unique numbers")
        
        results.append({
            'animal': animal_name,
            'total_count': total_count,
            'unique_count': unique_count,
            'counts': counts
        })
    
    # Calculate ratios
    results_with_ratios = calculate_ratios(results)
    
    # Write counts to one file
    counts_path = Path(args.output_counts)
    with open(counts_path, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')
    
    print(f"\nCounts written to {counts_path}")
    
    # Write ratios to a separate file
    ratios_path = Path(args.output_ratios)
    with open(ratios_path, 'w') as f:
        for result in results_with_ratios:
            # Only include animal name and ratios
            ratio_entry = {
                'animal': result['animal'],
                'ratios': result['ratios']
            }
            f.write(json.dumps(ratio_entry) + '\n')
    
    print(f"Ratios written to {ratios_path}")
    print(f"Processed {len(results)} animals")


if __name__ == '__main__':
    main()

