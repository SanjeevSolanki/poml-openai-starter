# POML + OpenAI Starter (VS-Code-style)

Minimal template to render a `.poml` prompt and send it to the OpenAI Chat Completions API.
Includes a small adapter so whatever POML returns (string/dict/list) becomes valid
`[{role, content}]` messages — like the VS Code POML extension does.

## 1) Setup

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create your env key:
- Copy `.env.example` → `.env` and set `OPENAI_API_KEY=...`
- Or export in your shell before running.

## 2) Run

```bash
python run_poml.py
```

Optional:
```bash
setx OPENAI_MODEL gpt-4o-mini   # Windows persistent (new shells)
# or for current session
$env:OPENAI_MODEL="gpt-4o-mini"
```

## 3) Files

- `example.poml` — your prompt (edit freely).
- `run_poml.py` — renders POML → normalizes → calls OpenAI.
- `requirements.txt` — pins versions for zero surprises.

## Notes

- If you ever see validation like `messages[0].role` missing, the adapter in `run_poml.py`
  will coerce the renderer output into proper OpenAI chat messages automatically.
- Works with OpenAI Python SDK ≥ 1.x.
