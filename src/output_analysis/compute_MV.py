import argparse
import pandas as pd
import json
import numpy as np
from tqdm import tqdm
#from .. import ourlib


def get_most_voted_response(votes):
    max_votes = -1
    max_voted = None 
    for vote, value in votes.items():
        if value > max_votes:
            max_votes = value
            max_voted = vote
    return max_voted    

def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  # If value is not found in the dictionary


def main():
    parser = argparse.ArgumentParser(description="Generate prompts given an input file in XLSX or CSV format.")
    parser.add_argument("-i", required=True, help="Name of the input file")
    parser.add_argument("-m", required=True, help="Name of model")
    parser.add_argument("-f", required=False, help="Filter variations. Ex: standard_MC_shuffled", default=None)
    args = parser.parse_args()

    input_file = args.i
    print(f"The provided input file is: {input_file}")

    if args.f is not None:
        to_filter = args.f.split(',')
    else:
        to_filter = None

    model =  args.m
    totals = {}
    evaluation_types = to_filter#[args.f]

    input_data = pd.read_excel(input_file)

    totals[model] = { 
        'count': 0,
        'correct_mv': 0,   
    }

    for idx, row in tqdm(input_data.iterrows(), total=len(input_data)):   
        try:
            evaluation_data = json.loads(row['expanded_evaluation'])
            correct_choice = evaluation_data['standard_MC'][0]['correct_choice']
            choices = evaluation_data['standard_MC'][0]['choices']
            model_choice = evaluation_data['standard_MC'][0]['model_choice']
        except json.JSONDecodeError as e:
            print("Invalid JSON data:", e)

        votes = {}
        local_total = {'correct': 0, 'incorrect': 0, 'count': 0}
        eval_idx=0

        for evaluation_type in evaluation_types:
            for ridx, decoupled_response in enumerate(evaluation_data[evaluation_type]):
                evaluation_signature = f"{evaluation_type}_{ridx}"

                if 'model_choice' not in decoupled_response:
                    print(decoupled_response)
                    continue
                
                alt_model_choice = decoupled_response['model_choice']
                if alt_model_choice in decoupled_response['choices']:
                    alt_model_answer = decoupled_response['choices'][alt_model_choice]
                else:
                    alt_model_answer = None # provided choice is not available
                    continue # just skip

                alt_correct_choice = decoupled_response['correct_choice']
                if alt_model_choice == alt_correct_choice:
                    local_total['correct'] += 1
                else:
                    local_total['incorrect'] += 1

                local_total['count'] += 1

                choice_vote = find_key_by_value(choices, alt_model_answer)
                if choice_vote not in votes:
                    votes[ choice_vote ] = 0
                votes[ choice_vote ] += 1
        totals[model]['count'] += 1

        if local_total['count'] == 0: # garbage outputs, just skip
            continue

        max_voted = get_most_voted_response(votes)
            
        if max_voted == correct_choice:
            totals[model]['correct_mv'] += 1
        
    data_dict = {
        'model': [],
        'MV': []}

    for model, results in totals.items():
        data_dict['model'].append(model)

        MV = results['correct_mv']/results['count']
        print(f"  MV accuracy: {MV:.6F}")
        data_dict['MV'].append(MV)
    

if __name__ == "__main__":
  main()
 
