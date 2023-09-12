from pathlib import Path

from customtkinter import CTk, CTkFont, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkCheckBox, CTkTextbox, \
    END, DISABLED, NORMAL
from tkinter import filedialog

from utils import make_link


class MainFrame(CTkFrame):
    def __init__(self, master: CTk, elements_font: CTkFont = None) -> None:
        super().__init__(master, fg_color="transparent")
        self._is_folder = False
        self._is_hard = False
        self.target_path = None
        self.link_path = None

        # Config
        self._elements_font = elements_font

        # Create elements
        self._target_frame = CTkFrame(self, fg_color="transparent")
        self._target_label = CTkLabel(self._target_frame, text="Target", font=self._elements_font)
        self._is_folder_check = \
            CTkCheckBox(self._target_frame, text="Is folder?", command=self.on_check_is_folder, font=self._elements_font)

        self._target_entry = CTkEntry(self, width=100, font=self._elements_font)
        self._target_folder_btn = CTkButton(self, text="Browse", command=self.browse_target, font=self._elements_font)

        self._link_frame = CTkFrame(self, fg_color="transparent")
        self._link_label = CTkLabel(self._link_frame, text="Link", font=self._elements_font)
        self._is_hard_check = \
            CTkCheckBox(self._link_frame, text="Is hard?", command=self.on_check_is_hard, font=self._elements_font)

        self._link_entry = CTkEntry(self, font=self._elements_font)
        self._link_folder_btn = \
            CTkButton(self, text="Browse", command=self.browse_link, font=self._elements_font)

        self._ok_button = CTkButton(self, text="OK", command=self._ok_button_click, font=self._elements_font)
        self._log_output = CTkTextbox(self, state=DISABLED, font=CTkFont("Roboto", 16))

        self._pack_elements()

    def on_check_is_folder(self):
        self._is_folder = not self._is_folder

    def on_check_is_hard(self):
        self._is_hard = not self._is_hard

    def browse_target(self):
        self.target_path = Path(filedialog.askopenfilename()) if not self._is_folder \
            else Path(filedialog.askdirectory())
        self._target_entry.delete(0, END)
        self._target_entry.insert(0, self.target_path)

    def browse_link(self):
        self.link_path = Path(filedialog.askopenfilename()) if not self._is_folder \
            else Path(filedialog.askdirectory())
        self._link_entry.delete(0, END)
        self._link_entry.insert(0, self.link_path)

    def _pack_elements(self) -> None:
        """
        Display all frame elements.
        """
        self._target_frame.pack(fill='x')
        self._target_label.grid(row=1, column=1, padx=5)
        self._is_folder_check.grid(row=1, column=2, padx=20)

        self._target_entry.pack(pady=5, fill='x')
        self._target_folder_btn.pack(pady=5, fill='x')

        self._link_frame.pack(fill='x')
        self._link_label.grid(row=1, column=1, padx=5)
        self._is_hard_check.grid(row=1, column=2, padx=20)

        self._link_entry.pack(pady=5, fill='x')
        self._link_folder_btn.pack(pady=5, fill='x')

        self._ok_button.pack(pady=10)  # y-axis padding = 10px
        self._log_output.pack(pady=5, fill='both')

    def _ok_button_click(self) -> None:
        """
        Put calculation results into the entry.
        """
        target = self._target_entry.get()
        link = self._link_entry.get()
        try:
            make_link(target, link, self._is_hard)
            self._log_output.configure(state=NORMAL)
            self._log_output.delete('1.0', END)
            self._log_output.insert('1.0', "The link was successfully created")
            self._log_output.configure(state=DISABLED)
        except Exception as e:
            self._log_output.configure(state=NORMAL)
            self._log_output.delete('1.0', END)
            self._log_output.insert('1.0', e)
            self._log_output.configure(state=DISABLED)
