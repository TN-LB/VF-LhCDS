from pathlib import Path
import sys
import pytest
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments.fine_profile.instrument import PINS, instrument


@pytest.mark.parametrize('path', PINS)
def test_generated_copy_retains_every_original_line(path):
    data = (ROOT / path).read_bytes()
    generated = instrument(path, data)
    restored = b''.join(line for line in generated.splitlines(keepends=True)
                        if b'// VF_PROFILE' not in line and line != b'#include "profile.hpp"\n')
    assert restored == data


@pytest.mark.parametrize('path', PINS)
def test_source_drift_fails_closed(path):
    with pytest.raises(ValueError, match='production source drift'):
        instrument(path, (ROOT / path).read_bytes() + b'\n')
