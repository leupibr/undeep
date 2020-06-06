import datetime
import hashlib
import logging
import os
import subprocess

import joblib
import pandas
from django.core.files.storage import default_storage
from django.db import models
from whoosh.index import open_dir

from api.utils import hsize, find_dates


class Category(models.Model):
    """Represents a base category"""
    name = models.CharField(max_length=20, null=False, blank=False, unique=True)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<Category {self.name!r}>'


class Document(models.Model):
    """Represents a stored document with some additional meta information"""
    path = models.CharField(max_length=200, null=False, blank=False, unique=True)
    checksum = models.CharField(max_length=64, null=False, blank=False, unique=True)
    name = models.CharField(max_length=200, blank=False)

    size = models.IntegerField(null=True)

    uploaded = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)
    date = models.DateField()

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    MANUAL = 0
    AUTO = 1
    CONFIRMED = 2
    METHOD_CHOICES = ((MANUAL, 'Manual'), (AUTO, 'Automatic'), (CONFIRMED, 'Confirmed'))
    method = models.IntegerField(choices=METHOD_CHOICES, null=True)

    @classmethod
    def create(cls, path, **kwargs):
        instance = cls(path=path, **kwargs)
        instance.checksum = Document._build_checksum(path)
        instance.size = Document._get_size(path)
        if not kwargs.get('date'):
            instance.date = Document.find_date(instance)
        return instance

    @staticmethod
    def index_multiple(documents):
        index_dir = os.path.join(default_storage.base_location, 'index')
        if not os.path.exists(index_dir):
            raise FileExistsError()

        ix = open_dir(index_dir)
        writer = ix.writer()
        for doc in documents:
            doc.index_write(writer)
        writer.commit()

    @staticmethod
    def predict_multiple(documents):
        store_dir = os.path.join(default_storage.base_location, 'category')
        vector_path = os.path.join(store_dir, 'vector')
        if not os.path.exists(vector_path):
            logging.warning('No vector for categories stored, skipping categorization')
            return
        model_path = os.path.join(store_dir, 'model')
        if not os.path.exists(model_path):
            logging.warning('No model for categories stored, skipping categorization')
            return

        vectorizer = joblib.load(vector_path)
        classifier = joblib.load(model_path)
        df = pandas.DataFrame([(None, d, d.content) for d in documents], columns='Category,Document,Content'.split(','))
        X_uploaded = vectorizer.transform(df.Content)
        df.Category = classifier.predict(X_uploaded)
        for index, item in df.iterrows():
            item.Document.category = Category.objects.get(name=item.Category)
            item.Document.method = Document.AUTO

    @staticmethod
    def _build_checksum(path):
        path = os.path.join(default_storage.base_location, path)
        return hashlib.sha3_256(open(path, 'rb').read()).hexdigest()

    @staticmethod
    def _get_size(path):
        path = os.path.join(default_storage.base_location, path)
        return os.stat(path).st_size

    @property
    def content(self):
        return subprocess.check_output(['pdftotext', self.get_storage_path(), '-']).decode('utf-8')

    @property
    def hsize(self):
        if not self.size:
            return '0 B'
        return hsize(self.size)

    def get_storage_path(self):
        return os.path.join(default_storage.base_location, self.path)

    def index(self, *fields):
        index_dir = os.path.join(default_storage.base_location, 'index')
        if not os.path.exists(index_dir):
            raise FileExistsError()

        ix = open_dir(index_dir)
        writer = ix.writer()
        self.index_write(writer, *fields)
        writer.commit()

    def de_index(self):
        index_dir = os.path.join(default_storage.base_location, 'index')
        if not os.path.exists(index_dir):
            raise FileExistsError()
        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.delete_by_term('path', self.path)
        writer.commit()

    def index_write(self, writer, *fields):
        fields = fields or ['name', 'content', 'date', 'uploaded', 'category']

        doc = dict(path=self.path)
        if 'name' in fields:
            doc['name'] = self.name
        if 'content' in fields:
            doc['content'] = self.content
        if 'date' in fields:
            doc['date'] = datetime.datetime(self.date.year, self.date.month, self.date.day)
        if 'uploaded' in fields:
            doc['uploaded'] = self.uploaded
        if 'category' in fields:
            doc['category'] = self.category.name if self.category else None
        writer.update_document(**doc)

    def predict(self):
        store_dir = os.path.join(default_storage.base_location, 'category')
        vector_path = os.path.join(store_dir, 'vector')
        if not os.path.exists(vector_path):
            logging.warning('No vector for categories stored, skipping categorization')
            return
        model_path = os.path.join(store_dir, 'model')
        if not os.path.exists(model_path):
            logging.warning('No model for categories stored, skipping categorization')
            return

        vectorizer = joblib.load(vector_path)
        classifier = joblib.load(model_path)

        X_uploaded = vectorizer.transform([self.content])
        category = classifier.predict(X_uploaded)
        self.category = Category.objects.get(name=category[0])
        self.method = Document.AUTO

    def find_dates(self, lower_bound=None, upper_bound=None):
        return find_dates(self.content, lower_bound, upper_bound)

    def find_date(self, lower_bound=None, upper_bound=None):
        in_content = self.find_dates(lower_bound, upper_bound)
        if not in_content:
            return self.uploaded

        # extract closest date to upload date
        in_content = [d.replace(tzinfo=datetime.timezone.utc) for d in in_content]
        found_dates = [(date, (self.uploaded - date).total_seconds()) for date in in_content]
        return sorted(found_dates, key=lambda x: x[1])[0][0]

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<Document {self.name!r}>'


