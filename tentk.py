import tkinter as tk
import tkmacosx
from math import log as ln
import math

ON = '#2F5596'  # not well named. ON applies to all selected buttons, entry background and calculate button
OFF = '#4472C4' # applies to background and all widgets of same color
BORDER = '#5590D0'
def toggle_btn(self):
    # better would be to subclass btns and add a pressed attribute
    if self.cget("bg") == OFF:
        self.config(bg = ON)
    else:
        self.config(bg= OFF)
def calculate():
    # get data entered and populate dict
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
    # coefficients are stored in a dict of 4 dicts one for each sex/race combination
    sex = sex_var.get()
    race = race_var.get()
    demographic = race + '_' + sex
    selected = coefficients[demographic]
    # multiply each variable by its coefficient and sum to get individual result
    individual = sum( value * coefficient for value, coefficient in zip(risk_profile.values(), selected.values()))
    mean = selected['mean']
    base = selected['base']
    result = ((1 - (base ** (math.e**(individual-mean)))) * 100)
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
root.minsize(500, 650)
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)

frm_title = tk.Frame(root,  bd = 3, bg = OFF)
frm_content = tk.Frame(root, bd = 3,background = OFF )
frm_data = tk.Frame(frm_content, bd = 3, background = OFF )

lbl_frm_sex = tk.LabelFrame(frm_content, text = 'sex', bd = 1, bg = OFF)
lbl_frm_race = tk.LabelFrame(frm_content, text = 'race', bd = 1, bg = OFF)
lbl_frm_history = tk.LabelFrame(frm_content, text = 'history', bd = 1, bg = OFF)

race_var = tk.StringVar()
sex_var = tk.StringVar()

lbl_font = tk.font.Font(size=20)
lbl_lg_font = tk.font.Font(size=24)

rbtn_male = tkmacosx.Radiobutton(lbl_frm_sex, text = 'male', value = 'male', pady = 10, padx = 27,
                                variable = sex_var, indicatoron = 0, bg = OFF,
                                 selectcolor = ON, bd = 1)
rbtn_female = tkmacosx.Radiobutton(lbl_frm_sex, text = 'female', value = 'female', pady = 10, padx = 26,
                                variable = sex_var, indicatoron = 0, bg = OFF,
                                 selectcolor = ON, bd = 1)
rbtn_white = tkmacosx.Radiobutton(lbl_frm_race, text = 'white', value = 'white', padx = 26, pady = 10,
                                 variable = race_var, indicatoron = 0, bg = OFF,
                                 selectcolor = ON, bd = 1)
rbtn_aa = tkmacosx.Radiobutton(lbl_frm_race, text = 'African-American', value = 'black', padx = 15, pady = 10,
                                 variable = race_var, indicatoron = 0, bg = OFF,
                                 selectcolor = ON, bd = 1)
rbtn_other = tkmacosx.Radiobutton(lbl_frm_race, text = 'other', value = 'white', padx = 26, pady = 10,
                                 variable = race_var, indicatoron = 0, bg = OFF,
                                 selectcolor = ON, bd = 1)

btn_smoker = tkmacosx.Button(lbl_frm_history, text = "smoker", bg = OFF, pady = 5, fg = 'white',
                             activebackground = '#619CCD', command = lambda: toggle_btn(btn_smoker),
                             bordercolor = BORDER, bd = 1)

btn_diabetic = tkmacosx.Button(lbl_frm_history, text = 'diabetic', bg = OFF, pady = 5, fg = 'white',
                               activebackground = '#619CCD', command = lambda: toggle_btn(btn_diabetic),
                             bordercolor = BORDER, bd = 1)
btn_htn = tkmacosx.Button(lbl_frm_history, text = "treated htn", bg = OFF, pady = 5, fg = 'white',
                          activebackground = '#619CCD', command = lambda: toggle_btn(btn_htn),
                             bordercolor = BORDER, bd = 1)
