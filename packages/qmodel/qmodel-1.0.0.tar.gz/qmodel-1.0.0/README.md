<div style= "display:flex"><h1 style="color: #154A9F ;" > QModel </h1>
<img style = "display:inline-flex ;margin-left: auto " src="Images/logo.png"  width = "200"></div>

Welcome to the QModel Documentation, here are every details you may need to understand how to use QModel.

<h2 style="color: #154A9F ;"> What does this library: </h2>
Q-model is a library that contains everything you need to create a Random Forest Classifer (RFC) to read 7 digits display from an image.


<h2 style="color: #154A9F ;">What can you do with that library ? </h2>
<ul>
    <li>Create a training dataset of images to train a RFC model</li>
    <li>Create a testing dataset of images to test a trained RFC model</li>
    <li>Create and train a RFC model with a training dataset</li>
    <li>Test a RFC model with a testing dataset of images</li>
    <li>Use a RFC model to read the values of a display image</li>
</ul>

<h2 style="color:#154A9F ;">Create a training dataset :</h2>

<h4>1st step :</h4>

First you have to take pictures of your 7-segment dipslay (try to take several photos to have at least every digit 0,9 with a good image quality).
Place them into a folder.

<h4>2nd step :</h4>

Then, for each photo open the photo editor and crop the image around the display to have a nice rectangle around all the digits you try to detect, as below.


Device image:

<img style = "display:block ;margin-left: auto ; margin-right:auto " src ="Images/token.jpg"></img>

Display image:

<img style = "display:block ;margin-left: auto ; margin-right:auto " src ="Images/display.jpg"></img>

Then place all theese images into a folder that you can name "display" for exemple.

<h4> 3rd step :</h4>

Now you have a folder full of display images.
Use the `Testingset` class from the `testing_set.py` file to extract digits images from display images and save them into a folder.

Example : 
```python
    from testing_set import Testingset
    testing_set = (display_images_path, destination_path)
```

You should now have a folder at the destination_path full of digits images.

<h4> 4th step :</h4>

You now must select 10 images for every token you used.
1 image per digits per token.

Name every images by the digit they are representating

For example this image: 

<img style = "display:block ;margin-left: auto ; margin-right:auto " src ="Images/digit.jpg"></img>

is going to be saved as "0.jpg".

Take them and place them into a folder named by the name of the token their are from.

For example if you have took images of the "A" token, place them into a folder named "A".

<h4>5th step :</h4>

Now you must call the ```TrainingSet ``` class from the `training_set.py` file, as below.

```python
from training_set.py import TrainingSet
training_set = TrainingSet(name, path , original_10_img, storeImages)
```

With : 

- `name` (str): name of the set that will be create

- `path_to_save` (str): root of the path where will be save the set

- `original_10_img` (list of str): path where are located the 10 digit images that you created. ( if you want to create a training dataset from multiple device, you have to add the path of the folder that contains theese images to the list)

- `storeImages` (boolean): set as False by default, if you set it at True, the images before renaming and resizing will be save 

<h4>Conclusion</h4>

You now should have a training dataset at the `path_to_save` 

<h2 style="color:#154A9F ;">Create a testing dataset :</h2>

To create a testing dataset follow the 3rd first step of the Training dataset guide. 

You need now to sort every digits image and place each one of them in a folder named by the digit they are representing.

For example put this image 
<img style = "display:block ;margin-left: auto ; margin-right:auto " src ="Images/digit.jpg"></img>

into a folder called "0"

You shoud have a testing dataset of digits images. 

<h2 style="color:#154A9F ;">Create and training a Random Forest Model Classifier  :</h2>

First you will need a training dataset so be sure you have one already created by following the guide above

You need to call a `ModelTraining` object from the `model_training.py` file, and use the `train()` method from that class.

Example :

```python
from model_training import ModelTraining
model_training = ModelTraining(training_set_path , model_path)
model_training.train()
```

You now have created and trained a Random Forest Classifer model.
If you want to test it or use it you can use the ``get_model_path()`` method of the `ModelTraining` object to get the path of that just created model.

<h2 style="color:#154A9F ;">Test a trained Random Forest Model Classifier  :</h2>

To test the model you need to first have a testing set created. 
Ensure you have created a testing dataset by following the guide above.
To test a model, you need to create a `ModelTesting` object from the `model_testing.py` file. 
Then call `prediction()` method to get the accuracy of the model. 

Example:

```python
    from model_testing import ModelTesting
    model_test = ModelTesting(testing_set_path, model_path)
    inverted_resulted , accuracy = model_test.prediction()

```
- `testing_set_path` is the path of the testing dataset
- `model_path` is the path of the model
- `accuracy` is the accuracy of the model
- `inverted_result` is the list of the predictions made by the model 

<h2 style="color:#154A9F ;">Make prediction with a Random Forest Model Classifier  :</h2>

The main goal of building a Random Forest Classifier with Q-model is to read the value of a 7 segment display.
To do that you have to make prediction with a Random Forest Classifer. 

To make a prediction you need to use a list of images.
For that you will use the `PredictionImages` class from the `prediction_images.py` file.

Example of list of images from a PredictionImages object :
```python
from prediction_images import PredictionImages

prediction_images = PredictionImages(display_path)
image_list = prediction_images.getdigitlist()
```
`display_path` is the path where are located all the display images.

So, now you should have a trained RFC model and tested it.

You now need to call a `ModelUsing` object from the `model_using.py` file.
A ModelUsing object need an image list to work so you need to use the image_list got above from the ``PredictionImages`` object. 

Now create a ``ModelUsing`` object by givinig it the path of the RFC model you want to use:

```python
    from model_using import ModelUsing
    from prediction_images import PredictionImages

    prediction_images = PredictionImages(display_path)
    image_list = prediction_images.getdigitlist()

    #model_path is the path of the model you want to use
    model_using = ModelUsing(model_path)

    result = model_using.otp_prediction(image_list)
    #result is a list of every digits value like [5, 6, 8, 6, 8, 5]

```
`result` is the result of the prediction made by the model.