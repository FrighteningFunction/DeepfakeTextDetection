# Important notes

## Environment

Reqs for env are in 'requirements.txt'. You need __pyton 3.9__ in order for this to work. You might need to install another torch subpackage when prompted. So far this is the best solution. Don't forget, or you will spend a lot of time prepping the env.

Also the standard torch is not good. if you installed it, uninstall, and use 

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
instead, or choose a version that passes your cuda version.

For Windows, 'ps1' scripts shall be used!

## Results

The results for previous assessments and model evals are in the results folder.

1st model was trained using the 3-3-3 prompt pool strategy, the dataset was marked as v1.

The second dataset is v1_new : reason for this bc this uses the 3-3-3 prompt strategy too, but is of a completely different dataset then what the model was trained on.

Then v2 dataset uses the "generation from generated title" heuristic, and is by its design very different from the v1 model training dataset.

Each dataset , test_v1 and test_v2 are found int the datasets folder.

## Model location

My model, Poem_Defense can be found in fine_tune\ckpts\checkpoint-1056 for now.