import tkinter as tk
from tkinter import ttk
import pickle
from tkinter import messagebox
from sklearn.preprocessing import StandardScaler



sc_area = pickle.load(open("sc_area.pkl", "rb"))
sc_price = pickle.load(open("sc_price.pkl", "rb"))
model = pickle.load(open("house_model.pkl", "rb"))

sc=StandardScaler()

root = tk.Tk()
root.title("House Input Form")
root.geometry("500x600")
root.configure(bg="#1a1a1a")

canvas = tk.Canvas(root, bg="#1a1a1a", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)

container = ttk.Frame(canvas)
container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=container, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#1a1a1a", foreground="white", font=("Segoe UI", 11))
style.configure("TFrame", background="#1a1a1a")
style.configure("TEntry",
                fieldbackground="#2d2d2d",
                background="#2d2d2d",
                foreground="white",
                padding=6,
                relief="flat",
                insertcolor="white")
style.configure("TCheckbutton", background="#1a1a1a", foreground="white")


def add_entry(row, col, text):
    lbl = ttk.Label(container, text=text)
    lbl.grid(row=row, column=col, padx=15, pady=10, sticky="w")

    entry = ttk.Entry(container, width=18)
    entry.grid(row=row + 1, column=col, padx=15, sticky="we")

    return entry

def add_bool(row, col, text):
    var = tk.IntVar()
    chk = ttk.Checkbutton(container, text=text, variable=var)
    chk.grid(row=row, column=col, padx=15, pady=8, sticky="w")
    return var



area = add_entry(0, 0, "Area")
bedrooms = add_entry(0, 1, "Bedrooms")

bathrooms = add_entry(2, 0, "Bathrooms")
parking = add_entry(2, 1, "Parking")

stories = add_entry(4, 0, "Stories")

mainroad = add_bool(6, 0, "Main Road")
airconditioning = add_bool(6, 1, "Air Conditioning")

guestroom = add_bool(7, 0, "Guest Room")
basement = add_bool(7, 1, "Basement")

hotwaterheating = add_bool(8, 0, "Hot Water Heating")
prefarea = add_bool(8, 1, "Preferred Area")

# -------------------------------------------------
# Submit Button at Bottom
# -------------------------------------------------
# def submit():
#     data = {
#         "area": int(area.get()),
#         "bedrooms": int(bedrooms.get()),
#         "bathrooms": int(bathrooms.get()),
#         "parking": int(parking.get()),
#         "stories": int(stories.get()),
#         "mainroad": mainroad.get(),
#         "airconditioning": airconditioning.get(),
#         "guestroom": guestroom.get(),
#         "basement": basement.get(),
#         "hotwaterheating": hotwaterheating.get(),
#         "prefarea": prefarea.get()
#     }
#     print("\nUser Input:", data)
def predict_price():
    
    area_val = float(area.get())
    bedrooms_val = int(bedrooms.get())
    bathrooms_val = int(bathrooms.get())
    parking_val = int(parking.get())
    stories_val = int(stories.get())
    mainroad_val = int(mainroad.get())
    airconditioning_val = int(airconditioning.get())
    guestroom_val = int(guestroom.get())
    basement_val = int(basement.get())
    hotwater_val = int(hotwaterheating.get())
    prefarea_val = int(prefarea.get())

    if area_val == "" or bedrooms_val == "" or bathrooms_val == "" or parking_val == "" or stories_val == "":
        messagebox.showwarning("Warning", "Please fill all the fields!")
        return


    
    area_scaled = sc_area.transform([[area_val]])[0][0]

    input_data = [[
        area_scaled, bedrooms_val, bathrooms_val, parking_val,
        stories_val, mainroad_val, airconditioning_val,
        guestroom_val, basement_val, hotwater_val, prefarea_val
    ]]

    # Step 4: Predict (scaled price)
    price_scaled = model.predict(input_data)[0]

    # Step 5: Convert price back to real value
    price_real = sc_price.inverse_transform([[price_scaled]])[0][0]

    messagebox.showinfo("Prediction", f"Predicted Price: {price_real:.2f}")
    print(price_real)

def submit():
  predict_price()
  
submit_btn = tk.Button(
    root,
    text="Submit",
    bg="#0a84ff",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    padx=15,
    pady=10,
    command=submit
)




submit_btn.pack(pady=15)

root.mainloop()
 