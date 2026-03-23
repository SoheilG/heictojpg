import pillow_heif
from PIL import Image, ImageOps
from pathlib import Path
import piexif

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
        print(f"Converting {heic_file.name} -> {jpg_file.name}")

        try:
            heif_file = pillow_heif.read_heif(heic_file)
            img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
            img = ImageOps.exif_transpose(img)

            exif_data = heif_file.info.get("exif")
            if exif_data:
                exif_dict = piexif.load(exif_data)
                # Reset orientation tag to "normal" (1) so viewers don't rotate again
                exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
                clean_exif = piexif.dump(exif_dict)
                img.save(jpg_file, "JPEG", quality=quality, exif=clean_exif)
            else:
                img.save(jpg_file, "JPEG", quality=quality)
                print(f"  ⚠ No EXIF data found in {heic_file.name}")

        except Exception as e:
            print(f"  ✗ Failed: {e}")
#Image.frombytes() constructs a Pillow image directly from raw pixel data 
#rather than from a file so it never needs to identify the file format. I had an issue that was making it fail previously with register_heif_opener() and image.open()

    print(f"Done! {len(heic_files)} file(s) converted.")

convert_heic_to_jpg(r"C:/Users/Soheil/Desktop/projects/heictojpg/heic_photos")


