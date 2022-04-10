# patentclass
Machine Learning for Patent Classification

This project publishes an multilabel clssification model developed for Penn States STAT 581 course.
The data set draws from the USPTO's Patent Grant publications https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2018/
These weekly XML files provide the patent description and abstract with several IPC codes assigned to each patent. A single
sample week of the extracted data is available in the data folder.
A MySQL database is used to stage the text and IPC assigments.
The multilabel model is estimated using Tensorflow and Keras and needs a server with 80GB of memory to estimate.
The study used an AWS r5a.4xlarge with 16 CPUs and 128GB memory.

The project's data extraction python (get_red_book.py) was updated for pulling 2021 versions of this publication.
