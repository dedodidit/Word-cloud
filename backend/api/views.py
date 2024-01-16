# wordcloud_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import WineMask
from .serializers import WineMaskSerializer
from django.http import HttpResponse
from backend.settings import MEDIA_ROOT
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS

stopwords = set(STOPWORDS)
stopwords.update(["drink", "now", "wine", "flavor", "flavors"])


def transform_format(val):
    return 255 if val != 0 else val


def one_color_func(
    word=None,
    font_size=None,
    position=None,
    orientation=None,
    font_path=None,
    random_state=None,
):
    h, s, l = 0, 0, 0
    return "hsl({}, {}%, {}%)".format(h, s, l)


def generate_wordcloud_async(text_input, wine_mask):
    wine_mask_np = np.array(Image.open(wine_mask))
    vectorized_transform_format = np.vectorize(transform_format)
    transformed_wine_mask = vectorized_transform_format(wine_mask_np)

    wc = WordCloud(
        background_color="white",
        mask=transformed_wine_mask,
        stopwords=stopwords,
        max_words=200,
        repeat=True,
        color_func=one_color_func,
    )

    wc.generate(text_input.upper())

    img_buffer = BytesIO()
    wc.to_image().save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return img_buffer


class GenerateWordCloudView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        wine_mask = request.data.get("wine_mask")
        text_input = request.data.get("text_input", "")

        with ThreadPoolExecutor() as executor:
            img_future = executor.submit(
                generate_wordcloud_async, text_input, wine_mask
            )
            img_buffer = img_future.result()

        response = HttpResponse(content_type="image/png")
        response["Content-Disposition"] = 'attachment; filename="wordcloud.png"'
        response.write(img_buffer.getvalue())
        return response
