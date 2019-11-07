from setuptools import setup
from codecs import open

exec(open('gtts/version.py').read())

setup(
    version=0.1,   # type: ignore # noqa: F821
    test_suite='gtts.tests',
)
