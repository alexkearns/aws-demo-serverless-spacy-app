FROM public.ecr.aws/lambda/python:3.8
COPY app.py requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
CMD ["app.lambda_handler"]