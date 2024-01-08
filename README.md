# Beauty Rating Software
This is an archive of the software used for my Math Modeling Project 1 in Secondary 3. The goal of this project was to find out who was <ins>the most mathematically beautiful person in the class is based on the Golden Ratio</ins>. It uses the [facial-keypoints-detecter](https://github.com/ShashankKumbhare/facial-keypoints-detecter) project by [ShashankKumbhare](https://github.com/ShashankKumbhare) to detect facial keypoints. Using the provided dataset stated in the repository's [`README.md`](https://github.com/ShashankKumbhare/facial-keypoints-detecter?tab=readme-ov-file#data-description) file, the model was trained for many hours overnight from my laptop (Acer Aspire 3 [A315-35-C5N7] with an [Intel® Celeron® Processor N5100](https://ark.intel.com/content/www/us/en/ark/products/212329/intel-celeron-processor-n5100-4m-cache-up-to-2-80-ghz.html) with 8GB of RAM) as I did not know how to use Jupyter Notebook. The training session in the IDLE can be seen in `trainingOutput.txt`. It can be seen that I tried to run `train.py` which did not work (for some reason).
<br><br>
Next, my group and I studied [Facial Beauty Analysis and the Golden Ratio (Phi 1.618) featuring Florence Colgate and PhiMatrix](https://www.youtube.com/watch?v=kKWV-uU_SoI) by [PhiMatrix1618](https://www.youtube.com/@phimatrix1618) to study the measurements my program needed to take (Google and I wrote all the code). Our Notes can be found in `Facial Keypoint Notes.xlsx`.
<br><br>
Following that, I wrote `cv2Capture.py` for data collection. Data was collected using the same laptop mentioned earlier, an iPad connected to the laptop as an external display for the user to position face in the allocated frame, and a webcam on top of the iPad to take the Photos. I will only share my photos to protect the privacy of my classmates. The output folder is `cv2Capture`. Within this folder, there are subfolders titled after the inputed name that was prompted for when the program starts. It was only after I collected all the data that I realized 2 things:
1. I forgot to save the facial keypoints (at least I still had the images)
2. The `facial-keypoints-detecter` model was not very accurate

Therefore, I wrote, then rewrote `FacialKeypointEditor2.py`, which redetected the facial keypoints and gave me an GUI to edit correct the position of the facial keypoints. The program then saved the corrected facial keypoints to `Output.xlsx`. I have again removed all of my classmates photos and data to maintain their privacy. I also shared the data without the images to other groups that did not manage to complete their data collection. However none of the other groups interpreted the data properly despite trying my best to help them make sense of the data. The data is in an x and y co-ordinates in a computer coordinate system and not the Cartesian Coordinate System they learn in school.
<br><br>
Finally, I `xlsxReader.py` was written. It read the facial keypoints from `Output - Backup.xlsx` which is just a duplicate of `Output.xlsx` just in case things went wrong. The program outputted `FinalOutput.xlsx` of which again has my classmates photos and data removed. The program also read images read a from the `media` folder which is basically the images obtained from `Output.xlsx` by renaming it to `Output.zip` and then extracting the `Output.zip\xl\media\` folder from it. The following is the rating of me from my program in text form:
```
15. Azlan [Full Name Censored]

1. (Eyes to Nose Flair) to Nose Base: 92.24037616514106%
2. (Eyes to Nostril top) to Centre of lips: 82.14628625601699%
3. (Eyes to Nose base) to Bottom of lips: 85.40295371948854%
4. (Eyes to Centre of lips) to Bottom of Chin: 90.56025858127997%
5. (Nose Flair to Bottom of Lips) to Bottom of Chin: 77.22144948724574%
6. (Nose Flair to Top of Lips) to Bottom of Chin: 90.74399067852939%
7. (Top of Lips to Bottom of lips) to Bottom of Chin: 70.8890502257808%
8. (Top of Lips to Centre of lips) to Bottom of Lips: 63.334123612615855%
9. (Top of Eyebrows to Top of eyes) to Bottom of eyes: 73.95585263194408%
10. (Top of Eyebrows to Top of lips) to Bottom of Chin: 99.72561643361321%
11a. (Left Side of Face to Left Side of eyes) to Centre of Left Pupil: 72.19632055847137%
11b. (Right Side of Face to Right Side of eyes) to Centre of Right Pupil: 87.11634993825339%
12a. (Left Side of Face to Left Side of Iris) to Other Side of Left eye: 68.62613933833971%
12b. (Right Side of Face to Right Side of Iris) to Other Side of Right eye: 86.4204921909742%
13a. (Left Side of Face to Left Side of Iris) to Centre of Face: 98.30884157610146%
13b. (Right Side of Face to Right Side of Iris) to Centre of Face: 59.512272439156824%
14a. (Left Side of Face to Side of Left eye) to the Right eye: 88.48388653788032%
14b. (Right Side of Face to Side of Right eye) to the Left eye: 94.74174611456012%
15a. (Left Side of Face to Centre of Face) to the Right eye: 89.92083811556368%
15b. (Right Side of Face to Centre of Face) to the Left eye: 85.32722636516657%
16a. (Left Side of Face to Inside Right eye) to Right side of face: 97.97147264257026%
16b. (Right Side of Face to Inside Left eye) to Left side of face: 92.37923835075567%
17a. (Left Side of Eye to Left Flair of Nose) to Right Flair of Nose: 75.9277545634001%
17b. (Right Side of Eye to Right Flair of Nose) to Left Flair of Nose: 65.50464070010563%
18a. (Centre of Left Pupil to Top of Nose Flair) to bottom of nose: 82.21016235463293%
18b. (Centre of Right Pupil to Top of Nose Flair) to bottom of nose: 87.2771480295427%
19a. (Centre of Left Pupil to Centre of Left Nostril) to Centre of Right Nostril: 23.908558639495283%
19b. (Centre of Right Pupil to Centre of Right Nostrils) to Centre of Left Nostril: 58.17789488598834%
20a. (Inside of Left Eye to Left Nose Bridge) to Right Nose Bridge: 66.2119804919902%
20b. (Inside of Right Eye to Right Nose Bridge) to Left Nose Bridge: 54.403691689094124%
21a. (Left Side of Mouth to Cupid’s Left bow point of lips) to Cupid’s Right bow point of lips: 77.71057219282864%
21b. (Right Side of Mouth to Cupid’s Right bow point of lips) to Cupid’s Left bow point of lips: 80.04860828241078%
22. (Bottom of nose to Top of lips) to Bottom of lips: 46.26356329004718%
23. Head Height to Head Width: 92.10338298543765%
Overall Rating: 78.14625706071834%
```
<br>

This project was very fun and was completed in just <ins>**19 days**</ins>. There was of course much room for improvement.<br>Firstly, training the model on Jupyter Notebook would have been faster and placed less strain on my computer.<br>Secondly, I should have used a pre-trained model that was accurate enough for face biometrics. This would have saved a lot of time and trouble preparing the data for calculation as I would not have needed to create an entire GUI with `pygame` to edit the facial keypoints.<br>Finally, I should have combined all of the programs together so that I could get the output immediately after a face was scanned.
> Bros gonna go tell me I'm Ugly in 7 different languages. <br> - One of my classmates
