from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from articleApp.models import Article


# Name of the Elasticsearch index
INDEX = Index('article')


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
   
    id = fields.IntegerField(attr='id')
    fielddata=True

    titre= fields.TextField(
       fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
            
        }
    )
    resume = fields.TextField(
          fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    motsCles = fields.TextField(
         fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    textIntegral = fields.TextField(
         fields={
            'raw': KeywordField(),
        }
    )


  
    urlPdf = fields.TextField(
          fields={
            'raw': KeywordField(),
        }
        
    )

    dateDePublication=fields.DateField(
         fields={
            'raw': {
                'type': 'keyword',
                
            }
        }, )


    # texteIntegral= fields.TextField(
    #     attr='texteIntegral',
    #     fields={
    #         'raw': {
    #             'type': 'keyword',
                
    #         }
    #     },
    # )
    traiter= fields.BooleanField(
        fields={
            'raw': {
                'type': 'keyword',
                
            }
        },
    )


    auteurs = fields.NestedField(
        properties={
        'full_name': fields.TextField(),
        'email': fields.TextField(),
        'institution': fields.ObjectField(
            properties={
            'nom': fields.TextField(),
            'adress': fields.TextField(),
        }),    
    })
    references = fields.NestedField(
        properties={
        'titre': fields.TextField(
            fields={
            'raw': KeywordField(),
        } ),
    })
    

    class Django(object):
        model = Article