from flask import render_template

from app import app
from app.forms.histogram_form import HistogramForm
from config import Configuration

config = Configuration()


@app.route('/histograms', methods=['GET', 'POST'])
def histograms():
    form = HistogramForm()

    if form.validate_on_submit():  # POST
        image_id = form.image.data
        return render_template("histogram_output_queue.html", image_id=image_id)

    return render_template('histogram_select.html', form=form)


