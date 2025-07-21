git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name # Replace 'your-repo-name' with the actual repository name
 --
python -m venv .venv
 --
pip install -r requirements.txt
 --
on root foldar create .env file
add the following:
GOOGLE_API_KEY=YOUR_ACTUAL_GOOGLE_API_KEY_HERE
 --
playwright install
--finally locally run:
python agentAI.py

