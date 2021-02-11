import sys, os, json, hashlib
import pytest
import redislite
from unittest.mock import MagicMock, patch

from tests.Mocks import Nlp as NlpMock
sys.modules['spacy'] = NlpMock

from entity_extractor import app

text = "This is Alex's test text"

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    return {
        "body": json.dumps({"text": text})
    }

def test_cache_is_set_on_first_req(apigw_event, mocker):
    redis = redislite.Redis()
    mocker.patch("entity_extractor.app.get_redis", return_value=redis)
    result = app.lambda_handler(apigw_event, "")
    hashed_key = hashlib.md5(text.encode('utf-8')).hexdigest()
    data = json.loads(result["body"])

    # Assert that Redis cache is set, request is successful and cache isn't hit
    assert redis.get(hashed_key) == json.dumps((["Alex", "PERSON"], ["test", "TEST_LABEL"])).encode()
    assert result["statusCode"] == 200
    assert data["cache_hit"] == False

def test_cache_is_hit_on_second_req(apigw_event, mocker):
    redis = redislite.Redis()
    mocker.patch("entity_extractor.app.get_redis", return_value=redis)
    result = app.lambda_handler(apigw_event, "")

    result = app.lambda_handler(apigw_event, "")
    data = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert data["cache_hit"] == True
