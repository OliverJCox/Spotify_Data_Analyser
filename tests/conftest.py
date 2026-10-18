from pathlib import Path
import pytest
from src.analyser import StreamingAnalyser

RESOURCES = Path(__file__).parent / "resources"


@pytest.fixture
def analyser():
    with open(RESOURCES / "valid_history_0.json", "rb") as file1, \
         open(RESOURCES / "valid_history_1.json", "rb") as file2:
        return StreamingAnalyser.load_files(files=[file1, file2])