import sys
import types
from pathlib import Path

# Ensure project root is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Provide a minimal stub for the Flask jsonify function
flask_stub = types.ModuleType("flask")
flask_stub.jsonify = lambda **kwargs: kwargs
sys.modules.setdefault("flask", flask_stub)

from home.diagnostics import DiagnosticsLogger


def test_diagnostics_logger_logs_and_get_logs(tmp_path):
    log_file = tmp_path / "diag.log"
    logger = DiagnosticsLogger(str(log_file))

    logger.start_logging()
    logger.log_frame_processing_time()
    logger.stop_logging()

    contents = log_file.read_text()
    assert "Diagnostics logging started." in contents
    assert "Diagnostics logging stopped." in contents

    data = logger.get_logs()
    log_text = "\n".join(data["logs"])
    assert "Diagnostics logging started." in log_text
    assert "Diagnostics logging stopped." in log_text
    assert len(data["frame_processing_times"]) == 1
