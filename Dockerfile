FROM bitnami/python

COPY autoscale.py .

RUN pip install kubernetes

CMD [ "sh" ]