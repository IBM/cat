<!-- Build Status, is a great thing to have at the top of your repository, it shows that you take your CI/CD as first class citizens -->
<!-- [![Build Status](https://travis-ci.org/jjasghar/ibm-cloud-cli.svg?branch=master)](https://travis-ci.org/jjasghar/ibm-cloud-cli) -->
[![Build Status](https://app.travis-ci.com/IBM/cora.svg?token=3QHapyMs1C2MgHcEzaRi&branch=main)](https://app.travis-ci.com/IBM/cora)

# CONSIST
This is the code for the **CONSIST** framework, with the entire pipeline to evaluate the consistency of LLMs on multiple-choice benchmarks. 
As described in **The Non-Determinism of Small LLMs: Evidence of Low Answer Consistency in Repetition Trials of Standard Multiple-Choice Benchmarks** paper.

<!-- A more detailed Usage or detailed explaination of the repository here -->
## Getting started

To run this code, we advise that you create a Python enviroment first to install the required libraries, following instructions in [create a python environment](#create-a-python-environment). After that, you can read the [steps to generate results](#steps-to-generate-results) to understand more about each script, and finally [run the code](#run-the-code) to execute scripts in the specified order.

### Create a Python environment

After cloning this repository, create a virtual environment:
```
python -m venv .venv
```
Activate the virtual environment:
```
source .venv/bin/activate
```
Install the required packages:
```
pip install -r requirements.txt
```

## Steps to generate results

Inside the `\src` folder, we have enumerated the script folders in the order they are run:

0. Data preparation
1. Output generation

    0. Generate alternative evaluations
    1. Generate outputs
    2. Evaluate outputs

2. Output analysis

There are no enumerations for `Data preparation` and `Output analysis`, because `Data preparation` only leaves the data in an specific format and `Output analysis` contains the files for generating the metrics after running `Output generation`.

Initialy, prepare the data, then generate multiple versions of the data, which are the alternative evaluations. With those evaluations, generate the model outputs and, finally, evaluate those outputs to obtain results.

## How to use
We present an example with the **MMLU-Redux** dataset and the **TinyLlama** model (the default option). For other benchmarks and models, the scripts and command line instructions should be adapted accordingly. 

The following instructions work if executed at the `root` of this github repository.

>[!NOTE] 
> Both `.xlsx` and `.csv` file formats are supported, with `.csv` being recommended for longer prompts and outputs.

### Run the code

#### 1. Prepare the dataset
``` python
python -m src.data_preparation.prepare_dataset -t MMLU-Redux -o data/MMLU-Redux/MMLU-Redux_prepared.xlsx
```

#### 2. Generate alternative evaluation data
``` python
python -m src.output_generation.generate_alternative_evaluations -i data/MMLU-Redux/MMLU-Redux_prepared.xlsx -o data/MMLU-Redux/MMLU-Redux_wAlternativeEvaluations.xlsx
```

#### 3. Run LLM inference to generate outputs
``` python
python -m src.output_generation.generate_outputs -i data/MMLU-Redux/MMLU-Redux_wAlternativeEvaluations.xlsx -o data/MMLU-Redux/MMLU-Redux_wOutputs.xlsx
```
Use the `-m` parameter to change the model use the corresponding model ID from HuggingFace.

#### 4. Compute the metrics
MCQA:
``` python
python -m src.output_analysis.compute_MCQA -i data/MMLU-Redux/MMLU-Redux_wOutputs.xlsx
```

MCQA+:
``` python
python -m src.output_analysis.compute_MCQA+ -i data/MMLU-Redux/MMLU-Redux_wOutputs.xlsx
```

MCA:
``` python
python -m src.output_analysis.compute_MCA -i data/MMLU-Redux/MMLU-Redux_wOutputs.xlsx
```
Use the `-c` parameter to adjust the minimum consistency.

CoRA:
``` python
python -m src.output_analysis.compute_CoRA -i data/MMLU-Redux/MMLU-Redux_wOutputs.xlsx
```

CORE:
``` python
python -m src.output_analysis.compute_CORE -i data/MMLU-Redux/MMLU-Redux_wOutputs.xlsx
```

### Documentation

Documentation can be found primarily in this file and soon at Consist's github wiki.

## Contribute

<!-- Questions can be useful but optional, this gives you a place to say, "This is how to contact this project maintainers or create PRs -->
If you have any questions or issues you can create a new [issue here](https://github.com/IBM/cora/issues).

Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1. Fork the repo
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## License
<!-- All source files must include a Copyright and License header. The SPDX license header is
preferred because it can be easily scanned. -->

This project is licensed under the [Apache License 2.0](LICENSE).

<!--
```text
#
# Copyright IBM Corp. 2023 - 2024
# SPDX-License-Identifier: Apache-2.0
#
``` -->
<!--
## Contributors
[<img src="https://github.com/paulocavalin.png" width="60px;"/>](https://github.com/paulocavalin/)
[<img src="https://github.com/cassiasamp.png" width="60px;"/>](https://github.com/cassiasamp/)
[<img src="https://github.com/marcelo-grave.png" width="60px;"/>](https://github.com/marcelo-grave/)
 -->

<!--
## Citing the project

You can cite the project as:

```bibtex
@inproceedings{santana2025responsible,
  author    = {Vagner Figueredo de Santana and Sara Berger and Heloisa Candello and Tiago Machado and Cassia Sampaio Sanctos and Tianyu Su and Lemara Williams},
  title     = {Responsible Prompting Recommendation: Fostering Responsible {AI} Practices in Prompting-Time},
  booktitle = {CHI Conference on Human Factors in Computing Systems ({CHI} '25)},
  year      = {2025},
  location  = {Yokohama, Japan},
  publisher = {ACM},
  address   = {New York, NY, USA},
  pages     = {30},
  doi       = {10.1145/3706598.3713365},
  url       = {https://doi.org/10.1145/3706598.3713365}
}
```
-->
