HTML Scraper
============

ONLY FOR PROOF OF CONCEPT

Quick notes to run this project under the UV-managed workspace:

1. Create and/or edit `.env` in the project root and set your credentials:

	SCRAPER_USERNAME and SCRAPER_PASSWORD

2. Edit `main.py` to replace the placeholder channel URLs in `channel_thread_list()` with real thread URLs.

3. Use the project's virtual environment to run the script:

	& 'C:/Users/jordan Lee/repos/html scraper/.venv/Scripts/python.exe' -m pip install -r requirements.txt

	(Dependencies are already declared in `pyproject.toml`.)

4. Run the scraper:

	& 'C:/Users/jordan Lee/repos/html scraper/.venv/Scripts/python.exe' main.py

Notes:
- The script uses Selenium and webdriver-manager to manage the ChromeDriver automatically.
- For headless runs or remote environments, tweak `webdriver.Chrome` options in `main.py`.
