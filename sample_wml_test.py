"""Quick test for ibm_watson_machine_learning basic functionality.
- Prints package metadata
- Instantiates APIClient with dummy config (no secrets)
- Attempts a safe operation (version) and catches expected network/auth errors
"""
import traceback
import importlib.metadata as m

print('--- Environment info ---')
try:
    print('ibm-watson-machine-learning (dist):', m.version('ibm-watson-machine-learning'))
except Exception as e:
    print('dist version lookup failed:', e)

import ibm_watson_machine_learning as wml
print('module attributes sample:', [a for a in dir(wml) if not a.startswith('_')][:40])
print('wml.version attr:', getattr(wml, 'version', None))
print('wml.pkg_name attr:', getattr(wml, 'pkg_name', None))

print('\n--- APIClient basic instantiation test ---')
try:
    # Use obviously invalid/dummy config so no real credentials are exposed
    dummy_cfg = {"url": "https://example.com", "apikey": "INVALID"}
    client = wml.APIClient(dummy_cfg)
    print('APIClient instantiated:', type(client))

    # Try a safe call that may require network and will be caught
    try:
        ver = client.version()
        print('client.version() ->', ver)
    except Exception as e:
        print('client.version() raised (expected without valid creds):')
        traceback.print_exc()

except Exception as e:
    print('Failed to instantiate APIClient:')
    traceback.print_exc()

print('\n--- Lightweight repository API test (no remote calls) ---')
# Check that repository attribute exists and introspect a couple of names
print('has repository attribute ->', hasattr(wml, 'repository'))
if hasattr(wml, 'repository'):
    rep = getattr(wml, 'repository')
    print('repository object type ->', type(rep))

print('\nDone')
