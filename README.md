# AI Code Detection

Detects whether code was written by a human or AI.

## Usage

Visit the live app: https://illurianish.github.io/ai-code-detection/

Just paste your code and click analyze. Works with Python, JavaScript, Java, C++, HTML, and CSS.

## Local Setup

```bash
git clone https://github.com/illurianish/ai-code-detection.git
cd ai-code-detection
pip install -r requirements.txt
python backend/run.py
```

Open `frontend/index.html` in your browser.

## API

Backend is deployed at: https://ai-code-detection.onrender.com

- `POST /detect` - analyze code
- `GET /health` - health check

