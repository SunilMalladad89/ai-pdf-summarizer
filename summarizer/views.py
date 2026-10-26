from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import pdfplumber
import yake
import re
import os

from django.shortcuts import render
from django.http import HttpResponse

import pdfplumber
import yake
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pathlib import Path
from dotenv import load_dotenv

import google.generativeai as genai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import (
    getSampleStyleSheet
)




def home(request):
    
    error_message=""
    
    if request.method == "GET":
        request.session.flush()

    extracted_text = request.session.get("pdf_text", "")
    summary = request.session.get("summary", "")
    keyword_list = request.session.get("keywords", [])

    page_count = request.session.get("page_count", 0)
    word_count = request.session.get("word_count", 0)
    char_count = request.session.get("char_count", 0)

    selected_summary_type = request.session.get(
        "selected_summary_type", ""
    )

    answer = ""
    question = ""
    source_context=""
    
    qa_history = request.session.get(
        "qa_history",
        []
    )

    # ==========================
# QUESTION ANSWERING
# ==========================

    question = request.POST.get(
        "question",
        ""
    ).strip()
    

    if question:

        paragraphs = request.session.get(
            "paragraphs",
            []
        )
        documents = paragraphs + [question]

        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform(
            documents
        )

        scores = cosine_similarity(
            tfidf_matrix[-1],
            tfidf_matrix[:-1]
        )[0]
        
        context = ""
        best_score = max(scores)

        print("BEST SCORE:", best_score)

        if best_score < 0.05:

            answer = (
                "This question does not appear to be related "
                "to the uploaded document."
            )

        else:

            top_indices = scores.argsort()[::-1][:5]
            
            print("\nTOP MATCHING SECTIONS\n")

            for idx in top_indices:

                print(paragraphs[idx][:300])

                print("-" * 50)

            context = ""

            for idx in top_indices:

                context += (
                    paragraphs[idx][:800]
                    + "\n\n"
                )
            source_context = context
            
            print("SOURCE CONTEXT:")
            print(source_context)

        
        prompt = f"""
        Answer using only the context .

        Format the answer as:
        
        Definition:
        ...
        
        Key Points:
        
        . ...
        . ...
        . ...
        
        Keep the answer concise and easy to read.
        

        If the answer is not available,
        reply:

        Information not found in document.

        Context:

        {context}

        Question:

        {question}

        Answer:
        """

        try:

            print("OLLAMA IS BEING CALLED")
            print("\nQUESTION:")
            print(question)

            print("\nCONTEXT SENT TO PHI3:")
            print(context[:3000])

            print("\nEND OF CONTEXT\n")

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            result = response.json()

            answer = result.get(
                "response",
                "No answer generated."
            )
            
            qa_history.insert(
                0,
                {
                    "question":question,
                    "answer":answer
                }
            )
            qa_history = qa_history[:10]
            
            request.session[
                "qa_history"
                
            ] = qa_history

            print("ANSWER RECEIVED")
            print(answer[:200])

        except Exception as e:

            answer = (
                f"Error generating answer: {str(e)}"
            )

