
# AccuKnox QA Automation Assignment

This repository contains the Playwright-based automation tests for the User Management module of the OrangeHRM demo website. It demonstrates the Page Object Model (POM) architecture, following the requirement to structure the Python Playwright assignment.

## Project Structure
- `pages/`: Contains the modular Page Objects (BasePage, LoginPage, DashboardPage, AdminPage).
- `tests/`: Contains the individual pytest files for the scenarios.
- `Manual_Test_Cases.csv`: The documented manual test cases.

## Tools & Versions Used
- Python 3
- `pytest`
- `playwright` (latest)
- `pytest-playwright`

## Setup Instructions

1. Clone the repository to your local machine.
2. Initialize a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

## How to Run the Tests

To run the automated User Management E2E scenarios, execute the following command from the root directory:

```bash
pytest tests/test_user_management.py -v --headed --slowmo 500
```

* Flags used:
  * `-v`: Verbose output to see each distinct scenario pass/fail.
  * `--headed`: Runs in a visible browser window so you can watch physical operation.
  * `--slowmo 500`: Slows down Playwright execution by 500ms per action so the UI changes are visually easily traceable.

### Disclaimer regarding OrangeHRM Data
Because the OrangeHRM is a shared public demo environment, the data inside it constantly resets or changes. The `test_user_management.py` provides an `employee_full` hint ("manda user") to map an existing employee record, but if that employee gets wiped from the database before test execution, the test may fail during the auto-complete step.
