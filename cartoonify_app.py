import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Fix for PyInstaller bundling
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class CartoonifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Cartoonify")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # Set window icon (optional)
        try:
            # If you have an icon file, uncomment and adjust this
            # self.root.iconbitmap(resource_path('icon.ico'))
            pass
        except:
            pass
        
        self.image_path = None
        self.original_image = None
        self.cartoon_image = None
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Modern Cartoonify", 
            font=("Helvetica", 28, "bold"), 
            bg="#f0f0f0", 
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Upload button
        self.upload_btn = tk.Button(
            button_frame,
            text="Select Image",
            command=self.upload_image,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.upload_btn.pack(side=tk.LEFT, padx=10)
        
        # Save button (initially disabled)
        self.save_btn = tk.Button(
            button_frame,
            text="Save Cartoon",
            command=self.save_cartoon,
            bg="#2196F3",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=10)
        
        # Cartoon strength slider
        self.slider_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.slider_frame.pack(pady=10)
        
        tk.Label(
            self.slider_frame, 
            text="Cartoon Effect Strength:", 
            font=("Helvetica", 12), 
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.effect_strength = tk.IntVar(value=9)
        self.slider = tk.Scale(
            self.slider_frame,
            from_=5,
            to=15,
            orient=tk.HORIZONTAL,
            variable=self.effect_strength,
            command=self.update_cartoon,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.slider.pack(side=tk.LEFT)
        self.slider.config(state=tk.DISABLED)
        
        # Color strength slider
        self.color_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.color_frame.pack(pady=10)
        
        tk.Label(
            self.color_frame, 
            text="Color Intensity:", 
            font=("Helvetica", 12), 
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.color_strength = tk.IntVar(value=300)
        self.color_slider = tk.Scale(
            self.color_frame,
            from_=100,
            to=500,
            orient=tk.HORIZONTAL,
            variable=self.color_strength,
            command=self.update_cartoon,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.color_slider.pack(side=tk.LEFT)
        self.color_slider.config(state=tk.DISABLED)
        
        # Brightness slider
        self.brightness_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.brightness_frame.pack(pady=10)
        
        tk.Label(
            self.brightness_frame, 
            text="Brightness:", 
            font=("Helvetica", 12), 
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.brightness = tk.DoubleVar(value=0.0)
        self.brightness_slider = tk.Scale(
            self.brightness_frame,
            from_=-50,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.brightness,
            command=self.update_cartoon,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0,
            resolution=0.1
        )
        self.brightness_slider.pack(side=tk.LEFT)
        self.brightness_slider.config(state=tk.DISABLED)
        
        # Contrast slider
        self.contrast_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.contrast_frame.pack(pady=10)
        
        tk.Label(
            self.contrast_frame, 
            text="Contrast:", 
            font=("Helvetica", 12), 
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.contrast = tk.DoubleVar(value=1.0)
        self.contrast_slider = tk.Scale(
            self.contrast_frame,
            from_=0.5,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.contrast,
            command=self.update_cartoon,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0,
            resolution=0.01
        )
        self.contrast_slider.pack(side=tk.LEFT)
        self.contrast_slider.config(state=tk.DISABLED)
        
        # Saturation slider
        self.saturation_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.saturation_frame.pack(pady=10)
        
        tk.Label(
            self.saturation_frame, 
            text="Saturation:", 
            font=("Helvetica", 12), 
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.saturation = tk.DoubleVar(value=1.0)
        self.saturation_slider = tk.Scale(
            self.saturation_frame,
            from_=0.0,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.saturation,
            command=self.update_cartoon,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0,
            resolution=0.01
        )
        self.saturation_slider.pack(side=tk.LEFT)
        self.saturation_slider.config(state=tk.DISABLED)
        
        # Image display frame
        self.display_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Select an image to begin")
        self.status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#e0e0e0"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def upload_image(self):
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
        self.image_path = filedialog.askopenfilename(filetypes=file_types)
        
        if not self.image_path:
            return
            
        try:
            self.original_image = cv2.imread(self.image_path)
            if self.original_image is None:
                messagebox.showerror("Error", "Unable to read the image file.")
                return
                
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            
            # Enable controls
            self.slider.config(state=tk.NORMAL)
            self.color_slider.config(state=tk.NORMAL)
            self.brightness_slider.config(state=tk.NORMAL)
            self.contrast_slider.config(state=tk.NORMAL)
            self.saturation_slider.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
            
            self.update_cartoon()
            self.status_var.set(f"Image loaded: {os.path.basename(self.image_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def update_cartoon(self, event=None):
        if self.original_image is None:
            return
            
        try:
            # Get current parameter values
            edge_strength = self.effect_strength.get()
            color_value = self.color_strength.get()
            brightness = self.brightness.get()
            contrast = self.contrast.get()
            saturation = self.saturation.get()
            
            # Clear previous display
            for widget in self.display_frame.winfo_children():
                widget.destroy()
                
            # Create cartoon image
            self.cartoon_image = self.cartoonify(
                self.original_image, 
                edge_strength, 
                color_value,
                brightness,
                contrast,
                saturation
            )
            
            if self.cartoon_image is None:
                self.status_var.set("Error: Failed to generate cartoon image.")
                return
                
            # Create figure for display
            fig = plt.figure(figsize=(12, 6))
            
            # Add original image
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.imshow(self.original_image)
            ax1.set_title("Original Image")
            ax1.axis('off')
            
            # Add cartoon image
            ax2 = fig.add_subplot(1, 2, 2)
            ax2.imshow(self.cartoon_image)
            ax2.set_title("Cartoon Image")
            ax2.axis('off')
            
            # Adjust layout to prevent cut-off
            plt.tight_layout()
            
            # Display in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.display_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
            canvas.draw()
            
            # Update status bar with current settings
            self.status_var.set(
                f"Effect: {edge_strength} | Color: {color_value} | " +
                f"Brightness: {brightness:.1f} | Contrast: {contrast:.2f} | Saturation: {saturation:.2f}"
            )
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to update cartoon: {str(e)}")
        
    def cartoonify(self, image, edge_strength=9, color_strength=300, brightness=0, contrast=1.0, saturation=1.0):
        try:
            # Apply brightness and contrast adjustments
            adjusted = np.clip(image * contrast + brightness, 0, 255).astype(np.uint8)
            
            # Apply saturation adjustment
            if saturation != 1.0:
                hsv = cv2.cvtColor(adjusted, cv2.COLOR_RGB2HSV).astype(np.float32)
                h, s, v = cv2.split(hsv)
                s = np.clip(s * saturation, 0, 255)
                hsv_merged = cv2.merge([h, s, v])
                adjusted = cv2.cvtColor(hsv_merged.astype(np.uint8), cv2.COLOR_HSV2RGB)
            
            # Convert to grayscale
            gray = cv2.cvtColor(adjusted, cv2.COLOR_RGB2GRAY)
            
            # Apply median blur
            gray_blur = cv2.medianBlur(gray, 5)
            
            # Fix for even values: make sure block sizes are odd for adaptiveThreshold
            # If edge_strength is even, add 1 to make it odd
            if edge_strength % 2 == 0:
                edge_strength += 1
                
            # Create edge mask
            edges = cv2.adaptiveThreshold(
                gray_blur, 
                255, 
                cv2.ADAPTIVE_THRESH_MEAN_C, 
                cv2.THRESH_BINARY, 
                edge_strength, 
                edge_strength
            )
            
            # Apply bilateral filter for cartoon effect
            color = cv2.bilateralFilter(adjusted, 9, color_strength, color_strength)
            
            # Combine color image with edges
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            
            return cartoon
            
        except Exception as e:
            # If there's an error, log it and return the original image
            print(f"Error in cartoonify: {str(e)}")
            self.status_var.set(f"Error: {str(e)}. Using original image.")
            return image
        
    def save_cartoon(self):
        if self.cartoon_image is None:
            messagebox.showwarning("Warning", "No cartoon image to save.")
            return
            
        # Get save path
        file_types = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=file_types,
            initialdir=os.path.dirname(self.image_path) if self.image_path else None,
            initialfile="cartoonified_image"
        )
        
        if not save_path:
            return
            
        try:
            # Convert RGB to BGR for cv2.imwrite
            save_image = cv2.cvtColor(self.cartoon_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(save_path, save_image)
            self.status_var.set(f"Image saved: {os.path.basename(save_path)}")
            messagebox.showinfo("Success", f"Cartoon image saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")

# Error handling for matplotlib backend
def excepthook(type, value, traceback):
    print(f"Uncaught exception: {value}")
    messagebox.showerror("Error", f"An unexpected error occurred: {value}")
    sys.__excepthook__(type, value, traceback)

if __name__ == "__main__":
    # Set up exception handler
    sys.excepthook = excepthook
    
    # Set matplotlib backend (prevents backend switching issues)
    plt.switch_backend('TkAgg')
    
    # Create splash screen (optional)
    """
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)
    splash_root.geometry("400x200+{}+{}".format(
        int(splash_root.winfo_screenwidth()/2 - 200),
        int(splash_root.winfo_screenheight()/2 - 100)
    ))
    splash_label = tk.Label(splash_root, text="Loading Modern Cartoonify...", font=("Helvetica", 18))
    splash_label.pack(expand=True, fill=tk.BOTH)
    splash_root.update()
    """
    
    # Start main application
    root = tk.Tk()
    app = CartoonifyApp(root)
    
    # Close splash screen (if used)
    # splash_root.destroy()
    
    root.mainloop()
