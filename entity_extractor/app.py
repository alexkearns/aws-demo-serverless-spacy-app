import json
import hashlib
import os
import logging
import spacy
import redis

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_redis():
  redis_config = {
    "host": os.environ['REDIS_ENDPOINT'],
    "port": 6379,
    "db": 0,
    "ssl": True,
    "ssl_cert_reqs": None
  }
  return redis.Redis(**redis_config)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    text_to_analyse = body['text']
    logger.info("Analysing: {text}".format(text=text_to_analyse))

    # Set up Redis configuration, check cache
    r = get_redis()
    hash_text = hashlib.md5(text_to_analyse.encode('utf-8')).hexdigest()
    entities = r.get(hash_text)
    cache_hit = True

    if entities == None:
        # Use spaCy to extract entities from our text
        nlp = spacy.load("en_core_web_sm")
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
