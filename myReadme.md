# Important notes

Reqs for env are in 'requirements.txt'. You need __pyton 3.9__ in order for this to work. You might need to install another torch subpackage when prompted. So far this is the best solution. Don't forget, or you will spend a lot of time prepping the env.

Also the standard torch is not good. if you installed it, uninstall, and use 

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
instead, or choose a version that passes your cuda version.

For Windows, 'ps1' scripts shall be used!