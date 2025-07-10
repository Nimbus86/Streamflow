from flask import Blueprint, render_template, request, flash, redirect, url_for
import os, uuid
from datetime import datetime

# Diffusers-imports
import torch
from diffusers import StableDiffusionPipeline

# Laad de Stable Diffusion-modelpipeline één keer
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if DEVICE=="cuda" else torch.float32,
    safety_checker=None
).to(DEVICE)

bp = Blueprint('thumbnail', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.form.get('prompt', '').strip()
        if not keywords:
            flash("Voer eerst wat keywords in.", "error")
            return redirect(url_for('thumbnail.index'))

        # 1) Refine je keywords via vaste template (gratis)
        #    Je kunt deze zin aanpassen naar je stijl
        detailed_prompt = (
            f"{keywords}, high detail, cinematic lighting, "
            "bold text overlay, vibrant colors, 4k resolution"
        )

        # 2) Genereer de afbeelding
        image = pipe(detailed_prompt).images[0]

        # 3) Sla op in static/results
        filename = f"{uuid.uuid4().hex}.png"
        out_dir = os.path.join('static', 'results')
        os.makedirs(out_dir, exist_ok=True)
        full_path = os.path.join(out_dir, filename)
        image.save(full_path)

        flash("Thumbnail gegenereerd!", "success")
        return redirect(url_for('thumbnail.index', image=filename))

    # GET
    image = request.args.get('image')
    return render_template('index.html', image=image)