btn_calculate = tkmacosx.Button(frm_data, text = "calculate", bg = ON , pady = 5, fg = 'white',
                                command = calculate, bordercolor = BORDER)

entry_age = tk.Entry(frm_data, width = 7, bg = ON, highlightbackground = OFF, bd = 1, relief = tk.FLAT)
entry_sbp = tk.Entry(frm_data, width = 7, bg = ON, highlightbackground = OFF, bd = 1, relief = tk.FLAT)
entry_tchol = tk.Entry(frm_data, width = 7, bg = ON, highlightbackground = OFF, bd = 1, relief = tk.FLAT)
entry_hdl = tk.Entry(frm_data, width = 7, bg = ON, highlightbackground = OFF, bd = 1, relief = tk.FLAT)

lbl_title = tk.Label(frm_title, text = "10 Year Cardiovascular Risk Calculator",
                     font = lbl_font, bg = OFF, pady = 15)
lbl_age = tk.Label(frm_data, text = "age: ", bg = OFF)
lbl_sbp = tk.Label(frm_data, text = "systolic BP: ", bg = OFF)
lbl_tchol = tk.Label(frm_data, text = "total cholesterol: ", bg = OFF)
lbl_hdl = tk.Label(frm_data, text = "hdl cholesterol: ", bg = OFF)
lbl_result = tk.Label(frm_data, text = "10 year cv risk: ",
                     font = lbl_font, bg = OFF)
txt_result = tk.Label(frm_data, text = "",
                     font = lbl_lg_font, fg = '#00ff00', bg = OFF)

frm_title.grid(row = 0, column = 0, sticky = 'ew')
frm_content.grid(row = 1, column = 0, sticky = 'nsew')
frm_data.grid(row = 3,  column = 0, pady = 10, padx = 50)

lbl_frm_sex.grid(row = 0, column = 0, columnspan = 3, sticky = 'ew', pady = 10,  padx = 50)
lbl_frm_race.grid(row = 1, column = 0, columnspan = 3, sticky = 'ew', pady = 10, padx = 50)
lbl_frm_history.grid(row = 2, column = 0, columnspan = 3, sticky = 'ew', pady = 10, padx = 50)

rbtn_male.grid(row = 0, column = 0, padx = (10,5), pady = 10)
rbtn_female.grid(row = 0, column = 1, padx = 5, pady =10 )
rbtn_white.grid(row = 1, column = 0, padx = (10,5), pady = 10)
rbtn_aa.grid(row = 1, column = 1, padx = 5, pady = 10)
rbtn_other.grid(row = 1, column = 2, padx = (5, 10), pady = 10)
btn_diabetic.grid(row = 2, column = 0, padx = (10,5), pady = 10)
btn_htn.grid(row = 2, column = 1, padx = 5, pady = 10)
btn_smoker.grid(row = 2, column = 2, padx = (5, 10), pady = 10)

entry_age.grid(row = 0, column = 1, padx = 5, pady= 10, sticky = 'w')
entry_sbp.grid(row = 1, column = 1, padx = 5, pady= 10, sticky = 'w')
entry_tchol.grid(row = 2, column = 1, padx = 5, pady= 10, sticky = 'w')
entry_hdl.grid(row = 3, column = 1, padx = 5, pady= 10, sticky = 'w')

lbl_title.grid(row = 0, column = 0, padx = (75, 25))
lbl_age.grid(row = 0, column = 0, sticky = 'e')
lbl_sbp.grid(row = 1, column = 0, sticky = 'e')
lbl_tchol.grid(row = 2, column = 0, sticky = 'e')
lbl_hdl.grid(row = 3, column = 0, sticky = 'e')
btn_calculate.grid(row = 4, column = 1, pady= 20)
lbl_result.grid(row = 5, column = 0, padx= (5,0), pady = (0,30), sticky = 'e')
txt_result.grid(row = 5, column = 1, pady = (0, 30), sticky = 'w')

root.mainloop()