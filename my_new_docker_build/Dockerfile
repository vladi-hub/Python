FROM python:3

ADD ./my_script.py /
ADD ./sort_script.py /

RUN pip install --upgrade pip

RUN pip install pystrich
RUN pip install Tensorflow
RUN pip install Keras
RUN pip install Pandas
RUN pip install Numpy
RUN pip install h5py
RUN pip install SciPy  
RUN pip install scikit-learn

CMD [ "python", "./my_script.py" ]
