import os
import threading
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox
from rembg import remove
from tkinterdnd2 import DND_FILES, TkinterDnD

# --- Professional Shadcn Zinc Palette ---
ZINC_950 = "#09090b"  # Deep Background
ZINC_900 = "#18181b"  # Card Surface
ZINC_800 = "#27272a"  # Border/Dropdowns
ZINC_400 = "#a1a1aa"  # Muted secondary text
ACCENT   = "#ffffff"  # Primary Action Button

class ImageStudio(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        # Window Configuration
        self.title("AI Image Studio v2.0")
        self.geometry("1100x750")
        self.configure(bg=ZINC_950)
        
        # System state
        self.input_path = None
        self.ctk_img = None
        
        self.setup_ui()

    def setup_ui(self):
        # 1. Sidebar (Controls)
        self.sidebar = ctk.CTkFrame(
            self, width=300, fg_color=ZINC_900, 
            corner_radius=0, border_width=1, border_color=ZINC_800
        )
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar, text="AI Studio", 
            font=("Inter", 26, "bold"), text_color="#ffffff"
        ).pack(pady=40)

        # Controls Container
        ctrl_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        ctrl_box.pack(fill="x", padx=30)

        # AI Switch
        ctk.CTkLabel(
            ctrl_box, text="ENHANCEMENTS", 
            font=("Inter", 11, "bold"), text_color=ZINC_400
        ).pack(anchor="w")
        
        self.bg_var = ctk.BooleanVar(value=False)
        self.bg_switch = ctk.CTkSwitch(
            ctrl_box, text="Remove Background", 
            variable=self.bg_var, progress_color="#3b82f6",
            font=("Inter", 13)
        )
        self.bg_switch.pack(pady=20, anchor="w")

        # Format Dropdown
        ctk.CTkLabel(
            ctrl_box, text="EXPORT FORMAT", 
            font=("Inter", 11, "bold"), text_color=ZINC_400
        ).pack(anchor="w", pady=(10, 5))
        
        self.fmt = ctk.CTkOptionMenu(
            ctrl_box, 
            values=["PNG", "JPEG", "WEBP", "BMP", "TIFF", "PDF"], 
            fg_color=ZINC_800, 
            button_color=ZINC_800, 
            button_hover_color="#3f3f46", # Fixed: used button_hover_color
            dynamic_resizing=False
        )
        self.fmt.pack(fill="x")

        # Export Button (Pinned to Bottom)
        self.btn = ctk.CTkButton(
            self.sidebar, text="Export Image", 
            fg_color=ACCENT, text_color=ZINC_950, 
            hover_color="#e4e4e7", font=("Inter", 14, "bold"), 
            height=45, command=self.start_thread
        )
        self.btn.pack(side="bottom", fill="x", padx=30, pady=40)

        # 2. Main Workspace (Preview)
        self.main = ctk.CTkFrame(self, fg_color=ZINC_950)
        self.main.pack(side="right", expand=True, fill="both", padx=50, pady=50)

        # Drop Zone Card
        self.drop_zone = ctk.CTkFrame(
            self.main, fg_color=ZINC_900, 
            border_width=1, border_color=ZINC_800, 
            corner_radius=16
        )
        self.drop_zone.pack(expand=True, fill="both")
        
        self.preview_lbl = ctk.CTkLabel(
            self.drop_zone, 
            text="Drag image here or click to browse\n(Supports WebP, AVIF, PNG, JPG)", 
            text_color=ZINC_400, font=("Inter", 14)
        )
        self.preview_lbl.pack(expand=True, fill="both")

        # 3. Events & Bindings
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', lambda e: self.load_image(e.data.strip('{}')))
        self.preview_lbl.bind("<Button-1>", lambda e: self.manual_load())

    def manual_load(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.avif *.bmp")]
        )
        if path: self.load_image(path)

    def load_image(self, path):
        """Loads and scales the image for the dynamic UI preview."""
        self.input_path = path
        try:
            img = Image.open(path)
            # Maintain aspect ratio for the preview
            img.thumbnail((700, 500))
            
            self.ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_lbl.configure(image=self.ctk_img, text="")
        except Exception as e:
            messagebox.showerror("Loading Error", f"Could not load image: {e}")

    def start_thread(self):
        """Prevents the UI from freezing during AI processing."""
        if not self.input_path:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
            
        self.btn.configure(state="disabled", text="AI Processing...")
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        try:
            # 1. Run AI/Image Logic
            img = Image.open(self.input_path)
            
            if self.bg_var.get():
                # Note: rembg requires an image in RGBA or RGB
                img = remove(img)
            
            # 2. Handle File Saving
            ext = self.fmt.get()
            save_path = filedialog.asksaveasfilename(
                defaultextension=f".{ext.lower()}",
                filetypes=[(f"{ext} files", f"*.{ext.lower()}")]
            )
            
            if save_path:
                # If JPEG/JPG, remove alpha channel (transparency)
                if ext in ["JPEG", "JPG"] and img.mode == "RGBA":
                    img = img.convert("RGB")
                
                img.save(save_path, ext)
                messagebox.showinfo("Success", f"Image exported as {ext}")
                
        except Exception as e:
            messagebox.showerror("Processing Error", f"Something went wrong: {e}")
        finally:
            # Re-enable the button on the main thread
            self.btn.configure(state="normal", text="Export Image")

if __name__ == "__main__":
    app = ImageStudio()
    app.mainloop()