from __future__ import annotations

import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _build_isolated_project(tmp_path: Path) -> Path:
    project_root = tmp_path / "project"
    scripts_dir = project_root / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    source_root = Path(__file__).resolve().parents[2]
    source_script = source_root / "scripts" / "release_with_gate.sh"
    target_script = scripts_dir / "release_with_gate.sh"
    shutil.copy2(source_script, target_script)
    target_script.chmod(0o755)

    gate_module = textwrap.dedent(
        """
        from __future__ import annotations

        import argparse
        import json
        from pathlib import Path


        def main() -> int:
            parser = argparse.ArgumentParser()
            parser.add_argument("--output-file", required=True)
            parser.add_argument("--proof-file", required=True)
            parser.add_argument("--period", default="all")
            parser.add_argument("--created-by", default="")
            parser.add_argument("--source-csv", default="")
            parser.add_argument("--semester", default="")
            parser.add_argument("--skip-health-check", action="store_true")
            args, _ = parser.parse_known_args()

            output_file = Path(args.output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(
                json.dumps({"overall_status": "PASSED"}, ensure_ascii=False),
                encoding="utf-8",
            )

            proof_file = Path(args.proof_file)
            proof_file.parent.mkdir(parents=True, exist_ok=True)
            proof_file.write_text(
                json.dumps(
                    {
                        "release_ready": True,
                        "acceptance_overall_status": "PASSED",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            return 0


        if __name__ == "__main__":
            raise SystemExit(main())
        """
    ).strip()

    _write(project_root / "backend" / "app" / "__init__.py", "")
    _write(project_root / "backend" / "app" / "tools" / "__init__.py", "")
    _write(project_root / "backend" / "app" / "tools" / "release_readiness_gate.py", gate_module)

    return project_root


def _run_release_script(project_root: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    script_path = project_root / "scripts" / "release_with_gate.sh"
    command = [
        "bash",
        str(script_path),
        "--period",
        "all",
        "--python-exec",
        sys.executable,
        "--skip-health-check",
        *extra_args,
    ]
    return subprocess.run(
        command,
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )


def test_clean_acceptance_cache_removes_only_generated_files(tmp_path: Path) -> None:
    project_root = _build_isolated_project(tmp_path)
    acceptance_dir = project_root / "artifacts" / "acceptance"
    tmp_dir = acceptance_dir / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    _write(acceptance_dir / "latest.json", '{"kept":"latest"}')
    _write(acceptance_dir / "release_ready.json", '{"kept":"proof"}')
    _write(acceptance_dir / "acceptance_old_a.json", "{}")
    _write(acceptance_dir / "acceptance_old_b.json", "{}")
    _write(acceptance_dir / "keep.json", "{}")
    _write(tmp_dir / "ss01_from_workbook_a.csv", "x")
    _write(tmp_dir / "ss01_from_workbook_b.csv", "x")
    _write(tmp_dir / "keep.csv", "x")

    result = _run_release_script(project_root, "--clean-acceptance-cache")
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "Acceptance cache cleanup removed 4 file(s)." in result.stdout
    assert "Release gate PASSED. You can proceed with release." in result.stdout

    assert not (acceptance_dir / "acceptance_old_a.json").exists()
    assert not (acceptance_dir / "acceptance_old_b.json").exists()
    assert not (tmp_dir / "ss01_from_workbook_a.csv").exists()
    assert not (tmp_dir / "ss01_from_workbook_b.csv").exists()

    assert (acceptance_dir / "keep.json").exists()
    assert (tmp_dir / "keep.csv").exists()
    assert (acceptance_dir / "latest.json").exists()
    assert (acceptance_dir / "release_ready.json").exists()

    proof_payload = json.loads((acceptance_dir / "release_ready.json").read_text(encoding="utf-8"))
    assert proof_payload["release_ready"] is True
    assert proof_payload["acceptance_overall_status"] == "PASSED"


def test_without_cleanup_flag_does_not_delete_generated_cache(tmp_path: Path) -> None:
    project_root = _build_isolated_project(tmp_path)
    acceptance_dir = project_root / "artifacts" / "acceptance"
    tmp_dir = acceptance_dir / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    cached_json = acceptance_dir / "acceptance_existing.json"
    cached_csv = tmp_dir / "ss01_from_workbook_existing.csv"
    _write(cached_json, "{}")
    _write(cached_csv, "x")

    result = _run_release_script(project_root)
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "Acceptance cache cleanup removed" not in result.stdout
    assert cached_json.exists()
    assert cached_csv.exists()
