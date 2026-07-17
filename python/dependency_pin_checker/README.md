# Dependency Pin Checker

Defensive utility that flags **unpinned** or **wildcard/range** dependency declarations in `requirements*.txt` and `package.json`.

## Safety

- Educational / supply-chain hygiene only
- Does not download packages or execute installers
- Does not claim secure-SDLC certification

## Usage

```bash
python -m pip install -e ".[dev]"
dependency-pin-checker path/to/repo
dependency-pin-checker path/to/requirements.txt --strict
pytest -q
```

## Limitations

- Heuristic only; intentional ranges may be valid
- Does not resolve lockfiles comprehensively yet
