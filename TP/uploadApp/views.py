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
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from .documents import ArticleDocument
from .serializers import ArticleDocumentSerializer




class ArticleDocumentView(BaseDocumentViewSet):
    """The ArticleDocument view."""

    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # Define search fields
    search_fields = (
        'titre',
        'resume',
        'texte_integral',
        'mots_cles',
        'URL_pdf',
        'references',
        'auteurs',
    )

    # Define filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            # Note, that we limit the lookups of id field in this example,
            # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'titre': 'titre.raw',
        'mots_cles': {
            'field': 'mots_cles',
            # Note, that we limit the lookups of `tags` field in
            # this example, to `terms, `prefix`, `wildcard`, `in` and
            # `exclude` filters.
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
        
    }


    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'titre': 'titre.raw',
       
    }
    # Specify default ordering
    ordering = ('id', 'titre',)



import requests
import os
import fitz  # PyMuPDF
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # For simplicity, disabling CSRF protection
from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import re
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from articleApp.models import Reference, Institution, Auteur, Article

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
REDIRECT_URI = 'https://localhost/'


# Function to authenticate and get drive service
def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']

    flow = InstalledAppFlow.from_client_secrets_file(
        'uploadApp/credentials.json', 
        scopes=SCOPES
    )

    creds = flow.run_local_server(port=0)
    
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service


# Function to extract folder ID from the folder link
def extract_folder_id(folder_link):
    # Check if the link contains '/folders/' (typical for folder links)
    if '/folders/' in folder_link:
        # Split the link by '/'
        split_link = folder_link.split('/')
        # The folder ID is typically after the '/folders/' segment
        # Find the index of '/folders/' in the link
        index = split_link.index('folders')
        # Extract the folder ID from the next segment
        folder_id = split_link[index + 1]
        folder_id = folder_id.split('?')[0]
        return folder_id
    else:
        return None  


# Function to retrieve PDF links from a specific folder in Google Drive
def get_pdf_links_from_folder(folder_id, drive_service):
    # Retrieve files from the folder
    response = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType='application/pdf'",fields='files(webViewLink)').execute()
    
    pdf_links = [file['webViewLink'] for file in response.get('files', [])]
    return pdf_links

#Function to extract file ID from the file link
def extract_file_id_from_url(pdf_link):
    start_idx = pdf_link.find('/d/') + len('/d/')
    end_idx = pdf_link.find('/view')
    if start_idx != -1 and end_idx != -1:
        file_id = pdf_link[start_idx:end_idx]
        return file_id
    else:
        return None

