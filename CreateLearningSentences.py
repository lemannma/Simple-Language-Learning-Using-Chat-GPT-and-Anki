"""
Created on Sat Apr 15 15:18:59 2023

@authors: Dr. Olga Lehmann and Matthias Lehmann
"""

import openai

# Set up OpenAI API credentials and endpoint
openai.api_key = "{your API-Key}"
model_engine = "text-davinci-002" # or any other model that supports the learning language

learning_sentence_list = []

learning_language = input("Which language do you whant to learn ")
translation_language = input("What is your native language? ")
amount_sentences_to_be_created = 500 #define this numer as you like

def createSentencesViaChatGPT():
    # Generate 30 random sentences using OpenAI API
    responses = openai.Completion.create(
        engine=model_engine,
        prompt="please create 25 sentences in " + learning_language + " with high variation of used words. the sentences should use different time forms and be no longer then 7 words. provide a translation in " + translation_language + " as well. the format is [sentence]:[translation in " + translation_language + "]",
        temperature=0.7,
        max_tokens=4000,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
        echo=True,
        stream=False,
    )
    return responses
        
while len(learning_sentence_list) < amount_sentences_to_be_created:

    chatGPT_responses = createSentencesViaChatGPT()
    
    #clean response from question text
    sentences = chatGPT_responses.choices[0].text.split("\n")
    sentences = sentences[2:]

    #clean response from numbering of ChatGPT and add to learning_sentence_list 
    for sentence in sentences:
        sentence = sentence.split(" ", 1)[1]
        #check four doubles
        if sentence not in learning_sentence_list:
            learning_sentence_list.append(sentence)
    
    #save the results
    with open('learning_sentence_list.txt', mode='w') as f:
        for item in learning_sentence_list:
            f.write("%s\n" % item)

