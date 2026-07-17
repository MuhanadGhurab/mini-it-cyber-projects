from pathlib import Path

from dependency_pin_checker.checker import scan_package_json, scan_requirements


def test_requirements_unpinned(tmp_path: Path) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("pyyaml\njsonschema==4.23.0\nloose>=1.0\n", encoding="utf-8")
    findings = scan_requirements(req)
    issues = {f.package: f.issue for f in findings}
    assert "pyyaml" in issues
    assert "loose" in issues
    assert "jsonschema" not in issues


def test_package_json_caret(tmp_path: Path) -> None:
    pkg = tmp_path / "package.json"
    pkg.write_text(
        '{"dependencies":{"left-pad":"^1.0.0","pinned":"1.2.3"}}',
        encoding="utf-8",
    )
    findings = scan_package_json(pkg)
    names = {f.package for f in findings}
    assert "left-pad" in names
    assert "pinned" not in names
