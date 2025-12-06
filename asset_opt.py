import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

class GameAssetOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Texture Optimizer")
        self.root.geometry("600x400")
        self.root.configure(bg="#2d2d2d")

        style = ttk.Style()
        style.theme_use('clam')

        lbl_title = tk.Label(root, text="Game Asset Pipeline Tool", bg="#2d2d2d", fg="white", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=20)

        self.btn_select = tk.Button(root, text="Select Texture Folder", command=self.select_folder, bg="#00ff88", width=20)
        self.btn_select.pack(pady=10)

        self.lbl_status = tk.Label(root, text="Waiting for input...", bg="#2d2d2d", fg="#aaaaaa")
        self.lbl_status.pack(pady=5)

        frame_opts = tk.Frame(root, bg="#2d2d2d")
        frame_opts.pack(pady=20)

        tk.Label(frame_opts, text="Target Resolution:", bg="#2d2d2d", fg="white").pack(side=tk.LEFT, padx=10)
        self.res_var = tk.StringVar(value="512")
        self.combo = ttk.Combobox(frame_opts, textvariable=self.res_var, values=["256", "512", "1024", "2048"])
        self.combo.pack(side=tk.LEFT)

        self.btn_run = tk.Button(root, text="RUN OPTIMIZATION BATCH", command=self.run_batch, bg="#ff4444", fg="white", font=("Arial", 10, "bold"))
        self.btn_run.pack(pady=20)

        self.log_text = tk.Text(root, height=8, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, padx=10, pady=10)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.lbl_status.config(text=f"Selected: {self.folder_path}")
            self.log(f"[SYSTEM] Pipeline targeted: {self.folder_path}")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def run_batch(self):
        if not hasattr(self, 'folder_path'):
            messagebox.showerror("Error", "Select a folder first.")
            return

        target_size = int(self.res_var.get())
        self.log(f"[BATCH] Starting optimization to {target_size}x{target_size}...")

        count = 0
        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tga')):
                try:
                    path = os.path.join(self.folder_path, filename)
                    img = Image.open(path)
                    img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
                    new_name = f"OPT_{filename.split('.')[0]}.png"
                    save_path = os.path.join(self.folder_path, "Optimized", new_name)

                    os.makedirs(os.path.join(self.folder_path, "Optimized"), exist_ok=True)
                    img.save(save_path, "PNG", optimize=True)

                    self.log(f"[SUCCESS] Processed: {filename} -> {new_name}")
                    count += 1
                except Exception as e:
                    self.log(f"[ERROR] Failed {filename}: {str(e)}")

        self.log(f"[COMPLETE] Batch finished. {count} assets optimized.")
        messagebox.showinfo("Pipeline Complete", f"Optimized {count} assets successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameAssetOptimizer(root)
    root.mainloop()