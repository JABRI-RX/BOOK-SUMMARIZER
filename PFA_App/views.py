from django.shortcuts import render
 
import re
import openai
openai.api_key = "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"


# Create your views here.
def index(request):
    status = "OK"
    #book object
    book = {
        'book_resume':"",
        'book_img':"",
    }
    if request.method == "POST":
        #book name from post data
        book_name:str = request.POST.get("book_name")
        #langauge name from post data
        language = request.POST.get("languages")

        
        #
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_resume(book_name,language),
            temperature=0.8,
            max_tokens=2000
        )

        book["book_resume"] = response.choices[0].text.replace("-","")
        isbn_num = re.findall(r'\d+',book["book_resume"])
        print(isbn_num)
        book["book_img"] = f"https://covers.openlibrary.org/b/isbn/{isbn_num[0]}-L.jpg"
        return render(request,"base.html",{
            'book':book,
            'status':status
        })
    elif request.method == "GET":
        print("data has been get")
        return render(request,"base.html",{})


def generate_resume(book_name,language):
    return f"Give me the english version ISBN and a summary of the book {book_name}  in {language} (please produce consistent result)"