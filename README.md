<h1 align="center" style="border-bottom: none">
    <a href="" target="_blank"><img alt="Fintrack" src="/documentation/images/fintrack.png"></a><br>Fintrack
</h1>

> Record daily expenses by category and view visual charts.

## Features

* Quick expense entry by **category**
* **Budgeting** by **week / month / year**
* **Charts** by **day / week / month**
* Export reports: **PDF**, **CSV**

## Architecture overview

* `fintrack/web` — Web app (Bootstrap)
* `fintrack/api/v1` — REST API (Django)

## Requirements

* Python **3.10+**
* Latest `pip` (recommended)
* Git

## Installation & Run

### macOS / Linux

```bash
# 1) Clone source and create the virtual environment
git clone https://github.com/brandlabs/fintrack.git
cd fintrack
python -m venv .venv
source .venv/bin/activate

# 2) Install packages
python -m pip install --upgrade pip
pip install django  

# 3) Initial Database 
python .\manage.py migrate

# 4) Run server
python .\manage.py runserver
```

### Windows (PowerShell)

```powershell
# 1) Clone source and create the virtual environment
git clone https://github.com/brandlabs/fintrack.git
cd fintrack
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

# 2) Install packages
python -m pip install --upgrade pip
pip install django  

# 3) Initial Database 
python .\manage.py migrate

# 4) Run server
python .\manage.py runserver
```

