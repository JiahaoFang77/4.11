# 4.11
https://www.youtube.com/watch?v=AuTeuRbuQDQ
# **Please download the necessary libraries before runing the code:**

 -pip install opencv-python-headless 
  
 -pip install pytesseract Pillow

### Abstract
What I tested is the license plate number of the vehicle from a surveillance video. I will record the total time that the corresponding license plate vehicle is within the monitoring range. If the total length of the road under monitoring is known, the speed of the vehicle can be calculated from this, and then the vehicle can be judged whether it is overspeeding. I used three different methods for detection. 

The first method did not use AIDB, but directly used OCR to identify vehicles. For the second method I used AIDB a method to optimize recognition speed, and the other parameters are exactly the same as the first. Moreover, the third method I used was the Approximate Queries mentioned in the paper, which further improved the recognition speed but sacrificed some accuracy.
