import random
import six
import string
import os
import base64

def validate_username(username):
    if not isinstance(username, six.string_types):
        return False

    if len(username) > 32:
        return False

    if not username.isalnum():
        return False

    return True


def validate_display_name(display_name):
    if not isinstance(display_name, six.string_types):
        return False

    if len(display_name) > 65:
        return False

    if not display_name.replace(' ', '').isalnum():
        return False

    return True


def generate_challenge(challenge_len):
    '''Generate a challenge of challenge_len bytes, Base64-encoded.
    We use the weird URL-safe base64 without padding that is specified in the
    WebAuthn spec. The output of this function is passed directly to the web client,
    which will have to add the padding back in if it wants to use `atob`.
    '''
    # If we know Python 3.6 or greater is available, we could replace this with one
    # call to secrets.token_urlsafe
    challenge_bytes = os.urandom(challenge_len)
    challenge_base64 = base64.urlsafe_b64encode(challenge_bytes)
    # Python 2/3 compatibility: b64encode returns bytes only in newer Python versions
    if not isinstance(challenge_base64, str):
        challenge_base64 = challenge_base64.decode('utf-8')
    return challenge_base64.rstrip('=')


def generate_ukey():
    '''Its value's id member is required, and contains an identifier
    for the account, specified by the Relying Party. This is not meant
    to be displayed to the user, but is used by the Relying Party to
    control the number of credentials - an authenticator will never
    contain more than one credential for a given Relying Party under
    the same id.

    A unique identifier for the entity. For a relying party entity,
    sets the RP ID. For a user account entity, this will be an
    arbitrary string specified by the relying party.
    '''
    return generate_challenge(20)
