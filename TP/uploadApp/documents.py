from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from articleApp.models import Article

# Name of the Elasticsearch index
INDEX = Index('article2')

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=[ "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@INDEX.doc_type
class ArticleDocument(Document):
    """Article Elasticsearch document."""
    id = fields.IntegerField(attr='id')
    fielddata=True
    titre= fields.TextField(
        fielddata=True,
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    resume = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    mots_cles = fields.TextField(
        analyzer=html_strip,
        
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    texte_integral = fields.TextField(
        analyzer=html_strip,
       
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    url_pdf = fields.TextField(
        analyzer=html_strip,
       
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )


 
    references = fields.TextField(
        attr='references_indexing',
        analyzer=html_strip,
        
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    auteurs= fields.TextField(
        attr='Auteurs_indexing',
        analyzer=html_strip,
        
        fields={
            'raw': fields.TextField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    class Django(object):
        """Inner nested class Django."""
        model = Article # The model associate with this Document