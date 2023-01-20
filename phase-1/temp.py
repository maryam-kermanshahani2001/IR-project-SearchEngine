# def tokenize():
#     token = {}
#     my_normalizer = Normalizer()
#     my_tokenizer = Tokenizer()
#     for k in
#         Tokenizer.tokenize_words(my_normalizer.normalize(all_data[]))

punctuations = language_punctuations.persian_punctuations
text = "(پرسپولیس فهرمان) است {معنی هرگز} نمیدانستم"
for punc in punctuations:
    text = text.replace(punc, "")
print(text)
