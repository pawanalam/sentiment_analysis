from rest_framework import generics
from .models import InputData
from .serializers import InputDataSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import PyPDF2
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView


class InputDataListCreate(generics.ListCreateAPIView):
    queryset = InputData.objects.all()
    serializer_class = InputDataSerializer
    parser_classes = (MultiPartParser, FormParser)  # Handle file uploads

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()

            # Store LinkedIn & GitHub URLs in Session
            request.session['linkedin'] = instance.linkedin if instance.linkedin else None
            request.session['github'] = instance.github if instance.github else None

            # Extract Resume Text & Store in Database
            if instance.resume:
                text = self.extract_text_from_pdf(instance.resume)
                instance.resume_text = text  # ✅ Save extracted text in DB
                instance.save()

                request.session['resume_text'] = text  # ✅ Store in session too
                print("📄 Extracted Resume Text:", text)

            # ✅ **Force session to be saved**
            request.session.modified = True  
            request.session.save()

            # Debugging: Print stored session data
            print("🟢 Stored in Session:")
            print("🔹 LinkedIn:", request.session.get('linkedin'))
            print("🔹 GitHub:", request.session.get('github'))
            print("🔹 Resume Text:", request.session.get('resume_text'))

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("❌ Validation Errors:", serializer.errors)  # Debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def extract_text_from_pdf(self, pdf_file):
        """Extract text from a PDF file"""
        text = ""
        try:
            print(f"📂 Trying to read PDF: {pdf_file.name}")

            with pdf_file.open('rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                num_pages = len(pdf_reader.pages)
                print(f"📄 Total Pages in PDF: {num_pages}")

                for i, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    print(f"📝 Extracted Text from Page {i+1}: {page_text[:200]}")

            if not text:
                print("❌ No text extracted! The PDF may be an image or encrypted.")

        except Exception as e:
            print(f"⚠️ Error extracting text: {e}")

        return text
    
class SessionDataView(APIView):
    def get(self, request, *args, **kwargs):
        print("🔎 Checking Session Data in GET Request:")
        print("🔹 LinkedIn:", request.session.get('linkedin', 'Not available'))
        print("🔹 GitHub:", request.session.get('github', 'Not available'))
        print("🔹 Resume Text:", request.session.get('resume_text', 'No resume text stored'))
        print(f"Session Keys: {request.session.keys()}")
        print(f"Full Session Data: {request.session.items()}")


        return Response({
            'linkedin': request.session.get('linkedin', 'Not available'),
            'github': request.session.get('github', 'Not available'),
            'resume_text': request.session.get('resume_text', 'No resume text stored'),
        })
