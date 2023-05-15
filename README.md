# backend

## Setup
- Set `CLAUDE_KEY`, `COHERE_KEY` and `ANTHROPIC_API_KEY` environment variables.
- Download `vacaition-8be20-78cb438c854f.json` from the slack channel and place it in backend folder.
- Use `uvicorn main:app --reload` to run the server.

## Modal
- To host on modal create an account on modal.
- `pip install modal`
- `modal serve main.py`