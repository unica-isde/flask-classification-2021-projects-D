import os
import random

import redis
from flask import render_template, redirect, url_for
from rq import Connection, Queue
from rq.job import Job
from torchvision import transforms

from app import app
from app.forms.color_jitter_form import ClassificationColorJitterForm
from config import Configuration
from ml.classification_utils import classify_image, fetch_image  #

config = Configuration()


@app.route('/classifications_jitter', methods=['GET', 'POST'])
def classificationsJitter():
    """
    API for selecting a model and an image and running a
    classification job. Returns the output scores from the
    model.
    """
    form = ClassificationColorJitterForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        model_id = form.model.data
        # Saving color jitter values from the form
        color_values = [form.brightness.data, form.contrast.data, form.saturation.data, form.hue.data]

        # The modify image function is called only if at least one of the fields has been changed
        if not all(values is None for values in color_values):
            image_id = modify_image(image_id, color_values)

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": image_id,
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())

    for file in os.listdir("app/static/imagenet_subset"):
        if file.startswith("modified"):
            os.remove("app/static/imagenet_subset/" + file)

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_jitter_select.html', form=form)


def modify_image(img_id, color_values):
    """
    Function that takes an array with color jitter values and applies them to
    the selected image. It creates a new modified image and saves it in the
    images set.
    @param color_values: array with values for color jitter transformation
    @return modified_id: returns the id of the modified image
    """
    # Setting default values for undefined fields
    for i, value in enumerate(color_values):
        if value is None:
            color_values[i] = 0

    # Fetching selected image and applying color jitter transform to the selected image
    img = fetch_image(img_id)
    transform = transforms.ColorJitter(brightness=color_values[0], contrast=color_values[1],
                                       saturation=color_values[2], hue=color_values[3])
    modified_img = transform(img)

    # Creating a new ID for the new image and saving it in the images set
    random_number = random.randint(0, 100000)
    modified_id = 'modified_' + img_id + str(random_number) + '.png'
    modified_img.save('app/static/imagenet_subset/' + modified_id)

    return modified_id
