FROM python:3.12.4

WORKDIR /opencv_highlight_line_breaks

COPY Example_Image_JPEG.jpg .
COPY Highlight_Line_Breaks_In_Image.py .

RUN apt-get update && apt-get install -y --no-install-recommends libgl1=1.6.0-1
RUN pip install --no-cache-dir  opencv-contrib-python==4.11.0.86
RUN pip install --no-cache-dir  numpy==2.2.3

CMD ["python", "Highlight_Line_Breaks_In_Image.py"]