def extract_text_from_pdf(pdf_link, drive_service):
    # Extract the file ID from the PDF link
    file_id = extract_file_id_from_url(pdf_link)  # Extracting the file ID from the link
    
    # Retrieve PDF file content from Google Drive using file_id
    pdf_content = drive_service.files().get_media(fileId=file_id).execute()

    text=''
    elements=''
    try:
        pdf_document = fitz.open(stream=pdf_content)
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)

            # Extract only text elements from the page
            page_text = page.get_text("text")
            if (page_num==0):
                
                client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
                completion = client.chat.completions.create(
                   model="gpt-3.5-turbo",
                   messages=[
                     {"role": "system", "content": "Extract the following information exactly as it appears in the text:1. Title, 2. Authors with emails and institutions: elements(author's full name, email and all the information of the institution to which he belongs) separated with ',' and separate each author from the other with'-' , 3. Abstract, 4. Keywords: separated with ',', 5. Rest of the text: exactly as it is in the text, after excluding title, authors, abstract, and keywords. Make sure to include the content starting with 'Introduction' in Rest of the text."},
                     {"role": "user", "content": page_text }
                    ]
                )
                elements = completion.choices[0].message.content
                elements = elements.replace("\n", " ")
                
                
                #elements = '1. Title: AI Model for Computer games based on Case Based Reasoning and AI Planning  2. Authors with emails and institutions:  - Vlado Menkovski, vmen@ait.edu.gr, Athens Information Technology  - Dimitrios Metafas, dmeta@ait.edu.gr, Athens Information Technology  3. Institutions with addresses:  - Athens Information Technology, 0.8km Markopoulou Ave., Peania, 19002, Greece  4. Abstract: Making efficient AI models for games with imperfect information can be a particular challenge. Considering the large number of possible moves and the incorporated uncertainties building game trees for these games becomes very difficult due to the exponential growth of the number of nodes at each level. This effort is focused on presenting a method of combined Case Based Reasoning (CBR) with AI Planning which drastically reduces the size of game trees. Instead of looking at all possible combinations we can focus only on the moves that lead us to specific strategies in effect discarding meaningless moves. These strategies are selected by finding similarities to cases in the CBR database. The strategies are formed by a set of desired goals. The AI planning is responsible for creating a plan to reach these goals. The plan is basically a set of moves that brings the player to this goal. By following these steps and not regarding the vast number of other possible moves the model develops Game Trees which grows slower so they can be built with more feature moves restricted by the same amount of memory.   5. Keywords: Game AI, Case Based Reasoning, AI Planning, Game Trees  6. Rest of the text:  Introduction The goal of this effort is to explore a model for design and implementation of an AI agent for turn based games. This model provides for building more capable computer opponents that rely on strategies that closely resemble human approach in solving problems opposed to classical computational centric heuristics in game AI. In this manner the computational resources can be focused on more sensible strategies for the game play.   With the advancement in computer hardware increasingly more computing power is left for executing AI algorithms in games. In the past AI in games was mainly a cheating set of instructions that simulated the increasing difficulty in the game environment so that the player had the illusion of real counterpart. Improvement in available memory and processing power allows implementation of more intelligent algorithms for building the game environment as well as direct interaction with the human players.    In this particular research the emphasis is put on the interaction between the AI agent and a computer player in the realm of the game rules. It is particularly focused on turn based games that have the elements of uncertainty like dice or concealed information. At the beginning a description of Game AI algorithms are given; such as Game Trees and Minimax. The following section describes an approach of using AI Planning to improve building Game Trees in games with imperfect information where Game Trees tend to be very large with high growth ratio. Section 4 discusses another approach that provides a significant reduction to the number of considered moves in order to find the favorable strategy of the AI player. This approach uses AI Planning techniques and Case Base Reasoning (CBR) to plan for different scenarios in predetermined strategies which would be analogous to human player experience in the particular game. The CBR database illustrates a set of past experiences for the AI problem and the AI Planning illustrates the procedure to deal with the given situation in the game. In the next two sections implementations and evaluations of both approaches are given. The AI Planning approach is implemented with the Tic-tac-toe game and the combined AI Planning and CBR approach is implemented with a model for the Monopoly game. The last part contains conclusions and future work ideas.  2. Game Trees and Minimax  Game Trees are common model for evaluating how different combinations of moves from the player and his opponents will affect the future position of the player and eventually the end result of the game. An algorithm that decides on the next move by evaluating the results from the built Game Tree is minimax [1]. Minimax assumes that the player at hand will always choose the best possible move for him, in other words the player will try to select the move that maximizes the result of the evaluation function over the game state. So basically the player at hand needs to choose the best move overall while taking into account that the next player(s) will try to do the same thing. Minimax tries to maximize the minimum gain. Minimax can be applied to multiple [1]'
                #Define regular expressions for extracting the desired sections
                title_pattern = re.compile(r'Title: (.+?)\s+\d+\. Authors', re.DOTALL)
                authors_pattern = re.compile(r'2\. Authors with emails and institutions:(.*?)3\. Abstract:', re.DOTALL)
                abstract_pattern = re.compile(r'3\. Abstract: (.+?)\s+\d+\. Keywords', re.DOTALL)
                keywords_pattern = re.compile(r'4\. Keywords: (.+?)\s+\d+\. Rest of the text', re.DOTALL)
                rest_of_text_pattern = re.compile(r'5\. Rest of the text: (.+)', re.DOTALL)

                # Extract the sections using the regular expressions
                title_match = title_pattern.search(elements)
                authors_match = authors_pattern.search(elements)
                abstract_match = abstract_pattern.search(elements)
                keywords_match = keywords_pattern.search(elements)
                rest_of_text_match = rest_of_text_pattern.search(elements)


                # Check if matches are found before extracting
                title = title_match.group(1) if title_match else None
                authors = authors_match.group(1).strip() if authors_match else None
                abstract = abstract_match.group(1) if abstract_match else None
                keywords = keywords_match.group(1) if keywords_match else None
                rest_of_text = rest_of_text_match.group(1) if rest_of_text_match else None

               
            else:
                text += page_text
        pdf_document.close() 
        text = text.replace("\n", " ")
        last_references_pattern = re.compile(r'(?i)references(.*)$')
        last_references_match = last_references_pattern.search(text)
        references = last_references_match.group(1).strip() if last_references_match else None
        text = text.replace(last_references_match.group(0), '')

        text = rest_of_text + text

    except Exception as e:
        text = f"Failed to extract text: {str(e)}" 

    return title, authors, abstract, keywords, text, references


