from flask import render_template

from app import app
from app.forms.histogram_form import HistogramForm
from config import Configuration

config = Configuration()


@app.route('/histograms', methods=['GET', 'POST'])
def histograms():
    """
    Function that takes the chosen image id and renders the html page with its corresponding histogram through a
    JavaScript script
    """

    form = HistogramForm()

    if form.validate_on_submit():  # POST

        # get the image id
        image_id = form.image.data

        return render_template("histogram_output_queue.html", image_id=image_id)

    return render_template('histogram_select.html', form=form)


