from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.constants import (
   
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from .documents import ArticleDocument
from .serializers import ArticleDocumentSerializer


class ArticleDocumentView(BaseDocumentViewSet):
    

    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    # # Define search fields
    # search_fields = (
    #     'titre',
    #     'resume',
    #     'texteIntegral',
    #     'motsCles',
    #     'references',
    #     'auteurs',
    #     'traier',
    #     )

    # # Define filter fields
    # filter_fields = {
    #     'traiter':'traiter.raw',
    #     'dateDePublication':'dateDePublication',

    #     'motsCles': {
    #         'field': 'motsCles.raw',
    #         'suggesters': [
    #             SUGGESTER_COMPLETION,
    #         ],
    #         # 'lookups': [
    #         #     LOOKUP_FILTER_TERMS,
    #         #     LOOKUP_FILTER_PREFIX,
    #         #     LOOKUP_FILTER_WILDCARD,
    #         #     LOOKUP_QUERY_IN,
    #         # ],
    #     },

    #     'auteurs': 'auteurs.raw',
        
    # }
    # nested_filter_fields = {
    #     'references': {
    #         'field': 'continent.country.name.raw',
    #         'path': 'continent.country',
    #     },
    #     'continent_country_city': {
    #         'field': 'continent.country.city.name.raw',
    #         'path': 'continent.country.city',
    #     },



    # }

    # # Define ordering fields
    # ordering_fields = {
    #     # 'dateDePublication':'dateDePublication',
    #     'id': 'id',
    # }

    # # Specify default ordering
    # ordering = ('id')







    # Define search fields
    search_fields = (
        'titre',
        'resume',
        'motsCles',
        'texteIntegral',
    )
    search_nested_fields = {
        'references': {
            'path': 'references',
            'fields': ['titre'],
        },
        'auteurs': {
            'path': 'auteurs',
            'fields': ['full_name','email','institution.nom','institution.adress'],
        },
    }

    # Define filtering fields
    filter_fields = {
        'id': None,
        'traiter': 'traiter.raw',
        'motsCles':'motsCles.raw',
        'auteurs.institution.nom': 'auteurs.institution.nom.raw',
        'auteurs.nom': 'auteurs.full_name.raw',
        # 'references':'references.titre.raw',
    }
    
    # Nested filtering fields
    # nested_filter_fields = {
    #     'references': {
    #         'field': 'titre.raw',
    #         'path': 'references',
            
    #     },
    #     'auteursName':{
    #         'field': 'full_name.raw',
    #         'path': 'auteurs',
    #     },
    # }

    nested_filter_fields = {
        'auteurs': ['full_name', 'institution.nom'],
    }




    ordering_fields ={
        'id': 'id',

    }

    # Specify default ordering
    ordering = ('id')

    # Suggester fields
    suggester_fields = {
        'titre_suggest': {
            'field': 'titre.suggest',
            'suggesters': [SUGGESTER_COMPLETION],
        },
        'resume_suggest': {
            'field': 'resume.suggest',
            'suggesters': [SUGGESTER_COMPLETION],
        },
        'motsCles_suggest': {
            'field': 'motsCles.suggest',
            'suggesters': [SUGGESTER_COMPLETION],
        },
    }