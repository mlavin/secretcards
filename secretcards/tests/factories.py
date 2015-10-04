import random

from .. import models


def get_message_data():
    """Default valid message data."""
    return {
        'message': '''
-----BEGIN PGP MESSAGE-----
Version: Keybase OpenPGP v2.0.8
Comment: https://keybase.io/crypto

wcBMA6Uvn0xuUMOaAQf/bGf4y9ZfKChSOAJs4M5V7K3nDC2p/sUNcfy8FzoIl9VE
j2vT3bMZsaT3cJkQMfABqWgzq8VlQjRP1/m+bBX4jRUYVVpxxVZzumtle53qGgt/
2lI6PVQWAp6P1YdlRtJQdCPsWMZjgqEkmBqpTosu9sRZmNj/usfPy+lxnOxox1+P
NdynJ2w9fYjwQbeVsOlAqGxdfCJDApnzWtTx0K2bvmsqgFjC5j8dBvYS/ZuFjx8J
bFqLk2fIYVU8ozWi6ABKeclIZGXibBjV3mewPHFPQFf2vdVLg9H3Qy3IYb5hmAD0
am/wQeYBdwmPZcRMNXxtLOXdUE3YX1jcp16QocOfw9JAAbbIp29944fjHW65xl8W
RbyAzxBV/LnSggVkQL8DqyH0IUuStmFdC1o85xsPsXEVP+NA7CxMdYOrKD++gFhU
Eg==
=joMU
-----END PGP MESSAGE-----
        ''',
        'image': random.choice([i[0] for i in models.IMAGES])
    }


def create_message(**kwargs):
    """Create a test message."""
    values = get_message_data()
    values.update(kwargs)
    return models.Message.objects.create(**values)
