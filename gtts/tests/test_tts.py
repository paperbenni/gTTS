# -*- coding: utf-8 -*-
import os
import pytest
from mock import Mock

from gtts.tts import gTTS, gTTSError


def test_empty_string():
    """Raise AssertionError on empty string"""
    text = ""
    with pytest.raises(AssertionError):
        gTTS(text=text)


def test_no_text_parts(tmp_path):
    """Raises AssertionError on no content to send to API (no text_parts)"""
    text = "                                                                                                          ..,\n"
    with pytest.raises(AssertionError):
        filename = tmp_path / 'no_content.txt'
        tts = gTTS(text=text)
        tts.save(filename)


# %%Test write_to_fp()/save() cases not covered elsewhere in this file

def test_bad_fp_type():
    """Raise TypeError if fp is not a file-like object (no .write())"""
    # Create gTTS and save
    tts = gTTS(text='test')
    with pytest.raises(TypeError):
        tts.write_to_fp(5)


def test_save(tmp_path):
    """Save .mp3 file successfully"""
    filename = tmp_path / 'save.mp3'
    # Create gTTS and save
    tts = gTTS(text='test')
    tts.save(filename)

    # Check if file created is > 2k
    assert filename.stat().st_size > 2000


def test_msg():
    """Test gTTsError internal exception handling
    Set exception message successfully"""
    error1 = gTTSError('test')
    assert 'test' == error1.msg

    error2 = gTTSError()
    assert error2.msg is None


def test_infer_msg():
    """Infer message sucessfully based on context"""

    # 403
    tts403 = Mock()
    response403 = Mock(status_code=403, reason='aaa')
    error403 = gTTSError(tts=tts403, response=response403)
    assert error403.msg == "403 (aaa) from TTS API. Probable cause: Bad token or upstream API changes"

    # 404 (and not lang_check)
    tts404 = Mock(lang='xx', lang_check=False)
    response404 = Mock(status_code=404, reason='bbb')
    error404 = gTTSError(tts=tts404, response=response404)
    assert error404.msg == "404 (bbb) from TTS API. Probable cause: Unsupported language 'xx'"

    # >= 500
    tts500 = Mock()
    response500 = Mock(status_code=500, reason='ccc')
    error500 = gTTSError(tts=tts500, response=response500)
    assert error500.msg == "500 (ccc) from TTS API. Probable cause: Uptream API error. Try again later."

    # Unknown (ex. 100)
    tts100 = Mock()
    response100 = Mock(status_code=100, reason='ddd')
    error100 = gTTSError(tts=tts100, response=response100)
    assert error100.msg == "100 (ddd) from TTS API. Probable cause: Unknown"


def test_WebRequest(tmp_path):
    """Test Web Requests"""

    text = "Lorem ipsum"

    """Raise gTTSError on unsupported language (without language check)"""
    lang = 'xx'
    check = False

    with pytest.raises(gTTSError):
        filename = tmp_path / 'xx.txt'
        # Create gTTS
        tts = gTTS(text=text, lang=lang, lang_check=check)
        tts.save(filename)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
