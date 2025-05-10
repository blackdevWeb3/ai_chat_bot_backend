from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from openai import OpenAI

# Initialize OpenAI client (v1.x style)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatAPIView(APIView):
    def post(self, request):
        message = request.data.get("message")
        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a hilarious AI that tells short, funny stories full of jokes, "
                            "silly characters, and surprise endings. Always end with a twist or moral."
                        )
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            reply = response.choices[0].message.content.strip()
            return Response({"reply": reply}, status=status.HTTP_200_OK)

        except Exception as e:
            print("OpenAI error:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
