from django.shortcuts import render, redirect
from PyDictionary import PyDictionary
import requests
from wordhoard import Antonyms, Definitions, Synonyms
import bs4
import random
import os
from requests.exceptions import Timeout
from mydico import models
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta
from django.utils import timezone
from spellchecker import SpellChecker

# from utils import Definitions 
# from gtts import gTTS?
import pyttsx3
from django.http import HttpResponse, HttpResponseRedirect

# SUPER USER NAME = admin PASSWOERD = 1234

# Create your views here.


def home(request):
    return render(request, 'temp/home.html')


# def get_random_word():

#     dictionary = PyDictionary()
#     response = requests.get('https://random-word-api.herokuapp.com/word')
#     random_word = response.json()[0]
#     return random_word


def history(request):
    
    # historys = models.History.objects.order_by('-id')
    history = request.session.get('history', [])
    history_list = list(history)[-0:]
    request.session['history'] = history_list
    # request.session['histroy'] = historys
    # request.session.modified=True
    
    favorites = request.session.get('favorites', [])
    
    if request.method =='POST':
        if 'delete' in request.POST:
            delete_word = request.POST['delete']
            if delete_word in history:
                history.remove(delete_word)
        elif 'addToFavorites' in request.POST:
            favorite_word = request.POST['addToFavorites']
            if favorite_word in history and favorite_word not in favorites:
                favorites.append(favorite_word)
        elif 'clear_history' in request.POST:
            history=[]
    
    request.session['history'] = history
    request.session['favorites'] = favorites
    request.session.modified=True
    context = {
        # 'historys' : historys,
        'history' : history,
    }
    return render(request, 'temp/history-page.html', context)


def favourite(request):
    favorite = request.session.get('favorites', [])
    
    if 'delete' in request.POST:
        delete_word = request.POST['delete']
        if delete_word in favorite:
            favorite.remove(delete_word)
            
            
    request.session['favorites'] =favorite
    request.session.modified = True
    
    context={
        'favorite' : favorite,
    }
    return render(request, 'temp/favourite-page.html', context)


def index(request):    
    data_get_recent = models.History.objects.order_by('-id')[0:4]
    history = request.session.get('history', [])[0:4]

     
    try:
        dictionary = PyDictionary()
        response = requests.get('https://random-word-api.herokuapp.com/word')
        random_word = response
        random_word = response.json()[0]
        

      

    except Timeout:   
        random_word = "No Internet Connetion 😭"
        meaning = None
        
        
    except requests.exceptions.RequestException as e:
        random_word = "No Internet Connetion 😭"
        meaning = None
        
    context = {
        'data_get_recent' : data_get_recent,
        'random_word' : random_word,
        'history' : history,
    }

    return render(request, 'temp/index.html', context)








def search(request):

    # ===== SEARCHING FOR WORDS AND FETCHING THE MEANING
    wordSearch = request.GET['wordSearch']
    dictionary = PyDictionary
    meaning = dictionary.meaning(wordSearch)
    
     
    # Auto-correct the search term
    spell = SpellChecker()
    corrected_word = spell.correction(wordSearch)
    
        # Use the corrected word for searching definitions
    # defi = Definitions(search_string=corrected_word)
    # try:
    #     definition = defi.find_definitions()
    #     if definition and all(x is not None for x in definition):
    #         part_of_speech = ''.join(set([x[1] for x in definition]))
    #     else:
    #         part_of_speech = ''
    # except TypeError:
    #     definition = []
    #     part_of_speech = ''
    

    
    
    defi = Definitions(search_string=corrected_word)
    definition = defi.find_definitions()
    
    history = request.session.get('history', [])
    
     #-===== TO ADD THE NEW SEARCHED INTO HISTORY====
    history.append(corrected_word)
    
    # Update the session with the new search history
    request.session['history'] = history

   
   
   
    # ==================== CODE TO SAVE SCEARCHED WORD IN THE HISTORY======
    models.History.objects.create(word = wordSearch)
  
     
        
    
    
    try:
        syn = Synonyms(search_string= wordSearch, output_format='list', )
        synonyms_word = syn.find_synonyms()
        synonyms = synonyms_word[:14]
    except TypeError:
        synonyms = []
        
        
    try:    
        anto = Antonyms(search_string= wordSearch, output_format='list', )
        antonyms_word = anto.find_antonyms()
        antonyms = antonyms_word[:10]
    
    except TypeError:
        antonyms = []
          
    # the try below will try to get the meaning and if the word does not exit like yoruba name it will not pop out error
    #  ======= MAKE SURE YOU DO THE SAME FOR OTHER PART OF SPEECH ======
    
    try:
        nouns = meaning.get('Noun', [])
                
        # The Except will return noting if the word searched does not exit
    except AttributeError:
        
        nouns = []
        
        
    #     # ============= VERB ============
    try:
        verbs = meaning.get('Verb', [])
    except AttributeError:

        verbs = []
        
    #             # ============= ADVERB ============

    try:
        adverbs = meaning.get('Adverb', [])
    except AttributeError:

        adverbs = []
        
   
        
    #             # ============= ADJECTIVE ============
 
    try:
        adjectives = meaning.get('Adjective', [])
    except AttributeError:

        adjectives = []
        
   
        
    #             # ============= PRONOUNS ============

    try:
        pronouns = meaning.get('Pronoun', [])
    except AttributeError:

        pronouns = []
        
   
   
        
    #             # ============= PREPOSITIONS ============

    try:
        prepositions = meaning.get('Preposition', [])
    except AttributeError:

        prepositions = []
        
   
   
    
    context = {
        'definition' : definition,
        'meaning' : meaning, 
        'nouns' : nouns[0:5],
        'pronouns' : pronouns[0:5],
        'prepositions' : prepositions[0:5],
        'synonyms' : synonyms,
        'antonyms' : antonyms,
        'verbs' : verbs[0:5],
        'adjectives' : adjectives[0:5],
        'adverbs' : adverbs[0:5],
        "wordSearch" : corrected_word, 
        "history" :  history, 
    }
    
    return render(request, 'temp/search-page.html',context)

def pronunce(request, wordSearch):
    
    try:
        # language = 'en-au'
        voice = pyttsx3.init()
        # accent = 'au'
        text= wordSearch
        voice.say(text)
        voice.save_to_file(text, " pronunciation.mp3")
        voice.runAndWait()
        # text_speech = #(text = wordSearch)
        # text_speech.save("pronunciation.mp3")
        file_path = os.path.join(os.path.dirname( __file__), 'pronunciation.mp3')
        
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="audio/mpeg")
            response['content-Disposition'] = 'inline; filename=pronunciation.mp3'
            return HttpResponse
    except RuntimeError as e:
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="audio/mpeg")
            response['content-Disposition'] = 'inline; filename=pronunciation.mp3'
            return HttpResponse






def setting(request):
    return render(request, 'temp/setting.html')


def developer(request):
    return render(request, 'temp/developer.html')


def help(request):
    return render(request, 'temp/help.html')


def about(request):
    return render(request, 'temp/about.html')