# ==========================
# PDF PROCESSING
# ==========================


       

        # ==========================
        # PDF PROCESSING
        # ==========================

    else:

            pdf_file = request.FILES.get(
                "pdf_file"
            )
            
            
            
            if pdf_file:
                
                if not pdf_file.name.lower().endswith(".pdf"):
                    
                    error_message = (
                        "Invalid file format. Please upload only PDF files."
                    )
                    
                    return render(
                                request,
                                "index.html",
                                {
                                    "text": extracted_text,
                                    "summary": summary,
                                    "keywords": keyword_list,
                                    "page_count": page_count,
                                    "word_count": word_count,
                                    "char_count": char_count,
                                    "keyword_count": len(keyword_list),
                                    "selected_summary_type": selected_summary_type,
                                    "question": question,
                                    "answer": answer,
                                    "source_context": source_context,
                                    "qa_history": qa_history,
                                    "error_message": error_message,
                                }
                            )

            summary_type = request.POST.get(
                "summary_type"
            )

            selected_summary_type = summary_type

            if pdf_file:

                extracted_text = ""

                with pdfplumber.open(
                    pdf_file
                ) as pdf:

                    page_count = len(
                        pdf.pages
                    )

                    for page in pdf.pages:

                        text = page.extract_text()

                        if text:

                            extracted_text += (
                                text + "\n"
                            )
                #Create paragrapg BEFORE Cleaning
                paragraphs = re.split(
                    r'(?=\d+\.\d+)',
                    extracted_text
                )
                
                paragraphs = [
                    p.strip()
                    for p in paragraphs
                    if len(p.strip()) > 50
                    
                ]
                
                print("Total Paragraphs :", len(paragraphs))

                # CLEAN TEXT
                
                cleaned_paragraphs = []
                
                for p in paragraphs:
                    
                    p = re.sub(
                        r"Storage Area Networks Module-d+",
                        " ",
                        p
                    )
                    
                    p = re.sub(
                        r"[•▪■□►◄]",
                        " ",
                        p
                    )

                    p = re.sub(
                        r"\s+",
                        " ",
                        p
                    )

                    cleaned_paragraphs.append(
                        p.strip()
                    )
                    
                paragraphs = cleaned_paragraphs

                extracted_text = re.sub(
                    r"Storage Area Networks Module-\d+",
                    " ",
                    extracted_text,
                )

                extracted_text = re.sub(
                    r"Fig\s*\d+[\.-]\d+",
                    " ",
                    extracted_text,
                )

                extracted_text = re.sub(
                    r"[•▪■□►◄]",
                    " ",
                    extracted_text,
                )

                extracted_text = re.sub(
                    r"\s+",
                    " ",
                    extracted_text,
                )
                
                #CREATE PARAGRAPHS
                
                

                # STATISTICS

                word_count = len(
                    extracted_text.split()
                )

                char_count = len(
                    extracted_text
                )

                # KEYWORDS

                kw_extractor = (
                    yake.KeywordExtractor(
                        top=10
                    )
                )

                keywords = (
                    kw_extractor.extract_keywords(
                        extracted_text
                    )
                )

                keyword_list = [
                    kw[0]
                    for kw in keywords
                ]

                # SUMMARY

                sentences = re.split(
                    r"[.!?]",
                    extracted_text,
                )

                ranked_sentences = []

                for sentence in sentences:

                    sentence = (
                        sentence.strip()
                    )

                    if len(sentence) < 50:
                        continue

                    score = 0

                    for keyword in keyword_list:

                        if (
                            keyword.lower()
                            in sentence.lower()
                        ):
                            score += 1

                    ranked_sentences.append(
                        (
                            score,
                            sentence,
                        )
                    )

                ranked_sentences.sort(
                    reverse=True
                )

                if summary_type == "short":

                    top_n = 5

                elif summary_type == "medium":

                    top_n = 10

                elif summary_type == "detailed":

                    top_n = 15

                else:

                    top_n = 8

                selected_sentences = []

                for (
                    score,
                    sentence,
                ) in ranked_sentences:

                    selected_sentences.append(
                        f"• {sentence}"
                    )

                    if (
                        len(
                            selected_sentences
                        )
                        >= top_n
                    ):
                        break

                summary = "\n\n".join(
                    selected_sentences
                )

                if not summary.strip():

                    summary = (
                        extracted_text[:1500]
                    )

                # SAVE TO SESSION

                request.session[
                    "pdf_text"
                ] = extracted_text
                
                print("TOTAL SECTIONS:", len(paragraphs))

                for i, p in enumerate(paragraphs[:5]):
                     print(f"\nSECTION {i+1}")
                     print(p[:200])
                request.session[
                    "paragraphs"
                ] = paragraphs
                
                

                request.session[
                    "summary"
                ] = summary

                request.session[
                    "keywords"
                ] = keyword_list

                request.session[
                    "page_count"
                ] = page_count

                request.session[
                    "word_count"
                ] = word_count

                request.session[
                    "char_count"
                ] = char_count

                request.session[
                    "selected_summary_type"
                ] = (
                    selected_summary_type
                )

    return render(
        request,
        "index.html",
        {
            "text": extracted_text,
            "summary": summary,
            "keywords": keyword_list,
            "page_count": page_count,
            "word_count": word_count,
            "char_count": char_count,
            "keyword_count": len(
                keyword_list
            ),
            "selected_summary_type": selected_summary_type,
            "question": question,
            "answer": answer,
            "source_context": source_context,
            "qa_history":qa_history,
            "error_message":error_message
        },
    )


def download_pdf(request):

    summary = request.GET.get(
        "summary",
        ""
    )

    keywords = request.GET.get(
        "keywords",
        ""
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="summary_report.pdf"'

    doc = SimpleDocTemplate(
        response
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI PDF Summary Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            summary,
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "<br/><br/>Keywords:<br/>" + keywords,
            styles["BodyText"]
        )
    )

    doc.build(content)

    return response