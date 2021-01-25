FROM python:3.8

ADD requirements.txt /

ADD assets.py /
ADD indicators.py /
ADD indicators_script.py /
ADD $FILE /

RUN pip install -r requirements.txt

CMD python indicators_script.py -file $FILE -begin_date "$BEGIN" -end_date "$END"
