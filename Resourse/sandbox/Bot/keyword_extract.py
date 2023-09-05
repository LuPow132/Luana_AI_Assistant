from rake_nltk import Rake

text = "Hey do you remember about what I need to buy at supermarketI used to tell you?"

rake = Rake()
rake.extract_keywords_from_text(text)
print(rake.get_ranked_phrases()[:3])