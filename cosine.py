import spacy
nlp = spacy.load('en')
doc1 = nlp(u'Hello hi there!')
doc2 = nlp(u'Hello hi there!')
doc3 = nlp(u'Hey whatsup?')

print (doc1.similarity(doc2)) # 0.999999954642
print (doc2.similarity(doc3)) # 0.699032527716
print( doc1.similarity(doc3)) # 0.699032527716