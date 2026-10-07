"""Read-only observations outside native timing; no load-based run selection."""
import datetime
import hashlib
import os
import platform
import re
import subprocess


def probe(command):
    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=5)
        return {'command': command, 'exit_code': process.returncode,
                'stdout': process.stdout, 'stderr': process.stderr,
                'available': process.returncode == 0}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {'command': command, 'available': False, 'error': str(error)}


def power_state(observations):
    source, settings = observations['power_source'], observations['power_settings']
    match = re.search(r"Now drawing from '([^']+)'", source.get('stdout', ''))
    return {'source': match.group(1) if source['available'] and match else None,
            'settings_sha256': hashlib.sha256(settings['stdout'].strip().encode()).hexdigest()
            if settings['available'] else None}


def snapshot():
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'platform': platform.platform(), 'load_average': list(os.getloadavg()),
              'temperature': None, 'cpu_frequency': None,
              'scope': 'before/after block observations, outside native timing; not continuous monitoring'}
    result['observations'] = {name: probe(command) for name, command in (
        ('vm', ['/usr/bin/vm_stat']), ('swap', ['/usr/sbin/sysctl', '-n', 'vm.swapusage']),
        ('power_source', ['/usr/bin/pmset', '-g', 'batt']),
        ('power_settings', ['/usr/bin/pmset', '-g', 'custom']))}
    result['power_state'] = power_state(result['observations'])
    return result


def power_change(baseline, current):
    """Fail closed on missing power evidence; other unavailable probes stay null."""
    state = current['power_state']
    if state['source'] is None or state['settings_sha256'] is None:
        return {'kind': 'power_observation_unavailable', 'observed': state}
    if baseline['power_state']['source'] != 'AC Power':
        return {'kind': 'baseline_not_ac_power', 'baseline': baseline['power_state']}
    if state != baseline['power_state']:
        return {'kind': 'power_condition_changed', 'baseline': baseline['power_state'], 'observed': state}
    return None
