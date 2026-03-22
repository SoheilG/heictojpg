import pillow_heif
from PIL import Image
from pathlib import Path


def convert_heic_to_jpg(input_folder, quality = 90):
    folder = Path(input_folder)
    heic_files = list(folder.glob("*.heic")) + list(folder.glob("*.HEIC"))

#glob("*.heic") finds all files matching that pattern. Im checking both HEIC and heic 
#because file extensions from phones can vary. 

    if not heic_files:
        print("No HEIC files found.")
        return
    
    for heic_file in heic_files:
        jpg_file = heic_file.with_suffix(".jpg")
        print(f"converting {heic_file.name} -> {jpg_file.name}")

        heif_file = pillow_heif.read_heif(heic_file)
        img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
        img.save(jpg_file, "JPEG", quality=quality)
#Image.frombytes() constructs a Pillow image directly from raw pixel data 
#rather than from a file so it never needs to identify the file format. I had an issue that was making it fail previously with register_heif_opener() and image.open()

    print(f"Done! {len(heic_files)} file(s) converted.")

convert_heic_to_jpg(r"C:/Users/Soheil/Desktop/projects/heictojpg/heic_photos")