def get_authors_list(authors):
    authors_data = authors.split('-')
    author_pattern = re.compile(r'\s*(\w+\s+\w+),\s+(\S+),\s+(.+)')
    # Initialize an empty list to store author dictionaries
    authors_list = []
    # Iterate through matches and create author dictionaries
    for author_info in authors_data:
      # Find all matches in the author_info
      author_matches = author_pattern.findall(author_info)

      # Iterate through matches and create author dictionaries
      for match in author_matches:
        full_name, email, institution = match
        institution = institution.strip(" ")

        # Create the author dictionary and append it to the list
        author_dict = {
          'full_name': full_name,
          'email': email,
          'institution': institution,
        }
        authors_list.append(author_dict)
    return authors_list

'''
def get_institutions_list(institutions):
    institutions_data = institutions.split('-')
    institution_pattern = re.compile(r'\s*(.+?),\s*(.+)')

    # Initialize an empty list to store institution dictionaries
    institutions_list = []

    # Iterate through institution information and create institution dictionaries
    for institution_info in institutions_data:
      # Find all matches in the institution_info
      institution_matches = institution_pattern.findall(institution_info)

      # Iterate through matches and create institution dictionaries
      for match in institution_matches:
        nom, adress = match
        nom = nom.strip(" ")
        # Create the institution dictionary and append it to the list
        institution_dict = {
            'nom': nom,
            'adress': adress,
        }
        institutions_list.append(institution_dict)
    return institutions_list
'''


def get_references_list(references):
    reference_pattern = re.compile(r'\[(\d+)\]\s*((?:(?!\[\d+\]).)*)', re.DOTALL)
    
    # Find all matches
    matches = reference_pattern.findall(references)

    # Store references in a list of dictionaries
    references_list = [{'titre': match[1].strip()} for match in matches]
    
    return references_list

'''
def create_references(references_list):
    reference_objects = []
    for reference_data in references_list:
        reference_objects.append(Reference.objects.get_or_create(titre=reference_data['titre']))
    return reference_objects


def create_institutions(institutions_list):
    institution_objects = []
    for institution_data in institutions_list:
        institution_objects.append(Institution.objects.get_or_create(nom=institution_data['nom'], adress=institution_data['adress']))
    return institution_objects



def add_authors(authors_list, article):
    
    for author_data in authors_list:
        institution_pattern = re.compile(r'\s*(.+?),\s*(.+)')
        match = institution_pattern.findall(author_data['institution'])
        nom, adress = match
        nom = nom.strip(" ")
        institution = Institution.objects.get_or_create(nom=nom, adress=adress)
        author_objects.append(Auteur.objects.get_or_create(full_name=author_data['full_name'], email=author_data['email'], institution=institution))
    return author_objects
'''


