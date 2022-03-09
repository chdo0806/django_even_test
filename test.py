# import googletrans
# from googletrans import Translator
 
# # print(googletrans.LANGUAGES)
 
# text1 = "Hello welcome to my website!"

# translator = Translator()
 
# print(translator.detect(text1))

# trans1 = translator.translate(text1, src='en', dest='ja')

# print("English to Japanese: ", trans1.text)



# -------------------------------------------
import pdfplumber

pdf = pdfplumber.open("아뱅.pdf")

num = len(pdf.pages) # pdf page 객체들의 리스트
                     # page 수만큼 객체들이 존재
for i in range(num):
    print(pdf.pages[i].extract_text())
# 1페이지 텍스트 추출
