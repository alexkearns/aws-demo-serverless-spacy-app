FROM public.ecr.aws/lambda/python:3.8

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy across source code
COPY app.py ./
CMD ["app.lambda_handler"]