#Python Code for Pixel Manipulation for image encryption.

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Function to encrypt/decrypt an image
def process_single_image(mode, folder, filename, key=50):
    input_path = os.path.join(folder, filename)
    
    if not os.path.exists(input_path):
        messagebox.showerror("Error", "File not found!")
        return
    
    output_folder = "encrypted_images" if mode == "encrypt" else "decrypted_images"
    os.makedirs(output_folder, exist_ok=True)
    
    output_path = os.path.join(output_folder, filename)
    
    img = Image.open(input_path)
    img = img.convert("RGB")  # Ensure RGB mode
    pixels = img.load()
    
    # Perform XOR operation for encryption/decryption
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (r ^ key, g ^ key, b ^ key)  
    
    # Preserve image format and quality
    if img.format == "JPEG":
        img.save(output_path, format="JPEG", quality=100)  # Prevent recompression
    else:
        img.save(output_path, format=img.format)  # Preserve PNG, BMP, etc.
    
    messagebox.showinfo("Success", f"Image {mode}ed successfully!\nSaved to {output_path}")

# Function to encrypt or decrypt a folder
def process_folder(mode, folder, key=50):
    if not os.path.exists(folder):
        messagebox.showerror("Error", "Folder not found!")
        return
    
    output_folder = "encrypted_images" if mode == "encrypt" else "decrypted_images"
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            input_path = os.path.join(folder, filename)
            output_path = os.path.join(output_folder, filename)

            img = Image.open(input_path)
            img = img.convert("RGB")  # Ensure RGB mode
            pixels = img.load()

            for i in range(img.width):
                for j in range(img.height):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = (r ^ key, g ^ key, b ^ key)  

            # Preserve original format and prevent quality loss
            if img.format == "JPEG":
                img.save(output_path, format="JPEG", quality=100)
            else:
                img.save(output_path, format=img.format)

    messagebox.showinfo("Success", f"All images {mode}ed successfully!\nSaved to {output_folder}")

# GUI Functions
def encrypt_single():
    folder = filedialog.askdirectory(title="Select Folder Containing Image")
    if folder:
        filename = input("Enter the image filename (with extension): ")
        process_single_image("encrypt", folder, filename)

def decrypt_single():
    folder = filedialog.askdirectory(title="Select Folder Containing Image")
    if folder:
        filename = input("Enter the image filename (with extension): ")
        process_single_image("decrypt", folder, filename)

def encrypt_folder():
    folder = filedialog.askdirectory(title="Select Folder to Encrypt")
    if folder:
        process_folder("encrypt", folder)

def decrypt_folder():
    folder = filedialog.askdirectory(title="Select Folder to Decrypt")
    if folder:
        process_folder("decrypt", folder)

# GUI Setup
root = tk.Tk()
root.title("Image Encryption Tool")

tk.Label(root, text="Image Encryption & Decryption Tool", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Encrypt Single Image", command=encrypt_single, bg="lightblue", width=25).pack(pady=5)
tk.Button(root, text="Decrypt Single Image", command=decrypt_single, bg="lightgreen", width=25).pack(pady=5)
tk.Button(root, text="Encrypt Folder", command=encrypt_folder, bg="lightblue", width=25).pack(pady=5)
tk.Button(root, text="Decrypt Folder", command=decrypt_folder, bg="lightgreen", width=25).pack(pady=5)

root.mainloop()