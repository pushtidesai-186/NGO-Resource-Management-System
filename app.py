from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB = Path(__file__).with_name("ngo.db")
MODULES = {
 "donors":{"title":"Donors","fields":[("name","Name"),("phone","Phone"),("email","Email"),("donation","Donation / Notes")]},
 "beneficiaries":{"title":"Beneficiaries","fields":[("name","Name"),("phone","Phone"),("need","Required assistance"),("address","Address")]},
 "resources":{"title":"Resources / Inventory","fields":[("item","Resource name"),("quantity","Quantity"),("condition","Condition"),("notes","Notes")]},
 "volunteers":{"title":"Volunteers","fields":[("name","Name"),("phone","Phone"),("skill","Skills"),("availability","Availability")]},
 "interns":{"title":"Internship Students","fields":[("name","Name"),("college","College"),("start_date","Start date"),("activities","Activities / Attendance")]},
 "events":{"title":"Events","fields":[("name","Event name"),("event_date","Date"),("location","Location"),("description","Description")]}
}
def connect():
 con=sqlite3.connect(DB); con.row_factory=sqlite3.Row; return con
def init_db():
 with connect() as con:
  for table,module in MODULES.items():
   cols=", ".join(f'"{f}" TEXT' for f,_ in module["fields"])
   con.execute(f'CREATE TABLE IF NOT EXISTS "{table}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols})')
@app.route("/")
def dashboard():
 counts={}
 with connect() as con:
  for table in MODULES: counts[table]=con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
 return render_template("dashboard.html",modules=MODULES,counts=counts)
@app.route("/<table>")
def list_records(table):
 if table not in MODULES: return "Module not found",404
 q=request.args.get("q","").strip(); fields=[f for f,_ in MODULES[table]["fields"]]
 with connect() as con:
  if q:
   where=" OR ".join(f'"{f}" LIKE ?' for f in fields)
   rows=con.execute(f'SELECT * FROM "{table}" WHERE {where} ORDER BY id DESC',[f"%{q}%"]*len(fields)).fetchall()
  else: rows=con.execute(f'SELECT * FROM "{table}" ORDER BY id DESC').fetchall()
 return render_template("records.html",table=table,module=MODULES[table],rows=rows,q=q)
@app.route("/<table>/add",methods=["GET","POST"])
def add_record(table):
 if table not in MODULES: return "Module not found",404
 module=MODULES[table]
 if request.method=="POST":
  values=[request.form.get(f,"").strip() for f,_ in module["fields"]]
  if not values[0]:
   flash("The first field is required."); return render_template("form.html",table=table,module=module,values=request.form)
  cols=", ".join(f'"{f}"' for f,_ in module["fields"]); marks=", ".join("?" for _ in values)
  with connect() as con: con.execute(f'INSERT INTO "{table}" ({cols}) VALUES ({marks})',values)
  flash("Record added successfully."); return redirect(url_for("list_records",table=table))
 return render_template("form.html",table=table,module=module,values={})
@app.route("/<table>/delete/<int:record_id>",methods=["POST"])
def delete_record(table,record_id):
 if table not in MODULES: return "Module not found",404
 with connect() as con: con.execute(f'DELETE FROM "{table}" WHERE id=?',(record_id,))
 flash("Record deleted."); return redirect(url_for("list_records",table=table))
@app.route("/reports")
def reports():
 with connect() as con:
  counts={t:con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in MODULES}
  resources=con.execute("SELECT item,quantity,condition FROM resources ORDER BY item").fetchall()
 return render_template("reports.html",counts=counts,resources=resources)
if __name__=="__main__":
 init_db(); app.run(debug=True)
