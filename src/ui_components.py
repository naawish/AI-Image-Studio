import os
import cv2
import numpy as np
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox
from rembg import remove

# Safe Import for Drag and Drop
DND_AVAILABLE = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    pass

# ==========================================================
# UNIVERSAL IMAGE TOOLKIT (BSc Level 6 Version)
# ==========================================================
class ImageToolkitApp:
    def __init__(self):
        # Initialize the window
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = ctk.CTk()
        
        self.root.title("BSc Digital Systems Project: Image Converter")
        self.root.geometry("1000x650")
        
        # Styling
        ctk.set_appearance_mode("dark")
        self.root.configure(bg="#242424")
        
        self.input_path = None

        # --- Layout ---
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="UWE AI Toolkit", font=("Arial", 22, "bold")).pack(pady=30)

        # AI Buttons
        ctk.CTkButton(self.sidebar, text="Remove Background", command=self.process_bg_removal).pack(pady=15, padx=20)
        ctk.CTkButton(self.sidebar, text="Surface Clean", command=self.process_eraser).pack(pady=15, padx=20)
        
        self.lbl_status = ctk.CTkLabel(self.sidebar, text="System: Online", text_color="#28a745")
        self.lbl_status.pack(side="bottom", pady=20)

        # Main Workspace
        self.main_view = ctk.CTkFrame(self.root, border_width=2, border_color="#444", corner_radius=15)
        self.main_view.pack(expand=True, fill="both", padx=30, pady=30)

        # Load Label
        self.lbl_main = ctk.CTkLabel(self.main_view, 
                                     text="DRAG & DROP IMAGE HERE\n(or use the button below)",
                                     font=("Arial", 20))
        self.lbl_main.place(relx=0.5, rely=0.4, anchor="center")

        # Select Button (The "Bulletproof" backup)
        ctk.CTkButton(self.main_view, text="Select Image Manually", 
                     command=self.manual_upload).place(relx=0.5, rely=0.6, anchor="center")

        # Export Area
        self.export_frame = ctk.CTkFrame(self.root, height=100)
        self.export_frame.pack(fill="x", side="bottom", padx=30, pady=(0, 30))
        
        self.format_var = ctk.StringVar(value="PNG")
        ctk.CTkOptionMenu(self.export_frame, values=["PNG", "JPEG", "WEBP", "BMP"], 
                         variable=self.format_var).pack(side="left", padx=30, pady=20)

        ctk.CTkButton(self.export_frame, text="Export & Save", fg_color="#28a745", 
                     command=self.save_final).pack(side="right", padx=30, pady=20)

        # Activate Drag and Drop if library loaded
        if DND_AVAILABLE:
            self.main_view.drop_target_register(DND_FILES)
            self.main_view.dnd_bind('<<Drop>>', self.handle_drop)
        else:
            print("Drag and Drop library not found. Using manual upload mode.")

    # --- Feature Logic ---

    def handle_drop(self, event):
        path = event.data.strip('{}')
        self.load_image(path)

    def manual_upload(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.webp *.avif *.bmp")])
        if path:
            self.load_image(path)

    def load_image(self, path):
        self.input_path = path
        self.lbl_main.configure(text=f"LOADED:\n{os.path.basename(path)}", text_color="#28a745")
        self.lbl_status.configure(text="Status: Image Loaded", text_color="white")

    def process_bg_removal(self):
        if not self.input_path: return
        self.lbl_status.configure(text="AI Processing...", text_color="orange")
        self.root.update()
        try:
            with open(self.input_path, 'rb') as i:
                result = remove(i.read())
            temp = "temp_nobg.png"
            with open(temp, "wb") as o: o.write(result)
            self.input_path = temp
            self.lbl_main.configure(text="AI SUCCESS:\nBackground Removed", text_color="#3b8ed0")
            self.lbl_status.configure(text="System: Ready", text_color="#28a745")
        except Exception as e:
            messagebox.showerror("AI Error", f"Engine failed: {e}")

    def process_eraser(self):
        if not self.input_path: return
        self.lbl_status.configure(text="Cleaning...", text_color="orange")
        self.root.update()
        img = cv2.imread(self.input_path)
        mask = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 248, 255, cv2.THRESH_BINARY)[1]
        dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        temp = "temp_cleaned.png"
        cv2.imwrite(temp, dst)
        self.input_path = temp
        self.lbl_main.configure(text="RESTORED:\nSurface Cleaned", text_color="#3b8ed0")
        self.lbl_status.configure(text="System: Ready", text_color="#28a745")

    def save_final(self):
        if not self.input_path: return
        ext = self.format_var.get().lower()
        target = filedialog.asksaveasfilename(defaultextension=f".{ext}")
        if target:
            img = Image.open(self.input_path)
            if ext in ["jpeg", "jpg"]: img = img.convert("RGB")
            img.save(target, self.format_var.get())
            messagebox.showinfo("Success", "File saved successfully!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageToolkitApp()
    app.run()