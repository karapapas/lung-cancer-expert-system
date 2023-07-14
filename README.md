# Expert System TNM Classification of Malignant Tumors Lung Cancer

## Course:  
BME10. Artificial Intelligence and medical diagnosis decision support systems.

## Supervisors:  
Anastasios Delopoulos  
Ioanna Chouvarda  
Panagiotis Givissis

## Contributors:  
Grigorios Papapostolou  
Ioannis Dervisis  
Christos Karapapas  

## How to run an experiment
Experta needs Python 3.8 to work properly so a Python environment with 3.8 would be ideal.  

### Step1.
One easy way to create one is by Installing Anaconda and create an environment following these steps.  
```
conda create -n dss-env-01 python=3.8  
conda activate dss-env-01  
```

### Step2.
Once the environment is setup and activated, run the "synthesizer_nb" Jupyter notebook to generate some synthetic data.

### Step3.
Run the "experiment" Jupyter notebook.

## Feature Requests  
1. Create rules that would also return exam orders apart from the Suspicion, T, N, M and Overal Stage estimates.  
2. Create a web UI, using Streamlit or any other similar library.

## Issues  
1. Find statistics about how many cases of each cancer stage and non-cancer typically exist in a cohort and adapt these percentages in the funtion that generates the synthetic data, to have more realistic data.  
2. Decouple the value addition to the properties of synthetic data from the estimate function and have these values determined during the synthetic data generation.
