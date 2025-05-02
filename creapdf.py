import os
from pathlib import Path
from PIL import Image
from tkinter import Tk, filedialog

def seleziona_cartella():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    cartella_selezionata = filedialog.askdirectory(title="Seleziona la cartella contenente gli screenshot")
    root.destroy()
    if not cartella_selezionata:
        raise ValueError("Nessuna cartella selezionata.")
    return cartella_selezionata

def crea_cartella_univoca(base_cartella, nome_base="PDF_Output"):
    cartella_output = base_cartella / nome_base
    if not cartella_output.exists():
        return cartella_output
    i = 1
    while True:
        nuova_cartella = base_cartella / f"{nome_base}_{i}"
        if not nuova_cartella.exists():
            return nuova_cartella
        i += 1

def crea_pdf_da_screenshot(cartella_input):
    cartella = Path(cartella_input)
    if not cartella.exists() or not cartella.is_dir():
        raise FileNotFoundError(f"La cartella selezionata non è valida: {cartella_input}")

    estensioni_valide = ('.png', '.jpg', '.jpeg')
    immagini = [img for img in cartella.iterdir() if img.suffix.lower() in estensioni_valide]

    if not immagini:
        print("Nessuna immagine trovata nella cartella.")
        return

    immagini_ordinate = sorted(immagini, key=lambda x: x.stat().st_mtime)

    immagini_rgb = []
    for img_path in immagini_ordinate:
        img = Image.open(img_path).convert("RGB")
        immagini_rgb.append(img)

    cartella_output = crea_cartella_univoca(cartella)
    cartella_output.mkdir(parents=True, exist_ok=False)

    nome_pdf_output = f"{cartella.name}.pdf"
    output_path = cartella_output / nome_pdf_output
    immagini_rgb[0].save(output_path, save_all=True, append_images=immagini_rgb[1:])
    print(f"Deli ho creato il PDF con successo nella cartella: {output_path.resolve()}")

if __name__ == "__main__":
    try:
        percorso = seleziona_cartella()
        crea_pdf_da_screenshot(percorso)
    except Exception as e:
        print(f"Errore: {e}")
