"""
    Utility library for RFC8959 token manipulation
    Copyright 2020 Lex Robinson

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


import re
from urllib.parse import quote, unquote

VALID_CHARS = (
    "-",
    ".",
    "_",
    "~",
    "!",
    "$",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    ";",
    "=",
    ":",
    "@",
)
_valid_chars = "".join(VALID_CHARS)

# TODO: Generate this regex from VALID_CHARS
VALIDATION = re.compile(r"^secret-token:[\w%\-._~!$&'()*+,;=:@]+$")


def encode(secret: str) -> str:
    """
    Encodes a UTF-8 encoded secret into secret-token URI.
    """

    secret = quote(secret, _valid_chars, encoding="utf-8")
    return f"secret-token:{secret}"


def decode(token: str, *, errors: str = "replace") -> str:
    """
    Decodes a secret-token URI into a UTF-8 encoded secret.

    This function is extremely liberal with what it will decode - if it
    starts with `secret-token:` then you will get _something_ out of it.

    Raises a ValueError if the token does not start with `secret-token:`.

    The `errors` parameter is passed to `.decode` if you do not wish to
    accept invalid UTF-8 sequences.
    """

    if not validate(token, strict=False):
        raise ValueError("Invalid secret token!")

    (_, secret) = token.split(":", maxsplit=1)
    return unquote(secret, encoding="utf-8", errors=errors)


def validate(token: str, *, strict: bool = True) -> bool:
    """
    Validates if a token is a valid secret-token URI.

    Optionally set `strict` to `False` for extremely permissive detection
    """

    if not strict:
        return token.startswith("secret-token:")

    return VALIDATION.match(token) is not None