@csrf_exempt  # Disable CSRF protection for demonstration purposes
def process_folder_link(request):
    if request.method == 'POST':

        # drive_service = get_drive_service()

        # folder_link = request.POST.get('folder_link', '')  # Get the folder link from the POST request
        
        # folder_id = extract_folder_id(folder_link) # Extract the folder ID from the link 
        # if folder_id is None:
        #     return JsonResponse({'error': 'Invalid folder link provided'})
        
        # pdf_links = get_pdf_links_from_folder(folder_id, drive_service) #Get the files' links from the folder ID 
        # if pdf_links is None:
        #     return JsonResponse({'error': 'Cannot extract links from folder'})
        # processed_pdfs = []

        # for pdf_link in pdf_links: #Processing each link
            '''
            title, authors, abstract, keywords, text, references = extract_text_from_pdf(pdf_link, drive_service) #Extracting text from the pdf file
            if title is None:
              return JsonResponse({'error': 'Error while extracting the title'})
            if authors is None:
              return JsonResponse({'error': 'Error while extracting the authors'})
            if abstract is None:
              return JsonResponse({'error': 'Error while extracting the abstract'}) 
            if text is None:
              return JsonResponse({'error': 'Error while extracting the text'}) 
            if keywords is None:
              return JsonResponse({'error': 'Error while extracting the keywords'}) 
            if references is None:
              return JsonResponse({'error': 'Error while extracting the references'})   

            authors_list = get_authors_list(authors)
            #institutions_list = get_institutions_list(institutions)
            references_list = get_references_list(references)
            '''

            
            pdf_link = "https://drive.google.com/file/d/1At7MFEUfW1OmDsapLNK4EXiOhYW74xrI/view?usp=drivesdk"
            title = "Semantic Analysis and Classification of Emails through Informative Selection of Features and Ensemble AI Model"
            authors_list = [
                {
                    "full_name": "Shivangi Sachan",
                    "email": "mcs21025@iiitl.ac.in",
                    "institution": "Department of CSE, IIIT Lucknow, Lucknow, UP, India"
                },
                {
                    "full_name": "Khushbu Doulani",
                    "email": "khushidoulani@gmail.com",
                    "institution": "Vardhaman College of Engineering, Hyderabad, India"
                },
                {
                    "full_name": "Mainak Adhikari",
                    "email": "mainak.ism@gmail.com",
                    "institution": "Department of CSE, IIIT Lucknow, UP, India"
                }
            ]

            abstract = "The emergence of novel types of communication, such as email, has been brought on by the development of the internet, which radically concentrated the way in that individuals communicate socially and with one another. It is now establishing itself as a crucial aspect of the communication network which has been adopted by a variety of commercial enterprises such as retail outlets. So in this research paper, we have built a unique spam-detection methodology based on email-body sentiment analysis."

            keywords = "Dataset, KNN, Gaussian Naive Bayes, LSTM, SVM, Bidirectional LSTM, GRU, Word-Embeddings, CNN"
            
            references_list = [
                {
                    "titre": "Rayan Salah Hag Ali and Neamat El Gayar. 2019. Sentiment analysis using unla- beled email data. In 2019 International Conference on Computational Intelligence and Knowledge Economy (ICCIKE). IEEE, 328–333."
                },
                {
                    "titre": "Ali Shafigh Aski and Navid Khalilzadeh Sourati. 2016. Proposed efficient algo- rithm to filter spam using machine learning techniques. Pacific Science Review A: Natural Science and Engineering 18, 2 (2016), 145–149."
                },
                {
                    "titre": "Huwaida T Elshoush and Esraa A Dinar. 2019. Using adaboost and stochastic gradient descent (sgd) algorithms with R and orange software for filtering e-mail spam. In 2019 11th Computer Science and Electronic Engineering (CEEC). IEEE, 41–46."
                },
                {
                    "titre": "Weimiao Feng, Jianguo Sun, Liguo Zhang, Cuiling Cao, and Qing Yang. 2016. A support vector machine based naive Bayes algorithm for spam filtering. In 2016 IEEE 35th International Performance Computing and Communications Conference (IPCCC). IEEE, 1–8."
                },
                {
                    "titre": "Pranjul Garg and Nancy Girdhar. 2021. A Systematic Review on Spam Filtering Techniques based on Natural Language Processing Framework. In 2021 11th Inter- national Conference on Cloud Computing, Data Science & Engineering (Confluence). IEEE, 30–35."
                },
                {
                    "titre": "Adam Kavon Ghazi-Tehrani and Henry N Pontell. 2021. Phishing evolves: Ana- lyzing the enduring cybercrime. Victims & Offenders 16, 3 (2021), 316–342."
                },
                {
                    "titre": "Radicati Group et al. 2015. Email Statistics Report 2015–2019. Radicati Group. Accessed August 13 (2015), 2019."
                },
                {
                    "titre": "Maryam Hina, Mohsin Ali, and Javed. 2021. Sefaced: Semantic-based forensic analysis and classification of e-mail data using deep learning. IEEE Access 9 (2021), 98398–98411."
                },
                {
                    "titre": "Maryam Hina, Mohsin Ali, Abdul Rehman Javed, Fahad Ghabban, Liaqat Ali Khan, and Zunera Jalil. 2021. Sefaced: Semantic-based forensic analysis and classification of e-mail data using deep learning. IEEE Access 9 (2021), 98398– 98411."
                },
                {
                    "titre": "Weicong Kong, Zhao Yang Dong, Youwei Jia, David J Hill, Yan Xu, and Yuan Zhang. 2017. Short-term residential load forecasting based on LSTM recurrent neural network. IEEE transactions on smart grid 10, 1 (2017), 841–851."
                },
                {
                    "titre": "T Kumaresan and C Palanisamy. 2017. E-mail spam classification using S-cuckoo search and support vector machine. International Journal of Bio-Inspired Compu- tation 9, 3 (2017), 142–156."
                },
                {
                    "titre": "Nuha H Marza, Mehdi E Manaa, and Hussein A Lafta. 2021. Classification of spam emails using deep learning. In 2021 1st Babylon International Conference on Information Technology and Science (BICITS). IEEE, 63–68."
                },
                {
                    "titre": "Tomas Mikolov and Geoffrey Zweig. 2012. Context dependent recurrent neural network language model. In 2012 IEEE Spoken Language Technology Workshop (SLT). IEEE, 234–239."
                },
                {
                    "titre": "Sarwat Nizamani, Nasrullah Memon, Mathies Glasdam, and Dong Duong Nguyen. 2014. Detection of fraudulent emails by employing advanced feature abundance. Egyptian Informatics Journal 15, 3 (2014), 169–174."
                },
                {
                    "titre": "V Priya, I Sumaiya Thaseen, Thippa Reddy Gadekallu, Mohamed K Aboudaif, and Emad Abouel Nasr. 2021. Robust attack detection approach for IIoT using ensemble classifier. arXiv preprint arXiv:2102.01515 (2021)."
                },
                {
                    "titre": "Justinas Rastenis, Simona Ramanauskait˙e, Justinas Janulevičius, Antanas Čenys, Asta Slotkien˙e, and Kęstutis Pakrijauskas. 2020. E-mail-based phishing attack taxonomy. Applied Sciences 10, 7 (2020), 2363."
                },
                {
                    "titre": "Karthika D Renuka and P Visalakshi. 2014. Latent semantic indexing based SVM model for email spam classification. (2014)."
                },
                {
                    "titre": "Shuvendu Roy, Sk Imran Hossain, MAH Akhand, and N Siddique. 2018. Sequence modeling for intelligent typing assistant with Bangla and English keyboard. In 2018 International Conference on Innovation in Engineering and Technology (ICIET). IEEE, 1–6."
                },
                {
                    "titre": "Tara N Sainath, Oriol Vinyals, Andrew Senior, and Haşim Sak. 2015. Convolu- tional, long short-term memory, fully connected deep neural networks. In 2015 IEEE international conference on acoustics, speech and signal processing (ICASSP). Ieee, 4580–4584."
                },
                {
                    "titre": "Anuj Kumar Singh, Shashi Bhushan, and Sonakshi Vij. 2019. Filtering spam messages and mails using fuzzy C means algorithm. In 2019 4th International Conference on Internet of Things: Smart Innovation and Usages (IoT-SIU). IEEE, 1–5."
                },
                {
                    "titre": "Kristina Toutanova and Colin Cherry. 2009. A global model for joint lemmati- zation and part-of-speech prediction. In Proceedings of the Joint Conference of the 47th Annual Meeting of the ACL and the 4th International Joint Conference on Natural Language Processing of the AFNLP. 486–494."
                },
                {
                    "titre": "Tian Xia. 2020. A constant time complexity spam detection algorithm for boosting throughput on rule-based filtering systems. IEEE Access 8 (2020), 82653–82661."
                },
                {
                    "titre": "Yan Zhang, PengFei Liu, and JingTao Yao. 2019. Three-way email spam filtering with game-theoretic rough sets. In 2019 International conference on computing, networking and communications (ICNC). IEEE, 552–556. Received 15 April 2023 187"
                }
            ]
        

            processed_pdfs = []
            processed_pdfs.append({
                'Lien': pdf_link,
                'Titre': title,
                'Auteurs': authors_list,
                'Résumé': abstract,
                'Mots clés':keywords,
                #'Texte intégral': text,
                'Références': references_list,
                })
            

        #    # institution_objects = create_institutions(institutions_list)
            
            article_data = {
              'titre': title,
              'resume': abstract,
            #   'texte_integral': text,
              'mots_cles': keywords,
              'URL_Pdf': pdf_link,
            }
            article = Article.objects.get_or_create(**article_data)
            article.save()
        #     article = Article.objects.get_or_create(titre = title,resume = abstract,
        #       texte_integral = text,
        #       mots_cles = keywords,
        #       URL_Pdf = pdf_link,)
             
            
            
        #     # for author_data in authors_list:
        #     #      institution_data = author_data['institution']  
        #     #      nom, adress = institution_data.split(',', 1)  
        #     #      institution = Institution.objects.get_or_create(nom=nom, adress=adress) 
        #     #      auteur = Auteur.objects.get_or_create(full_name=author_data['full_name'], email=author_data['email'], institution=institution)
        #     #      article.auteurs.add(auteur)
              

        #     for reference_data in references_list:
        #          titre=reference_data['titre']
        #          print(titre)
        #          reference = Reference.objects.get_or_create(titre=titre)
        #          article.references.add(reference)
            
            
        #     article.save()

        
            
        # #  except Exception as e:
        # #     processed_pdfs.append({'Lien': pdf_link, 'Erreur': f'Failed to process PDF: {str(e)}'})
    
    return JsonResponse({'processed_pdfs': processed_pdfs})


