#!/bin/csh -f
#
# Install python3 and packages needed
# Used for configuring new AWS instances running Ubuntu
#

# Update apt environ
sudo apt-get update

# Install and start mysql
sudo apt-get install mysql-server
sudo service mysql start

# Install Python 3
sudo apt-get install python3.6

# Install packages
sudo apt install python3-pip
sudo pip3 install pandas
sudo pip3 install tensorflow
sudo pip3 install sklearn
sudo pip3 install glove==1.0.0
sudo pip3 install nltk
sudo pip3 install keras
sudo pip3 install glove_python
sudo pip3 install matplotlib
