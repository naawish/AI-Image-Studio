import os
import threading
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox
from rembg import remove
from tkinterdnd2 import DND_FILES, TkinterDnD

# Shadcn Zinc Palette
ZINC_950 = "#09090b"  # Deep Background
ZINC_900 = "#18181b"  # Surface
ZINC_800 = "#27272a"  # Border
ZINC_400 = "#a1a1aa"  # Muted text
ACCENT   = "#ffffff"  # Primary Button

class ImageStudio(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Image Studio v2.0")
        self.geometry("1100x750")
        self.configure(bg=ZINC_950)
        
        self.input_path = None
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color=ZINC_900, corner_radius=0, border_width=1, border_color=ZINC_800)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="AI Studio", font=("Inter", 24, "bold"), text_color="#fff").pack(pady=40)

        # Controls
        ctrl_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        ctrl_box.pack(fill="x", padx=30)

        ctk.CTkLabel(ctrl_box, text="ENHANCEMENTS", font=("Inter", 11, "bold"), text_color=ZINC_400).pack(anchor="w")
        self.bg_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(ctrl_box, text="Remove Background", variable=self.bg_var, progress_color="#3b82f6").pack(pady=20, anchor="w")

        ctk.CTkLabel(ctrl_box, text="EXPORT FORMAT", font=("Inter", 11, "bold"), text_color=ZINC_400).pack(anchor="w", pady=(10, 5))
        self.fmt = ctk.CTkOptionMenu(ctrl_box, values=["PNG", "JPEG", "WEBP", "BMP", "TIFF", "PDF"], fg_color=ZINC_800, button_color=ZINC_800, hover_color="#3f3f46")
        self.fmt.pack(fill="x")

        self.btn = ctk.CTkButton(self.sidebar, text="Export Image", fg_color=ACCENT, text_color=ZINC_950, hover_color="#e4e4e7", font=("Inter", 14, "bold"), height=45, command=self.start_thread)
        self.btn.pack(side="bottom", fill="x", padx=30, pady=40)

        # Main Workspace
        self.main = ctk.CTkFrame(self, fg_color=ZINC_950)
        self.main.pack(side="right", expand=True, fill="both", padx=50, pady=50)

        self.drop_zone = ctk.CTkFrame(self.main, fg_color=ZINC_900, border_width=1, border_color=ZINC_800, corner_radius=16)
        self.drop_zone.pack(expand=True, fill="both")
        
        self.preview_lbl = ctk.CTkLabel(self.drop_zone, text="Drag image here or click to browse", text_color=ZINC_400, font=("Inter", 14))
        self.preview_lbl.pack(expand=True, fill="both")

        # Drag & Drop Binding
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', lambda e: self.load_image(e.data.strip('{}')))
        self.preview_lbl.bind("<Button-1>", lambda e: self.manual_load())

    def manual_load(self):
        path = filedialog.askopenfilename()
        if path: self.load_image(path)

    def load_image(self, path):
        self.input_path = path
        img = Image.open(path)
        img.thumbnail((700, 500))
        self.ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self.preview_lbl.configure(image=self.ctk_img, text="")

    def start_thread(self):
        if not self.input_path: return
        self.btn.configure(state="disabled", text="AI Processing...")
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        try:
            img = Image.open(self.input_path)
            if self.bg_var.get():
                img = remove(img)
            
            ext = self.fmt.get()
            save_path = filedialog.asksaveasfilename(defaultextension=f".{ext.lower()}")
            
            if save_path:
                if ext in ["JPEG", "JPG"] and img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(save_path, ext)
                messagebox.showinfo("Success", "Saved successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.btn.configure(state="normal", text="Export Image")

if __name__ == "__main__":
    app = ImageStudio()
    app.mainloop()