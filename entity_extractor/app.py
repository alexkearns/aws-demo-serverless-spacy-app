import json
import logging
import spacy

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    text_to_analyse = body['text']
    logger.info("Analysing: {text}".format(text=text_to_analyse))

    # Use spaCy to extract entities from our text
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text_to_analyse)
    entities = [[e.text, e.label_] for e in doc.ents]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": text_to_analyse,
            "entities": entities
        }),
    }
