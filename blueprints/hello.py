import os
import uuid
from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from ultralyticsplus import YOLO
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()

# Crea il Blueprint per questa sezione
hello = Blueprint('hello', __name__, template_folder='../templates')

# Configurazioni
UPLOAD_FOLDER = 'static/uploads'
MODEL_NAME = "foduucom/plant-leaf-detection-and-classification"

# Carica il modello YOLOv8 per il rilevamento delle foglie
model = YOLO(MODEL_NAME)

# Funzione per eseguire il rilevamento e classificazione
def classify_plant(image_path):
    results = model.predict(image_path)
    if results[0].boxes:
        # Estrai il nome della pianta dalla classe predetta
        plant_name = results[0].names[results[0].boxes.cls[0].item()]
    else:
        plant_name = "Foglia non riconosciuta"
    return plant_name

# Funzione per salvare l'immagine
def save_uploaded_image(image):
    filename = secure_filename(image.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    try:
        image.save(filepath)
        return filepath
    except Exception as e:
        flash(f'Errore nel salvataggio del file: {str(e)}', 'danger')
        return None

# Route per il caricamento dell'immagine
@hello.route('/upload', methods=['GET', 'POST'])
def upload_leaf():
    if request.method == 'POST':
        if 'image' not in request.files or request.files['image'].filename == '':
            flash('Nessun file selezionato. Riprova.', 'warning')
            return redirect(request.url)

        image = request.files['image']
        filepath = save_uploaded_image(image)
        if not filepath:
            return redirect(request.url)

        # Classifica la pianta
        plant_name = classify_plant(filepath)
        
        # Mostra il risultato
        flash(f'Pianta classificata come: {plant_name}', 'success')
        return render_template('result.html', plant_name=plant_name, image_path=filepath)
    
    return render_template('profile.html')
