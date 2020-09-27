# ShellHacks2020-AutoNation-Challenge-Using-Google-Vision-API

AutoNation License Plate Detection Challenge:
- I used Google Cloud VISION API to process the images and get the required data.
- Stored mock data for customers in a .json file
- Stored the function to find and display the customer's information in  a separate file for easy access and modification
- Google Cloud authorization key for this project and the file name for the picture are stored at the top of the licensePlateProcessor.py
- Pictures are stored in the separate folder. Any license plate outside this data set won't have a match with the customer data set unless manually added.
- Pictures "F1.jpg" & "F2.jpg" have errors in detecting the text. F1 reads a 2 as a "Z", and F2 reads some design to the right as an "E"; but those are errors that the AI model would have to learn through unsupervised learning.



## Requirements:
- Python 3.8
- Run this line in the command prompt/terminal: pip install google-cloud-vision

## Encountered Challenges / Solutions
- Challenge #1:
  Sometimes Google Vision wouldn't detect the license plate as an object if the car is too far out or if there are other objects in the picture.
  
  Solution:
  I created a function to detect the car as a whole and crop out that part of the picture and ran it again to detect the license plate.

- Challenge #2:
  When trying to extract the text in the license plate, it would sometime includes data such as the State, or a sticket that it would have.
  
  Solution:
  Found the text block with the largest letter height, and infered that as the license tag.
