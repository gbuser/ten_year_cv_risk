import tkinter as tk
import tkmacosx
from math import log as ln
import math

ON = '#619CCD'
OFF = '#18354C'
def toggle_btn(self):
    if self.cget("bg") == OFF:
        self.config(bg = ON)
    else:
        self.config(bg= OFF)
def calculate():
    sex = sex_var.get()
    race = race_var.get()
    demographic = race + '_' + sex
    htn = 0 if btn_htn.cget("bg") == OFF else 1
    # risk_profile items match items in coefficients
    # interim calculation step requires sum of each product of coefficient * value
    risk_profile = {'age': (age := ln(int(entry_age.get()))),
                    'age_squared': age * age,
                    'tchol': (tchol := ln(int(entry_tchol.get()))),
                    'age*tchol': age * tchol,
                    'hdl': (hdl := ln(int(entry_hdl.get()))),
                    'age*hdl': age * hdl,
                    'treatedSBP': (treatedSBP := ln(int(entry_sbp.get())) if htn else 0),
                    'age*treatedSBP': age * treatedSBP,
                    'untreatedSBP': (untreatedSBP := ln(int(entry_sbp.get())) if not htn else 0),
                    'age*untreatedSBP': age * untreatedSBP,
                    'smoker': (smoker := 0 if btn_smoker.cget("bg") == OFF else 1),
                    'age*smoker': age * smoker,
                    'diabetic': 0 if btn_diabetic.cget("bg") == OFF else 1
    }

    print(*risk_profile.items(), sep = '\n')
    selected = coefficients[demographic]
    individual = sum( value * coefficient for value, coefficient in zip(risk_profile.values(), selected.values()))
    print (f'individual: {individual}')
    mean = selected['mean']
    base = selected['base']
    result = ((1 - (base ** (math.e**(individual-mean)))) * 100)
    print(result)
    color = 'red' if result >= 7.5 else '#00ff00'
    txt_result.config(text = f'{result:.1f}%',   fg = color)
file = "tenyrdata"
data = open(file, 'r').readlines()
data = [line.strip().split(',') for line in data]
keys = data[0][2:]  # keys = variable labels after sex and race
coefficients = {}
# create a dict of 4 dicts, one for each sex/race combination
# in each dict, keys, vals are variable label and coefficients
for line in data[1:]:
    vals = [float(x) for x in line[2:]]
    coefficients[f'{line[1]}_{line[0]}'] = dict(zip(keys,vals))

root = tk.Tk()
root.minsize(400,600)
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)
frm_title = tk.Frame(root,  bd = 3, bg = '#002855')
frm_content = tk.Frame(root, bd = 3,background = '#002855' )

race_var = tk.StringVar()
sex_var = tk.StringVar()
lbl_font = tk.font.Font(size=20)
lbl_lg_font = tk.font.Font(size=24)

rbtn_male = tkmacosx.Radiobutton(frm_content, text = 'male', value = 'male', pady = 5,
                                variable = sex_var, indicatoron = 0, bg = '#18354C',
                                 selectcolor = '#619CCD')
rbtn_female = tkmacosx.Radiobutton(frm_content, text = 'female', value = 'female', pady = 5,
                                variable = sex_var, indicatoron = 0, bg = '#18354C',
                                 selectcolor = '#619CCD')
rbtn_white = tkmacosx.Radiobutton(frm_content, text = 'white', value = 'white', pady = 5,
                                 variable = race_var, indicatoron = 0, bg = '#18354C',
                                 selectcolor = '#619CCD')
rbtn_aa = tkmacosx.Radiobutton(frm_content, text = 'African-American', value = 'black', pady = 5,
                                 variable = race_var, indicatoron = 0, bg = '#18354C',
                                 selectcolor = '#619CCD')
rbtn_other = tkmacosx.Radiobutton(frm_content, text = 'other', value = 'white', pady = 5,
                                 variable = race_var, indicatoron = 0, bg = '#18354C',
                                 selectcolor = '#619CCD')

btn_smoker = tkmacosx.Button(frm_content, text = "smoker", bg = '#18354C', pady = 5, fg = 'white',
                             activebackground = '#619CCD', command = lambda: toggle_btn(btn_smoker))
btn_diabetic = tkmacosx.Button(frm_content, text = 'diabetic', bg = '#18354C', pady = 5, fg = 'white',
                               activebackground = '#619CCD', command = lambda: toggle_btn(btn_diabetic))
btn_htn = tkmacosx.Button(frm_content, text = "treated htn", bg = '#18354C', pady = 5, fg = 'white',
                          activebackground = '#619CCD', command = lambda: toggle_btn(btn_htn))
btn_calculate = tkmacosx.Button(frm_content, text = "calculate", bg = '#18354C', pady = 5, fg = 'white',
                                command = calculate)
entry_age = tk.Entry(frm_content, width = 7, bg = '#18354C', bd = 1)
entry_tchol = tk.Entry(frm_content, width = 7, bg = '#18354C')
entry_hdl = tk.Entry(frm_content, width = 7, bg = '#18354C')
entry_sbp = tk.Entry(frm_content, width = 7, bg = '#18354C')
lbl_title = tk.Label(frm_title, text = "10 Year Cardiovascular Risk Calculator",
                     font = lbl_font, bg = '#002855')
lbl_age = tk.Label(frm_content, text = "age: ", bg = '#002855')
lbl_tchol = tk.Label(frm_content, text = "total cholesterol: ", bg = '#002855')
lbl_hdl = tk.Label(frm_content, text = "hdl cholesterol: ", bg = '#002855')
lbl_sbp = tk.Label(frm_content, text = "systolic BP: ", bg = '#002855')
lbl_result = tk.Label(frm_content, text = "10 year cv risk: ",
                     font = lbl_font, bg = '#002855')
txt_result = tk.Label(frm_content, text = "",
                     font = lbl_lg_font, fg = '#00ff00', bg = '#002855')


frm_title.grid(row = 0, column = 0, sticky = 'ew')
frm_content.grid(row = 1, column = 0, sticky = 'nsew')
rbtn_male.grid(row = 0, column = 0, pady = 10)
rbtn_female.grid(row = 0, column = 1, pady =10 )
rbtn_white.grid(row = 1, column = 0, pady = 10)
rbtn_aa.grid(row = 1, column = 1, pady = 10)
rbtn_other.grid(row = 1, column = 2, pady = 10)
btn_diabetic.grid(row = 2, column = 0, pady = 10)
btn_htn.grid(row = 2, column = 1, pady = 10)
btn_smoker.grid(row = 2, column = 2, pady = 10)
entry_age.grid(row = 3, column = 1, padx = 5, pady= 10, sticky = 'w')
entry_tchol.grid(row = 5, column = 1, padx = 5, pady= 10, sticky = 'w')
entry_hdl.grid(row = 6, column = 1, padx = 5, pady= 10, sticky = 'w')
entry_sbp.grid(row = 4, column = 1, padx = 5, pady= 10, sticky = 'w')
lbl_title.grid(row = 0, column = 0, padx = (25, 0))
lbl_age.grid(row = 3, column = 0, sticky = 'e')
lbl_tchol.grid(row = 5, column = 0, sticky = 'e')
lbl_hdl.grid(row = 6, column = 0, sticky = 'e')
lbl_sbp.grid(row = 4, column = 0, sticky = 'e')
btn_calculate.grid(row = 7, column = 1, pady= 25)
lbl_result.grid(row = 8, column = 0, padx= (25,0))
txt_result.grid(row = 8, column = 1, sticky = 'w')
root.mainloop()