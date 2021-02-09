# spacy-serverless-app
A serverless application built with AWS SAM, focused around using spaCy to perform NLP on given text.

The general gist of this application is to provide the following functionality:
- Use API gateway to expose a Lambda function
- The Lambda function performs named entity recognition on the text submitted via API gateway using spaCy
- The Lambda function makes use of ElastiCache in order to reduce the compute required when requests are the same