@csrf_exempt  # Disable CSRF protection for demonstration purposes
def test(request):
    if request.method == 'POST':
            pdf_link = "https://drive.google.com/file/d/1At7MFEUfW1OmDsapLNK4EXiOhYW74xrI/view?usp=drivesdk"
            title = "Semantic Analysis and Classification of Emails through Informative Selection of Features and Ensemble AI Model"
            authors_list = [
                {
                    "full_name": "Shivangi Sachan",
                    "email": "mcs21025@iiitl.ac.in",
                    "institution": "Department of CSE, IIIT Lucknow, Lucknow, UP, India"
                },
                {
                    "full_name": "Khushbu Doulani",
                    "email": "khushidoulani@gmail.com",
                    "institution": "Vardhaman College of Engineering, Hyderabad, India"
                },
                {
                    "full_name": "Mainak Adhikari",
                    "email": "mainak.ism@gmail.com",
                    "institution": "Department of CSE, IIIT Lucknow, UP, India"
                }
            ]

            abstract = "The emergence of novel types of communication, such as email, has been brought on by the development of the internet, which radically concentrated the way in that individuals communicate socially and with one another. It is now establishing itself as a crucial aspect of the communication network which has been adopted by a variety of commercial enterprises such as retail outlets. So in this research paper, we have built a unique spam-detection methodology based on email-body sentiment analysis."

            keywords = "Dataset, KNN, Gaussian Naive Bayes, LSTM, SVM, Bidirectional LSTM, GRU, Word-Embeddings, CNN"
            
            references_list = [
                {
                    "titre": "Rayan Salah Hag Ali and Neamat El Gayar. 2019. Sentiment analysis using unla- beled email data. In 2019 International Conference on Computational Intelligence and Knowledge Economy (ICCIKE). IEEE, 328–333."
                },
                {
                    "titre": "Ali Shafigh Aski and Navid Khalilzadeh Sourati. 2016. Proposed efficient algo- rithm to filter spam using machine learning techniques. Pacific Science Review A: Natural Science and Engineering 18, 2 (2016), 145–149."
                },
                ]
            text = 'ggggggggggggggggggggggggg'

            processed_pdfs = []
            processed_pdfs.append({
                'Lien': pdf_link,
                'Titre': title,
                'Auteurs': authors_list,
                'Résumé': abstract,
                'Mots clés':keywords,
                'Texte intégral': text,
                'Références': references_list,
                })

            article = Article.objects.create(titre = title,resume = abstract,
              texte_integral = text,
              mots_cles = keywords,
              URL_Pdf = pdf_link,)
            

            
            # article_data = {
            #   'titre': title,
            #   'resume': abstract,
            #   'texte_integral': text,
            #   'mots_cles': keywords,
            #   'URL_Pdf': pdf_link,
            # }
            # article = Article.objects.create(**article_data)
            article.save()
    return JsonResponse({'processed_pdfs': processed_pdfs})

