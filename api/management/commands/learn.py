import os
import pathlib

import joblib
import pandas
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from stop_words import get_stop_words

from api.models import Document


class Command(BaseCommand):
    help = 'Initializes the `whoosh` index and schema'

    def add_arguments(self, parser):
        parser.add_argument(
            'element', type=str, choices={'category'},
            help='Element to learn from existing data')

    def handle(self, *args, **options):
        if options['element'] == 'category':
            return self.handle_category(**options)

    def handle_category(self, **options):
        columns = 'Category,Document,Content'.split(',')

        documents = Document.objects.filter(method__in={Document.MANUAL, Document.CONFIRMED})
        df = pandas.DataFrame([(d.category.pk, d.path, d.content) for d in documents], columns=columns)

        X_train, X_test, y_train, y_test = train_test_split(df.Content, df.Category, random_state=0)

        vectorizer = TfidfVectorizer(
            sublinear_tf=True,
            min_df=5, norm='l2',
            encoding='utf-8', ngram_range=(1, 2),
            stop_words=get_stop_words('de'))

        X_train = vectorizer.fit_transform(X_train).toarray()
        # noinspection PyTypeChecker
        classifier: LinearSVC = LinearSVC().fit(X_train, y_train)

        if options.get('verbosity') > 1:
            y_pred = classifier.predict(vectorizer.transform(X_test))
            self.stdout.write(self.style.SUCCESS('Classification Report'))
            self.stdout.write(classification_report(y_test, y_pred))

            self.stdout.write(self.style.SUCCESS('Accuracy'))
            print('Accuracy:', accuracy_score(y_test, y_pred))

        store_dir = os.path.join(default_storage.base_location, 'category')
        pathlib.Path(store_dir).mkdir(parents=True, exist_ok=True)
        delattr(vectorizer, 'stop_words_')
        joblib.dump(vectorizer, os.path.join(store_dir, 'vector'))
        joblib.dump(classifier, os.path.join(store_dir, 'model'))

