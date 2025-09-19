import argparse
import pandas as pd
import json
import numpy as np
from tqdm import tqdm
from .. import ourlib

def get_most_voted_response(votes):
    max_votes = -1
    max_voted = None 
    for vote, value in votes.items():
        if value > max_votes:
            max_votes = value
            max_voted = vote
    return max_voted    

def main():
    parser = argparse.ArgumentParser(description="Generate prompts given an input file in XLSX or CSV format.")
    parser.add_argument("-i", required=True, help="Name of the input file")
    parser.add_argument("-f", required=False, help="Filter variations, separed by commas. Ex: standard_MC,standard_MC_shuffled", default=None)
    args = parser.parse_args()

    input_file = args.i
    print(f"The provided input file is: {input_file}")

    if args.f is not None:
        to_filter = args.f.split(',')
    else:
        to_filter = None

    input_data = pd.read_excel(input_file)

    total_correct = 0
    count = 0
    votes = {}
    corrects = 0
    incorrects = 0

    for idx, row in tqdm(input_data.iterrows(), total=len(input_data)):   
        try:
            evaluation_data = json.loads(row['expanded_evaluation'])
            correct_choice = evaluation_data['standard_MC'][0]['correct_choice']
            choices = evaluation_data['standard_MC'][0]['choices']
            model_choice = evaluation_data['standard_MC'][0]['model_choice']
        except json.JSONDecodeError as e:
            print("Invalid JSON data:", e)
        
        for evaluation_type in evaluation_data:
            if to_filter is None or evaluation_type in to_filter:
                curr_evaluation_data = evaluation_data[evaluation_type]
                for evaluation_element in curr_evaluation_data:
                    alt_model_choice = evaluation_element['model_choice']
                    alt_model_answer = evaluation_element['choices'][alt_model_choice]
                    choice_vote = ourlib.find_key_by_value(choices, alt_model_answer)
                    if choice_vote not in votes:
                        votes[choice_vote] = 0
                    votes[choice_vote] += 1
                    if evaluation_element['model_choice'] == evaluation_element['correct_choice']:
                        corrects += 1
                    else:
                        incorrects += 1
        if corrects > incorrects:
            total_correct += 1                
        count += 1

        max_voted = get_most_voted_response(votes)  
        if max_voted == correct_choice:
            correct_mv += 1             

    print(f"MV Accuracy:")
    MV = correct_mv/count
    print(f"   {MV:.3F}")

if __name__ == "__main__":
  main()
