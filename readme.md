# OpenGov's Public Consultations Analysis Code Repository

Code repository for my Master Thesis in MSc. in  Business Analytics, AUEB, titled "Impact Analysis of Greece's OpenGov Public Consultation Contributions on Final Legislation"

The main goal of the thesis is to extract initial article legislation proposals, public consultation contributions and the final version of the legislative article, as voted by the Hellenic Parliament, in order to asses public consultation feedback's impact.

The relevant data is extract from
-  [OpenGov's](http://www.opengov.gr/home/category/consultations "OpenGov's Website") where public consultations are hosted
- PDF files of Voted Laws

Extracted data is held in a local relational `sqlite` database file.

## Database Schema

## Repository Structure

**config.ini** holds `sqlite`'s database file configurations for different scenarios

### data_objects

Holds `sqlalchemy`'s ORM classes for the main extracted entities

### notesbooks

Notebooks contain the main extraction and data cleaning scripts required for arriving at the relational schema.

*Why Notebooks? Iterative processes such as extraction and data cleansing are done more efficiently using notebooks files (`.ipynb`) due to not losing state when exceptions occur. This allows quicker debugging, since the previous state of the program is not lost.*


### scripts

One-off scripts desinged to do a specific job, usually explained sufficiently by the script title

### sql_migrations

Schema changes after the initial database creation with SQLAlchemy's ORM

### sql_queries

Stand-alone SQL queries

### tests

### text_utils

Classes and functions related to text processing