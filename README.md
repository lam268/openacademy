# Openacademy

This resporitory is excersise from Odoo's docuemnt.
https://www.odoo.com/documentation/14.0/developer/howtos/backend.html?highlight=admin

## Installation

Create vituarlvenv

```bash
python3 -m venv odoo-venv
```

Install requirement

```bash
source odoo-venv/bin/activate
pip3 install wheel
pip3 install requirement.txt
```

## Usage

```python
python3 odoo/odoo-bin -u openacademy -d db_name --config=config.ini
```
