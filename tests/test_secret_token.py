"""
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

import pytest

from secret_token import VALID_CHARS, decode, encode, validate


@pytest.mark.parametrize(
    ("strict",),
    [
        (True,),
        (False,),
    ],
    ids=["Strict", "Not Strict"],
)
class TestValidate:
    def test_example(self, strict):
        token = r"secret-token:E92FB7EB-D882-47A4-A265-A0B6135DC842%20foo"
        expected = True
        result = validate(token, strict=strict)
        assert result == expected

    def test_invalid(self, strict):
        token = "banana"
        expected = False
        result = validate(token, strict=strict)
        assert result == expected

    def test_every_char(self, strict):
        token = "secret-token:aA%20" + "".join(VALID_CHARS)
        expected = True
        result = validate(token, strict=strict)
        assert result == expected

    def test_accidentally_invalid(self, strict):
        token = "secret-token:domain/authtype/code"
        expected = not strict
        result = validate(token, strict=strict)
        assert result == expected


class TestEncode:
    def test_example(self):
        secret = "E92FB7EB-D882-47A4-A265-A0B6135DC842 foo"
        expected = r"secret-token:E92FB7EB-D882-47A4-A265-A0B6135DC842%20foo"
        result = encode(secret)

        assert result == expected
        assert decode(result) == secret
        assert validate(result, strict=True)

    def test_unicode(self):
        secret = "/El Niño/"
        expected = r"secret-token:%2FEl%20Ni%C3%B1o%2F"
        result = encode(secret)

        assert result == expected
        assert decode(result) == secret
        assert validate(result, strict=True)

    def test_twice(self):
        secret = "secret-token:domain%2Fauthtype%2Fcode"
        expected = r"secret-token:secret-token%3Adomain%252Fauthtype%252Fcode"
        result = encode(secret)

        assert result == expected
        assert decode(result) == secret
        assert validate(result, strict=True)


class TestDecode:
    def test_example(self):
        token = r"secret-token:E92FB7EB-D882-47A4-A265-A0B6135DC842%20foo"
        expected = "E92FB7EB-D882-47A4-A265-A0B6135DC842 foo"
        result = decode(token)

        assert result == expected

    def test_unicode(self):
        token = r"secret-token:%2FEl%20Ni%C3%B1o%2F"
        expected = "/El Niño/"
        result = decode(token)

        assert result == expected

    def test_invalid(self):
        token = r"banana"
        with pytest.raises(ValueError):
            decode(token)

    def test_every_char(self):
        token = r"secret-token:aA%20" + "".join(VALID_CHARS)
        expected = "aA " + "".join(VALID_CHARS)
        result = decode(token)

        assert result == expected

    def test_slightly_invalid(self):
        token = r"secret-token:domain/authtype/code"
        expected = "domain/authtype/code"
        result = decode(token)

        assert result == expected

    def test_rather_more_invalid(self):
        token = r"secret-token:Honestly: you can put anything in here! %%%\" 🤪"
        expected = r"Honestly: you can put anything in here! %%%\" 🤪"
        result = decode(token)

        assert result == expected

    def test_invalid_unicode(self):
        token = r"secret-token:%ae"
        expected = "�"
        result = decode(token)

        assert result == expected
