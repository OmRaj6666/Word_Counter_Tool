"""A tkinter-based word count tool for counting lines, words, bytes, and characters in files."""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

def count_file(filepath, options):
    """Count lines, words, bytes, and characters in a file based on options."""
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read()
    counts = {}
    if options['bytes']:
        counts['bytes'] = len(data.encode('utf-8'))
    if options['lines']:
        counts['lines'] = data.count('\n')
    if options['words']:
        counts['words'] = len(data.split())
    if options['chars']:
        counts['chars'] = len(data)
    return counts

def format_output(counts, filename):
    """Format the output string for the counted values."""
    if len(counts) == 1:
        key = list(counts.keys())[0]
        return (
            f"{key.capitalize()}: {counts[key]} "
            f"({os.path.basename(filename)})"
        )
    return (
        f"Lines: {counts.get('lines', 0)}\n"
        f"Words: {counts.get('words', 0)}\n"
        f"Bytes: {counts.get('bytes', 0)}\n"
        f"Chars: {counts.get('chars', 0)}\n"
        f"File: {os.path.basename(filename)}"
    )

class ccwc_app(tk.Tk):
    """Main application class for the word count tool."""
    def __init__(self):
        super().__init__()
        self.title(
            "CCWC - Word Count Tool"
        )
        self.geometry(
            "400x400"
        )
        self.filepaths = []

        self.options = {
            'bytes': tk.BooleanVar(
                value=True
            ),
            'lines': tk.BooleanVar(
                value=True
            ),
            'words': tk.BooleanVar(
                value=True
            ),
            'chars': tk.BooleanVar(
                value=False
            )
        }

        tk.Button(
            self,
            text="Add Files",
            command=self.add_files
        ).pack(
            pady=10
        )
        self.selected_files_label = tk.Label(
            self,
            text="No files selected"
        )
        self.selected_files_label.pack(
            pady=5
        )
        tk.Checkbutton(
            self,
            text="Count Bytes",
            variable=self.options['bytes']
        ).pack(
            anchor='w'
        )
        tk.Checkbutton(
            self,
            text="Count Lines",
            variable=self.options['lines']
        ).pack(
            anchor='w'
        )
        tk.Checkbutton(
            self,
            text="Count Words",
            variable=self.options['words']
        ).pack(
            anchor='w'
        )
        tk.Checkbutton(
            self,
            text="Count Characters",
            variable=self.options['chars']
        ).pack(
            anchor='w'
        )
        tk.Button(
            self,
            text="Count",
            command=self.run_count
        ).pack(
            pady=10
        )
        self.result = tk.Text(
            self,
            height=12,
            width=40
        )
        self.result.pack(
            pady=10
        )

    def add_files(self):
        """Open file dialog and add selected files to the list."""
        files = filedialog.askopenfilenames(
            title="Select files"
        )
        if files:
            self.filepaths.extend(files)
            self.selected_files_label.config(
                text="Selected files:\n" +
                "\n".join(
                    os.path.basename(f)
                    for f in self.filepaths
                )
            )
            self.result.delete(
                1.0,
                tk.END
            )
            self.result.insert(
                tk.END,
                "Selected files:\n"
            )
            for f in self.filepaths:
                self.result.insert(
                    tk.END,
                    f"{os.path.basename(f)}\n"
                )

    def run_count(self):
        """Run the count operation on selected files."""
        if not self.filepaths:
            messagebox.showerror(
                "Error",
                "No files selected!"
            )
            return
        opts = {
            k: v.get()
            for k, v in self.options.items()
        }
        if not any(opts.values()):
            opts['bytes'] = True
            opts['lines'] = True
            opts['words'] = True
        self.result.delete(
            1.0,
            tk.END
        )
        for filepath in self.filepaths:
            counts = count_file(
                filepath,
                opts
            )
            output = format_output(
                counts,
                filepath
            )
            self.result.insert(
                tk.END,
                output + "\n\n"
            )

if __name__ == '__main__':
    app = ccwc_app()
    app.mainloop()
