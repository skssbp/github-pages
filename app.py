import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

# Subject Mapping
subnm = {
    '301': 'ENG',
    '042': 'PHY',
    '043': 'CHEM',
    '044': 'BIO',
    '048': 'PHE',
    '835': 'MMS',
    '041': 'MTH',
    '049': 'PAINT',
    '083': 'COMP',
    '030': 'ECO',
    '054': 'BST',
    '055': 'ACCT',
    '811': 'BNK',
    '028': 'POLSC',
    '029': 'GEO',
    '039': 'SOCIO',
    '027': 'HIST',
    '034': 'MUSIC',
    '302': 'HINDI-C'
}


class ResultConverter:

    def __init__(self, filepath):
        self.filepath = filepath
        self.output_dir = os.path.splitext(filepath)[0]

        # Create output folder
        os.makedirs(self.output_dir, exist_ok=True)

    def create_header(self):

        data = {
            'RN': '',
            'NAME': ''
        }

        with open(self.filepath, 'r', encoding='utf-8') as file:

            for line in file:

                b = line.split()

                if b and b[0].isdigit() and int(b[0]) > 100:

                    if '301' in b:

                        subjects = b[b.index('301'):]

                        for sub in subjects:

                            if sub.isdigit() and sub in subnm:
                                data[subnm[sub]] = ''

        data['TOT'] = ''
        data['PER'] = ''
        data['RESULT'] = ''
        data['6thSUB'] = ''

        csv_path = os.path.join(self.output_dir, 'xiiall.csv')

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:

            writer = csv.writer(f)

            writer.writerow(list(data.keys()))

        return data

    def convert(self):

        csv_path = os.path.join(self.output_dir, 'xiiall.csv')

        base_data = self.create_header()

        with open(self.filepath, 'r', encoding='utf-8') as txtfile, \
                open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:

            writer = csv.writer(csvfile)

            while True:

                line = txtfile.readline()

                if not line:
                    break

                b = line.split()

                if b and b[0].isdigit() and int(b[0]) >= 100:

                    row_data = base_data.copy()

                    row_data['RN'] = b[0]

                    row_data['NAME'] = ' '.join(
                        b[2:b.index('301')]
                    )

                    subjects = b[b.index('301'):]

                    marks_line = txtfile.readline().split()

                    marks = [
                        s for s in marks_line
                        if s.isdigit()
                    ]

                    if len(marks) >= 5:

                        total = sum(
                            map(int, marks[:5])
                        )

                        percent = total / 5

                    else:

                        total = 0
                        percent = 0

                    for sub, mark in zip(subjects, marks):

                        if sub in subnm:

                            row_data[subnm[sub]] = mark

                    if subjects[-1].isdigit():

                        row_data['RESULT'] = (
                            'COMP ' + subjects[-1]
                        )

                    else:

                        row_data['RESULT'] = subjects[-1]

                    row_data['TOT'] = total
                    row_data['PER'] = percent

                    if len(marks) == 6:

                        row_data['6thSUB'] = subnm.get(
                            subjects[len(marks) - 1],
                            ''
                        )

                    writer.writerow(
                        list(row_data.values())
                    )


# ================= GUI ================= #

def browse_file():

    filepath = filedialog.askopenfilename(
        title='Select TXT File',
        filetypes=[('Text Files', '*.txt')]
    )

    if filepath:

        file_entry.delete(0, tk.END)

        file_entry.insert(0, filepath)


def convert_file():

    filepath = file_entry.get().strip()

    if not filepath:

        messagebox.showerror(
            'Error',
            'Please select a TXT file.'
        )

        return

    if not os.path.exists(filepath):

        messagebox.showerror(
            'Error',
            'File not found.'
        )

        return

    try:

        converter = ResultConverter(filepath)

        converter.convert()

        messagebox.showinfo(
            'Success',
            f'CSV created successfully.\n\n'
            f'Output Folder:\n{converter.output_dir}'
        )

    except Exception as e:

        messagebox.showerror(
            'Error',
            str(e)
        )


# ================= MAIN WINDOW ================= #

root = tk.Tk()

root.title('TXT to CSV Converter')

root.geometry('650x220')

root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text='CBSE TXT to CSV Converter',
    font=('Arial', 16, 'bold')
)

heading.pack(pady=20)

# Frame
frame = tk.Frame(root)

frame.pack(pady=10)

# Entry
file_entry = tk.Entry(
    frame,
    width=60
)

file_entry.grid(
    row=0,
    column=0,
    padx=10
)

# Browse Button
browse_btn = tk.Button(
    frame,
    text='Browse',
    width=12,
    command=browse_file
)

browse_btn.grid(
    row=0,
    column=1
)

# Convert Button
convert_btn = tk.Button(
    root,
    text='Convert to CSV',
    width=20,
    height=2,
    command=convert_file
)

convert_btn.pack(pady=25)

root.mainloop()
