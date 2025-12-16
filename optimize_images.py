from PIL import Image
import os
import glob

def optimize_images():
    base_dir = r"e:\Project\Connectly\static\images"
    # Mapping of image pattern to target width (height auto)
    # Keeping None for auto/original size if resizing not critical or complex
    
    # logo.png -> logo.webp (Resize to small since it's used as nav logo, keep original for safety)
    # chat-card.png -> chat-card.webp
    # login-card.png -> login-card.webp
    
    targets = [
        {"pattern": "logo.png", "width": 80}, # For navbar (displayed at ~40px)
        {"pattern": "chat-card.png", "width": 400}, # Displayed in card
        {"pattern": "login-card.png", "width": 400},
    ]
    
    print(f"Optimizing images in {base_dir}...")
    
    for target in targets:
        files = glob.glob(os.path.join(base_dir, target["pattern"]))
        for file_path in files:
            try:
                img = Image.open(file_path)
                filename = os.path.basename(file_path)
                name, ext = os.path.splitext(filename)
                
                # Calculate new height to maintain aspect ratio
                w_percent = (target["width"] / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                
                img_resized = img.resize((target["width"], h_size), Image.Resampling.LANCZOS)
                
                new_file_path = os.path.join(base_dir, f"{name}.webp")
                img_resized.save(new_file_path, "WEBP", quality=85)
                
                print(f"Converted {filename} -> {name}.webp")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    optimize_images()
