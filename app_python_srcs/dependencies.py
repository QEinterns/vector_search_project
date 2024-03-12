from PyPDF2 import PdfReader
import nltk
nltk.download('punkt')
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import timedelta
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
import ast
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from json import JSONEncoder
import logging