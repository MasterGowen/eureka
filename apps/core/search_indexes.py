from haystack import indexes
from .models import Bid


class BidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    product = indexes.CharField(model_attr='product')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Bid

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()  # TODO: filter