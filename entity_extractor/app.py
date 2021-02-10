import json
import hashlib
import os
import logging
import spacy
import redis

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CacheManager:
    def __init__(self, cache_driver):
        self.cache = cache_driver

class NlpManager:
    def __init__(self, nlp_driver):
        self.nlp = nlp_driver

"""
Expose method for API gateway to proxy to
- Inject module dependencies
- Pass on event and context
"""
def lambda_handler(event, context):
    cache_driver = redis
    nlp_driver = spacy
    return handle(event, context, cache_driver, nlp_driver)

def handle(event, context, cache_driver, nlp_driver):
    body = json.loads(event['body'])
    text_to_analyse = body['text']
    logger.info("Analysing: {text}".format(text=text_to_analyse))

    # Set up Redis configuration, check cache
    cache = CacheManager(cache_driver).cache
    r = cache.Redis(host=os.environ['REDIS_ENDPOINT'], port=6379, db=0,
                    ssl=True, ssl_cert_reqs=None)
    hash_text = hashlib.md5(text_to_analyse.encode('utf-8')).hexdigest()
    entities = r.get(hash_text)
    cache_hit = True

    if entities == None:
        # Use spaCy to extract entities from our text
        nlp_manager = NlpManager(nlp_driver).nlp
        nlp = nlp_manager.load("en_core_web_sm")
        doc = nlp(text_to_analyse)
        entities = [[e.text, e.label_] for e in doc.ents]
        cache_hit = False
        # Update cache, expires in 1 hour
        r.set(hash_text, json.dumps(entities), ex=3600)
    else:
        # Entities stored in JSON in cache
        entities = json.loads(entities)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": text_to_analyse,
            "entities": entities,
            "cache_hit": cache_hit
        }),
    }
