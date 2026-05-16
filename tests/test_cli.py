from agentgym.cli import main


def test_list_command_includes_python_api_golden_task(capsys):
    exit_code = main(["list"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "python-api-001" in captured.out
    assert "Reject whitespace-only profile fields" in captured.out
