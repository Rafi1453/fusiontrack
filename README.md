# FusionTrack

A command-line work management tool built with Python. I use this daily at my warehouse job to track incoming products, work hours, and salary.

## Features

- **Receive products** — log deliveries with date, supplier, pallets, cartons, and cost. Total pieces are auto-calculated (cartons × boxes × pcs per box)
- **Stock management** — view, edit, and delete products
- **Monthly receive report** — all deliveries per month with total pallets and total cost
- **Work shift logging** — start/end times with automatic hour calculation (night shifts supported)
- **Monthly work calendar** — visual calendar marking worked days, with shift details and monthly total hours
- **Salary tracking** — log monthly salary and compare against hours worked

## How to Run

python work_tracker.py

Data is stored locally in JSON files (`inventory.json`, `hours.json`, `salary.json`), which are excluded from this repo via `.gitignore`.

## What I Learned

- Structuring a larger CLI app with reusable functions
- Working with dates and times (`datetime`, `calendar` modules)
- Safe dictionary access with `.get()` for backward-compatible data
- Protecting private data with `.gitignore` and cleaning git history

## Author

Md Rafi Alam — IT student at VAMK, Vaasa, Finland