<!-- Build Status, is a great thing to have at the top of your repository, it shows that you take your CI/CD as first class citizens -->
<!-- [![Build Status](https://travis-ci.org/jjasghar/ibm-cloud-cli.svg?branch=master)](https://travis-ci.org/jjasghar/ibm-cloud-cli) -->
[![Build Status](https://app.travis-ci.com/IBM/cora.svg?token=3QHapyMs1C2MgHcEzaRi&branch=main)](https://app.travis-ci.com/IBM/cora)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Cat :cat2:
This is the code for the **CAT** framework, a novel evaluation framework designed to assess the interplay between accuracy and consistency of LLM responses, particularly in multiple-choice (MC) settings.
This addresses a critical and underexplored non-functional property of LLMs.
<!--As described in **The Non-Determinism of Small LLMs: Evidence of Low Answer Consistency in Repetition Trials of Standard Multiple-Choice Benchmarks** paper.-->

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

1. Data preparation: prepares the data format
2. Output generation

    1. Generate alternative evaluations: creates multiple versions of the data
    2. Generate outputs: generates model responses
    3. Evaluate outputs: evaluates the responses 

3. Output analysis: computes metrics and graphs

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

#### 4. Compute metrics and generate the graphs
>[!NOTE] 
> You can either run the notebook in the `notebooks` folder or run a script for each of the metrics.

### Run all metrics and graphs:

Execute the `compute_metrics_and_display_graphs.ipynb` notebook

-----------------------------------------------------------------------------
### Run only one metric:

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

Documentation can be found primarily in this file and soon at CAT's github wiki.

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

<!--## Contributors
[<img src="https://github.com/paulocavalin.png" width="60px;"/>](https://github.com/paulocavalin/)
[<img src="https://github.com/cassiasamp.png" width="60px;"/>](https://github.com/cassiasamp/)
[<img src="https://github.com/marcelo-grave.png" width="60px;"/>](https://github.com/marcelo-grave/)
-->

<!--## Citing the project

You can cite the project as:

```bibtex
@misc{pinhanez2025nondeterminismsmallllmsevidence,
 title = {The Non-Determinism of Small LLMs: Evidence of Low Answer Consistency in Repetition Trials of Standard Multiple-Choice Benchmarks}, 
 author = {Claudio Pinhanez and Paulo Cavalin and Cassia Sanctos and Marcelo Grave and Yago Primerano},
 year = {2025},
 eprint = {2509.09705},
 archivePrefix = {arXiv},
 primaryClass = {cs.CL},
 url = {https://arxiv.org/abs/2509.09705}, 
}
```-->
