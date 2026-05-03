# =============================================================================
# Salary Management System - Streamlit Frontend
# =============================================================================
# Run with:  streamlit run app.py
# (from inside the final_Salary_Mangement_System folder)
# =============================================================================

import streamlit as st
import pandas as pd
import sys
import os

# ---------------------------------------------------------------------------
# Path setup so Backend_Modules can be imported as a package
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))

from Backend_Modules.db_connection import get_connection
from Backend_Modules.employee import (
    Add_employee,
    add_permanent_employee,
    add_intern_employee,
    delete_employee,
)
from Backend_Modules.department import add_department
from Backend_Modules.Salary import add_salary

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Salary Management System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown(
    """
    <style>
    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 1rem;
        padding: 4px 0;
    }

    /* ---- Metric cards ---- */
    .metric-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 5px solid #3b82f6;
        margin-bottom: 12px;
    }
    .metric-card.green  { border-left-color: #22c55e; }
    .metric-card.orange { border-left-color: #f97316; }
    .metric-card.purple { border-left-color: #a855f7; }
    .metric-card.red    { border-left-color: #ef4444; }
    .metric-card h3 { margin: 0 0 4px 0; font-size: 0.85rem; color: #64748b; }
    .metric-card h2 { margin: 0; font-size: 1.8rem; color: #1e293b; font-weight: 700; }

    /* ---- Employee / info card ---- */
    .info-card {
        background: #f8fafc;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }
    .info-card p { margin: 4px 0; font-size: 0.95rem; color: #334155; }
    .info-card .label { font-weight: 600; color: #1e293b; }

    /* ---- Payslip ---- */
    .payslip-container {
        background: #ffffff;
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 28px 32px;
        max-width: 560px;
        margin: 0 auto;
        font-family: 'Courier New', monospace;
    }
    .payslip-header {
        text-align: center;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 12px;
        margin-bottom: 16px;
    }
    .payslip-header h2 { color: #1e40af; margin: 0; font-size: 1.4rem; }
    .payslip-header p  { color: #64748b; margin: 4px 0 0 0; font-size: 0.85rem; }
    .payslip-section   { margin: 14px 0; }
    .payslip-section h4 {
        color: #1e40af;
        border-bottom: 1px solid #bfdbfe;
        padding-bottom: 4px;
        margin-bottom: 8px;
        font-size: 0.95rem;
    }
    .payslip-row {
        display: flex;
        justify-content: space-between;
        padding: 3px 0;
        font-size: 0.9rem;
        color: #334155;
    }
    .payslip-total {
        display: flex;
        justify-content: space-between;
        padding: 10px 0 4px 0;
        border-top: 2px solid #3b82f6;
        font-weight: 700;
        font-size: 1.05rem;
        color: #1e40af;
    }

    /* ---- Highest-paid highlight ---- */
    .highlight-card {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        border-radius: 12px;
        padding: 24px 28px;
        color: #ffffff;
        text-align: center;
    }
    .highlight-card h2 { margin: 0 0 6px 0; font-size: 1.6rem; }
    .highlight-card p  { margin: 4px 0; font-size: 1rem; opacity: 0.9; }
    .highlight-card .salary { font-size: 2rem; font-weight: 800; margin-top: 10px; }

    /* ---- Success / error overrides ---- */
    div[data-testid="stAlert"] { border-radius: 8px; }

    /* ---- Section title ---- */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 4px;
    }
    .section-sub {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# HELPER UTILITIES
# =============================================================================

def run_query(sql: str, params: tuple = (), fetch: str = "all"):
    """Execute a SELECT query and return rows (or None on error)."""
    conn = get_connection()
    if conn is None:
        st.error("❌ Database connection failed. Check your MySQL server.")
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        if fetch == "one":
            return cursor.fetchone()
        return cursor.fetchall()
    except Exception as exc:
        st.error(f"❌ Query error: {exc}")
        return None
    finally:
        cursor.close()
        conn.close()


def run_write(sql: str, params: tuple = ()):
    """Execute an INSERT / UPDATE / DELETE and return (success, rowcount/error)."""
    conn = get_connection()
    if conn is None:
        return False, "Database connection failed."
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return True, cursor.rowcount
    except Exception as exc:
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()


def get_dept_options():
    """Return list of (DepartmentID, DepartmentName) tuples."""
    rows = run_query("SELECT DepartmentID, DepartmentName FROM DEPARTMENT ORDER BY DepartmentName")
    return rows or []


def fmt_currency(val):
    """Format a number as Indian-style currency string."""
    try:
        return f"₹ {float(val):,.2f}"
    except Exception:
        return "₹ 0.00"


def metric_card(title: str, value: str, color: str = "blue"):
    color_map = {"blue": "", "green": " green", "orange": " orange", "purple": " purple", "red": " red"}
    cls = color_map.get(color, "")
    st.markdown(
        f"""<div class="metric-card{cls}">
                <h3>{title}</h3>
                <h2>{value}</h2>
            </div>""",
        unsafe_allow_html=True,
    )


# =============================================================================
# DASHBOARD (Home)
# =============================================================================

def show_dashboard():
    st.markdown('<div class="section-title">💼 Salary Management System</div>', unsafe_allow_html=True)

    # Fetch key metrics
    total_emp   = run_query("SELECT COUNT(*) FROM EMPLOYEE", fetch="one")
    total_dept  = run_query("SELECT COUNT(*) FROM DEPARTMENT", fetch="one")
    total_bill  = run_query(
        "SELECT SUM(BasicSalary + HRA + DA + Bonus - Tax - PF) FROM SALARY", fetch="one"
    )
    highest_sal = run_query(
        "SELECT MAX(BasicSalary + HRA + DA + Bonus - Tax - PF) FROM SALARY", fetch="one"
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("👥 Total Employees",   str(total_emp[0])  if total_emp  else "—", "blue")
    with c2:
        metric_card("🏢 Total Departments", str(total_dept[0]) if total_dept else "—", "green")
    with c3:
        metric_card("💰 Total Salary Bill", fmt_currency(total_bill[0])  if total_bill  and total_bill[0]  else "₹ 0.00", "orange")
    with c4:
        metric_card("🏆 Highest Net Salary", fmt_currency(highest_sal[0]) if highest_sal and highest_sal[0] else "₹ 0.00", "purple")

    st.markdown("---")

    # Quick chart
    st.subheader("📊 Employees per Department")
    rows = run_query(
        """SELECT d.DepartmentName, COUNT(e.EmployeeID) AS Total
           FROM DEPARTMENT d
           LEFT JOIN EMPLOYEE e ON d.DepartmentID = e.DepartmentID
           GROUP BY d.DepartmentName"""
    )
    if rows:
        df = pd.DataFrame(rows, columns=["Department", "Employees"])
        st.bar_chart(df.set_index("Department"))

    # Recent employees
    st.subheader("🕐 Recent Employees")
    rows = run_query(
        """SELECT e.EmployeeID, e.Name, e.EmpType, d.DepartmentName, e.Email
           FROM EMPLOYEE e
           LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
           ORDER BY e.EmployeeID DESC LIMIT 5"""
    )
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Name", "Type", "Department", "Email"])
        st.dataframe(df, use_container_width=True, hide_index=True)


# =============================================================================
# EMPLOYEE SECTION
# =============================================================================

def show_employees():
    st.markdown('<div class="section-title">👥 Employee Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Add, view, search, update and delete employee records.</div>', unsafe_allow_html=True)

    tabs = st.tabs([
        "➕ Add Employee",
        "📋 View All",
        "🔍 Search by ID",
        "🔍 Search by Name",
        "📊 Count by Dept",
        "✏️ Update Employee",
        "🗑️ Delete Employee",
        "🔄 Change Type",
    ])

    # ------------------------------------------------------------------
    # TAB 1 — Add Employee
    # ------------------------------------------------------------------
    with tabs[0]:
        st.subheader("➕ Add New Employee")
        dept_rows = get_dept_options()
        dept_map  = {name: did for did, name in dept_rows}

        with st.form("form_add_employee", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                emp_id   = st.number_input("Employee ID *", min_value=1, step=1)
                name     = st.text_input("Full Name *")
                email    = st.text_input("Email *")
            with c2:
                phone    = st.text_input("Phone *")
                emp_type = st.selectbox("Employee Type *", ["Permanent", "Intern"])
                dept_sel = st.selectbox("Department *", list(dept_map.keys()) if dept_map else ["No departments"])

            st.markdown("---")
            # Conditional fields
            if emp_type == "Permanent":
                st.markdown("**Permanent Employee Details**")
                pc1, pc2, pc3 = st.columns(3)
                with pc1:
                    basic = st.number_input("Basic Salary (₹)", min_value=0.0, step=500.0)
                with pc2:
                    bonus = st.number_input("Bonus (₹)", min_value=0.0, step=100.0)
                with pc3:
                    pf    = st.number_input("PF (₹)", min_value=0.0, step=100.0)
                duration = None
            else:
                st.markdown("**Intern Details**")
                duration = st.number_input("Internship Duration (months) *", min_value=1, step=1)
                basic = bonus = pf = None

            submitted = st.form_submit_button("✅ Add Employee", use_container_width=True)

        if submitted:
            if not name or not email or not phone:
                st.error("❌ Name, Email and Phone are required.")
            elif not dept_map:
                st.error("❌ No departments found. Add a department first.")
            else:
                dept_id = dept_map[dept_sel]
                with st.spinner("Adding employee…"):
                    try:
                        Add_employee(int(emp_id), name, email, phone, emp_type, dept_id)
                        if emp_type == "Permanent":
                            add_permanent_employee(int(emp_id), basic, bonus, pf)
                        else:
                            add_intern_employee(int(emp_id), int(duration))
                        st.success(f"✅ Employee **{name}** (ID: {emp_id}) added successfully!")
                    except Exception as exc:
                        st.error(f"❌ Error: {exc}")

    # ------------------------------------------------------------------
    # TAB 2 — View All
    # ------------------------------------------------------------------
    with tabs[1]:
        st.subheader("📋 All Employees")
        with st.spinner("Loading employees…"):
            rows = run_query(
                """SELECT e.EmployeeID, e.Name, e.Email, e.Phone, e.EmpType,
                          COALESCE(d.DepartmentName, 'N/A') AS Department
                   FROM EMPLOYEE e
                   LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                   ORDER BY e.EmployeeID"""
            )
        if rows:
            df = pd.DataFrame(rows, columns=["ID", "Name", "Email", "Phone", "Type", "Department"])
            metric_card("Total Employees", str(len(df)), "blue")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No employees found.")

    # ------------------------------------------------------------------
    # TAB 3 — Search by ID
    # ------------------------------------------------------------------
    with tabs[2]:
        st.subheader("🔍 Search Employee by ID")
        search_id = st.number_input("Enter Employee ID", min_value=1, step=1, key="search_emp_id")
        if st.button("🔍 Search", key="btn_search_id"):
            with st.spinner("Searching…"):
                row = run_query(
                    """SELECT e.EmployeeID, e.Name, e.Email, e.Phone, e.EmpType,
                              COALESCE(d.DepartmentName,'N/A') AS Department
                       FROM EMPLOYEE e
                       LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                       WHERE e.EmployeeID = %s""",
                    (int(search_id),),
                    fetch="one",
                )
            if row:
                st.markdown(
                    f"""<div class="info-card">
                        <p><span class="label">🆔 Employee ID:</span> {row[0]}</p>
                        <p><span class="label">👤 Name:</span> {row[1]}</p>
                        <p><span class="label">📧 Email:</span> {row[2]}</p>
                        <p><span class="label">📞 Phone:</span> {row[3]}</p>
                        <p><span class="label">💼 Type:</span> {row[4]}</p>
                        <p><span class="label">🏢 Department:</span> {row[5]}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                # Show type-specific details
                if row[4] == "Permanent":
                    perm = run_query(
                        "SELECT BasicSalary, Bonus, PF FROM PERMANENT_EMPLOYEE WHERE EmployeeID=%s",
                        (int(search_id),), fetch="one"
                    )
                    if perm:
                        st.info(f"💰 Basic: {fmt_currency(perm[0])}  |  Bonus: {fmt_currency(perm[1])}  |  PF: {fmt_currency(perm[2])}")
                else:
                    intern = run_query(
                        "SELECT Internship_Duration FROM INTERN WHERE EmployeeID=%s",
                        (int(search_id),), fetch="one"
                    )
                    if intern:
                        st.info(f"📅 Internship Duration: {intern[0]} month(s)")
            else:
                st.warning("⚠️ Employee not found.")

    # ------------------------------------------------------------------
    # TAB 4 — Search by Name
    # ------------------------------------------------------------------
    with tabs[3]:
        st.subheader("🔍 Search Employee by Name")
        search_name = st.text_input("Enter name (partial match supported)", key="search_emp_name")
        if st.button("🔍 Search", key="btn_search_name"):
            if not search_name.strip():
                st.error("❌ Please enter a name to search.")
            else:
                with st.spinner("Searching…"):
                    rows = run_query(
                        """SELECT e.EmployeeID, e.Name, e.Email, e.Phone, e.EmpType,
                                  COALESCE(d.DepartmentName,'N/A') AS Department
                           FROM EMPLOYEE e
                           LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                           WHERE LOWER(e.Name) LIKE LOWER(%s)
                           ORDER BY e.Name""",
                        (f"%{search_name.strip()}%",),
                    )
                if rows:
                    df = pd.DataFrame(rows, columns=["ID", "Name", "Email", "Phone", "Type", "Department"])
                    st.success(f"✅ Found {len(df)} result(s).")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning("⚠️ No employees found matching that name.")

    # ------------------------------------------------------------------
    # TAB 5 — Count by Department
    # ------------------------------------------------------------------
    with tabs[4]:
        st.subheader("📊 Employee Count by Department")
        dept_rows = get_dept_options()
        if dept_rows:
            dept_map  = {name: did for did, name in dept_rows}
            dept_sel  = st.selectbox("Select Department", list(dept_map.keys()), key="count_dept_sel")
            if st.button("📊 Get Count", key="btn_count_dept"):
                with st.spinner("Counting…"):
                    result = run_query(
                        "SELECT COUNT(*) FROM EMPLOYEE WHERE DepartmentID = %s",
                        (dept_map[dept_sel],), fetch="one"
                    )
                if result is not None:
                    metric_card(f"Employees in {dept_sel}", str(result[0]), "green")
        else:
            st.warning("⚠️ No departments available.")

    # ------------------------------------------------------------------
    # TAB 6 — Update Employee
    # ------------------------------------------------------------------
    with tabs[5]:
        st.subheader("✏️ Update Employee")
        upd_id = st.number_input("Enter Employee ID to update", min_value=1, step=1, key="upd_emp_id")

        if st.button("🔎 Load Employee", key="btn_load_upd"):
            row = run_query(
                """SELECT e.EmployeeID, e.Name, e.Email, e.Phone, e.EmpType,
                          d.DepartmentName, e.DepartmentID
                   FROM EMPLOYEE e
                   LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                   WHERE e.EmployeeID = %s""",
                (int(upd_id),), fetch="one"
            )
            if row:
                st.session_state["upd_emp_row"] = row
            else:
                st.warning("⚠️ Employee not found.")
                st.session_state.pop("upd_emp_row", None)

        if "upd_emp_row" in st.session_state:
            row = st.session_state["upd_emp_row"]
            st.markdown(
                f"""<div class="info-card">
                    <p><span class="label">👤 Name:</span> {row[1]} &nbsp;|&nbsp;
                       <span class="label">📞 Phone:</span> {row[3]} &nbsp;|&nbsp;
                       <span class="label">🏢 Dept:</span> {row[5]}</p>
                </div>""",
                unsafe_allow_html=True,
            )
            update_field = st.radio("What do you want to update?", ["Phone Number", "Department"], key="upd_field_radio")

            if update_field == "Phone Number":
                new_phone = st.text_input("New Phone Number", key="new_phone_input")
                if st.button("✅ Update Phone", key="btn_upd_phone"):
                    if not new_phone.strip():
                        st.error("❌ Phone number cannot be empty.")
                    else:
                        ok, res = run_write(
                            "UPDATE EMPLOYEE SET Phone = %s WHERE EmployeeID = %s",
                            (new_phone.strip(), int(row[0]))
                        )
                        if ok and res > 0:
                            st.success("✅ Phone number updated successfully!")
                            st.session_state.pop("upd_emp_row", None)
                        elif ok:
                            st.warning("⚠️ No rows updated.")
                        else:
                            st.error(f"❌ Error: {res}")
            else:
                dept_rows = get_dept_options()
                dept_map  = {name: did for did, name in dept_rows}
                new_dept  = st.selectbox("New Department", list(dept_map.keys()), key="new_dept_sel")
                if st.button("✅ Update Department", key="btn_upd_dept"):
                    ok, res = run_write(
                        "UPDATE EMPLOYEE SET DepartmentID = %s WHERE EmployeeID = %s",
                        (dept_map[new_dept], int(row[0]))
                    )
                    if ok and res > 0:
                        st.success("✅ Department updated successfully!")
                        st.session_state.pop("upd_emp_row", None)
                    elif ok:
                        st.warning("⚠️ No rows updated.")
                    else:
                        st.error(f"❌ Error: {res}")

    # ------------------------------------------------------------------
    # TAB 7 — Delete Employee
    # ------------------------------------------------------------------
    with tabs[6]:
        st.subheader("🗑️ Delete Employee")
        del_id = st.number_input("Enter Employee ID to delete", min_value=1, step=1, key="del_emp_id")

        if st.button("🔎 Load Employee", key="btn_load_del"):
            row = run_query(
                """SELECT e.EmployeeID, e.Name, e.Email, e.Phone, e.EmpType,
                          COALESCE(d.DepartmentName,'N/A') AS Department
                   FROM EMPLOYEE e
                   LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                   WHERE e.EmployeeID = %s""",
                (int(del_id),), fetch="one"
            )
            if row:
                st.session_state["del_emp_row"] = row
            else:
                st.warning("⚠️ Employee not found.")
                st.session_state.pop("del_emp_row", None)

        if "del_emp_row" in st.session_state:
            row = st.session_state["del_emp_row"]
            st.markdown(
                f"""<div class="info-card">
                    <p><span class="label">🆔 ID:</span> {row[0]} &nbsp;|&nbsp;
                       <span class="label">👤 Name:</span> {row[1]}</p>
                    <p><span class="label">📧 Email:</span> {row[2]} &nbsp;|&nbsp;
                       <span class="label">📞 Phone:</span> {row[3]}</p>
                    <p><span class="label">💼 Type:</span> {row[4]} &nbsp;|&nbsp;
                       <span class="label">🏢 Dept:</span> {row[5]}</p>
                </div>""",
                unsafe_allow_html=True,
            )
            confirm = st.checkbox(
                f"⚠️ I confirm I want to permanently delete **{row[1]}** (ID: {row[0]}) and all related records.",
                key="del_confirm_chk"
            )
            if st.button("🗑️ Delete Employee", key="btn_del_emp", disabled=not confirm):
                with st.spinner("Deleting…"):
                    try:
                        delete_employee(int(row[0]))
                        st.success(f"✅ Employee **{row[1]}** deleted successfully.")
                        st.session_state.pop("del_emp_row", None)
                    except Exception as exc:
                        st.error(f"❌ Error: {exc}")

    # ------------------------------------------------------------------
    # TAB 8 — Change Employee Type
    # ------------------------------------------------------------------
    with tabs[7]:
        st.subheader("🔄 Change Employee Type")
        chg_id = st.number_input("Enter Employee ID", min_value=1, step=1, key="chg_type_id")

        if st.button("🔎 Load Employee", key="btn_load_chg"):
            row = run_query(
                "SELECT EmployeeID, Name, EmpType FROM EMPLOYEE WHERE EmployeeID = %s",
                (int(chg_id),), fetch="one"
            )
            if row:
                st.session_state["chg_emp_row"] = row
            else:
                st.warning("⚠️ Employee not found.")
                st.session_state.pop("chg_emp_row", None)

        if "chg_emp_row" in st.session_state:
            row = st.session_state["chg_emp_row"]
            current_type = row[2]
            st.info(f"👤 **{row[1]}** — Current Type: **{current_type}**")

            new_type_options = ["Intern"] if current_type == "Permanent" else ["Permanent"]
            new_type = st.selectbox("Change to", new_type_options, key="chg_new_type")

            if new_type == "Permanent":
                st.markdown("**New Permanent Employee Details**")
                nc1, nc2, nc3 = st.columns(3)
                with nc1:
                    chg_basic = st.number_input("Basic Salary (₹)", min_value=0.0, step=500.0, key="chg_basic")
                with nc2:
                    chg_bonus = st.number_input("Bonus (₹)", min_value=0.0, step=100.0, key="chg_bonus")
                with nc3:
                    chg_pf    = st.number_input("PF (₹)", min_value=0.0, step=100.0, key="chg_pf")
                chg_duration = None
            else:
                chg_duration = st.number_input("Internship Duration (months)", min_value=1, step=1, key="chg_duration")
                chg_basic = chg_bonus = chg_pf = None

            if st.button("🔄 Change Type", key="btn_chg_type"):
                conn = get_connection()
                if conn is None:
                    st.error("❌ Database connection failed.")
                else:
                    try:
                        cursor = conn.cursor()
                        emp_id_val = int(row[0])

                        if current_type == "Permanent" and new_type == "Intern":
                            cursor.execute("DELETE FROM PERMANENT_EMPLOYEE WHERE EmployeeID = %s", (emp_id_val,))
                            cursor.execute(
                                "INSERT INTO INTERN(EmployeeID, Internship_Duration) VALUES(%s,%s)",
                                (emp_id_val, int(chg_duration))
                            )
                        elif current_type == "Intern" and new_type == "Permanent":
                            cursor.execute("DELETE FROM INTERN WHERE EmployeeID = %s", (emp_id_val,))
                            cursor.execute(
                                "INSERT INTO PERMANENT_EMPLOYEE(EmployeeID, BasicSalary, Bonus, PF) VALUES(%s,%s,%s,%s)",
                                (emp_id_val, chg_basic, chg_bonus, chg_pf)
                            )

                        cursor.execute(
                            "UPDATE EMPLOYEE SET EmpType = %s WHERE EmployeeID = %s",
                            (new_type, emp_id_val)
                        )
                        conn.commit()
                        st.success(f"✅ Employee type changed to **{new_type}** successfully!")
                        st.session_state.pop("chg_emp_row", None)
                    except Exception as exc:
                        conn.rollback()
                        st.error(f"❌ Error: {exc}")
                    finally:
                        cursor.close()
                        conn.close()


# =============================================================================
# DEPARTMENT SECTION
# =============================================================================

def show_departments():
    st.markdown('<div class="section-title">🏢 Department Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Manage departments and view department-level analytics.</div>', unsafe_allow_html=True)

    tabs = st.tabs([
        "➕ Add Department",
        "📋 View All",
        "🔍 Search by ID",
        "📊 Total Count",
        "👥 Employees in Dept",
        "📈 Count per Dept",
        "💰 Salary Report",
    ])

    # ------------------------------------------------------------------
    # TAB 1 — Add Department
    # ------------------------------------------------------------------
    with tabs[0]:
        st.subheader("➕ Add New Department")
        with st.form("form_add_dept", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                dept_id   = st.number_input("Department ID *", min_value=1, step=1)
            with c2:
                dept_name = st.text_input("Department Name *")
            submitted = st.form_submit_button("✅ Add Department", use_container_width=True)

        if submitted:
            if not dept_name.strip():
                st.error("❌ Department name is required.")
            else:
                with st.spinner("Adding department…"):
                    try:
                        add_department(int(dept_id), dept_name.strip())
                        st.success(f"✅ Department **{dept_name}** (ID: {dept_id}) added successfully!")
                    except Exception as exc:
                        st.error(f"❌ Error: {exc}")

    # ------------------------------------------------------------------
    # TAB 2 — View All
    # ------------------------------------------------------------------
    with tabs[1]:
        st.subheader("📋 All Departments")
        with st.spinner("Loading…"):
            rows = run_query("SELECT DepartmentID, DepartmentName FROM DEPARTMENT ORDER BY DepartmentID")
        if rows:
            df = pd.DataFrame(rows, columns=["Department ID", "Department Name"])
            metric_card("Total Departments", str(len(df)), "green")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No departments found.")

    # ------------------------------------------------------------------
    # TAB 3 — Search by ID
    # ------------------------------------------------------------------
    with tabs[2]:
        st.subheader("🔍 Search Department by ID")
        s_dept_id = st.number_input("Enter Department ID", min_value=1, step=1, key="s_dept_id")
        if st.button("🔍 Search", key="btn_search_dept"):
            with st.spinner("Searching…"):
                row = run_query(
                    "SELECT DepartmentID, DepartmentName FROM DEPARTMENT WHERE DepartmentID = %s",
                    (int(s_dept_id),), fetch="one"
                )
            if row:
                st.markdown(
                    f"""<div class="info-card">
                        <p><span class="label">🆔 Department ID:</span> {row[0]}</p>
                        <p><span class="label">🏢 Department Name:</span> {row[1]}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.warning("⚠️ Department not found.")

    # ------------------------------------------------------------------
    # TAB 4 — Total Count
    # ------------------------------------------------------------------
    with tabs[3]:
        st.subheader("📊 Total Department Count")
        with st.spinner("Counting…"):
            result = run_query("SELECT COUNT(*) FROM DEPARTMENT", fetch="one")
        if result is not None:
            metric_card("🏢 Total Departments", str(result[0]), "green")

    # ------------------------------------------------------------------
    # TAB 5 — Employees in Department
    # ------------------------------------------------------------------
    with tabs[4]:
        st.subheader("👥 Employees in a Department")
        dept_rows = get_dept_options()
        if dept_rows:
            dept_map = {name: did for did, name in dept_rows}
            sel_dept = st.selectbox("Select Department", list(dept_map.keys()), key="emp_in_dept_sel")
            if st.button("👥 Show Employees", key="btn_emp_in_dept"):
                with st.spinner("Loading…"):
                    rows = run_query(
                        """SELECT e.EmployeeID, e.Name, e.Email, e.Phone, e.EmpType
                           FROM EMPLOYEE e
                           WHERE e.DepartmentID = %s
                           ORDER BY e.EmployeeID""",
                        (dept_map[sel_dept],)
                    )
                if rows:
                    df = pd.DataFrame(rows, columns=["ID", "Name", "Email", "Phone", "Type"])
                    metric_card(f"Employees in {sel_dept}", str(len(df)), "blue")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"⚠️ No employees found in **{sel_dept}**.")
        else:
            st.warning("⚠️ No departments available.")

    # ------------------------------------------------------------------
    # TAB 6 — Count per Department (bar chart)
    # ------------------------------------------------------------------
    with tabs[5]:
        st.subheader("📈 Employee Count per Department")
        with st.spinner("Loading…"):
            rows = run_query(
                """SELECT d.DepartmentName, COUNT(e.EmployeeID) AS TotalEmployees
                   FROM DEPARTMENT d
                   LEFT JOIN EMPLOYEE e ON d.DepartmentID = e.DepartmentID
                   GROUP BY d.DepartmentName
                   ORDER BY TotalEmployees DESC"""
            )
        if rows:
            df = pd.DataFrame(rows, columns=["Department", "Total Employees"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No data available.")

    # ------------------------------------------------------------------
    # TAB 7 — Department Salary Report
    # ------------------------------------------------------------------
    with tabs[6]:
        st.subheader("💰 Department Salary Report")
        with st.spinner("Generating report…"):
            rows = run_query(
                """SELECT d.DepartmentName,
                          COUNT(e.EmployeeID) AS TotalEmployees,
                          COALESCE(SUM(s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF), 0) AS TotalSalary,
                          COALESCE(ROUND(AVG(s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF), 2), 0) AS AvgSalary
                   FROM DEPARTMENT d
                   LEFT JOIN EMPLOYEE e ON d.DepartmentID = e.DepartmentID
                   LEFT JOIN SALARY   s ON e.EmployeeID   = s.EmployeeID
                   GROUP BY d.DepartmentName
                   ORDER BY TotalSalary DESC"""
            )
        if rows:
            df = pd.DataFrame(rows, columns=["Department", "Total Employees", "Total Salary (₹)", "Avg Salary (₹)"])
            # Summary metrics
            c1, c2, c3 = st.columns(3)
            with c1:
                metric_card("Total Departments", str(len(df)), "blue")
            with c2:
                metric_card("Total Salary Bill", fmt_currency(df["Total Salary (₹)"].sum()), "orange")
            with c3:
                metric_card("Overall Avg Salary", fmt_currency(df["Avg Salary (₹)"].mean()), "purple")

            st.markdown("---")
            st.subheader("📊 Total Salary per Department")
            st.bar_chart(df.set_index("Department")["Total Salary (₹)"])

            st.subheader("📋 Detailed Report")
            # Format currency columns for display
            display_df = df.copy()
            display_df["Total Salary (₹)"] = display_df["Total Salary (₹)"].apply(lambda x: f"₹ {float(x):,.2f}")
            display_df["Avg Salary (₹)"]   = display_df["Avg Salary (₹)"].apply(lambda x: f"₹ {float(x):,.2f}")
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No salary data available.")


# =============================================================================
# SALARY SECTION
# =============================================================================

def show_salary():
    st.markdown('<div class="section-title">💰 Salary Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">View, add, update salary records and generate payslips.</div>', unsafe_allow_html=True)

    tabs = st.tabs([
        "📋 View All Salaries",
        "📊 Salary Report",
        "🏆 Highest Paid",
        "🧾 Generate Payslip",
        "➕ Add Salary",
        "✏️ Update Salary",
        "🔎 Salary Range Filter",
        "📉 Average Salary",
    ])

    # ------------------------------------------------------------------
    # TAB 1 — View All Salaries
    # ------------------------------------------------------------------
    with tabs[0]:
        st.subheader("📋 All Salary Records")
        with st.spinner("Loading salary records…"):
            rows = run_query(
                """SELECT s.SalaryID, s.EmployeeID, e.Name,
                          s.BasicSalary, s.HRA, s.DA, s.Bonus, s.Tax, s.PF,
                          (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
                   FROM SALARY s
                   LEFT JOIN EMPLOYEE e ON s.EmployeeID = e.EmployeeID
                   ORDER BY NetSalary DESC"""
            )
        if rows:
            df = pd.DataFrame(rows, columns=[
                "Salary ID", "Emp ID", "Name",
                "Basic (₹)", "HRA (₹)", "DA (₹)", "Bonus (₹)", "Tax (₹)", "PF (₹)", "Net Salary (₹)"
            ])
            c1, c2 = st.columns(2)
            with c1:
                metric_card("Total Records", str(len(df)), "blue")
            with c2:
                metric_card("Total Salary Bill", fmt_currency(df["Net Salary (₹)"].sum()), "orange")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No salary records found.")

    # ------------------------------------------------------------------
    # TAB 2 — Salary Report
    # ------------------------------------------------------------------
    with tabs[1]:
        st.subheader("📊 Full Salary Report")
        with st.spinner("Generating report…"):
            rows = run_query(
                """SELECT e.EmployeeID, e.Name, d.DepartmentName,
                          s.BasicSalary, s.HRA, s.DA, s.Bonus, s.Tax, s.PF,
                          (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
                   FROM SALARY s
                   JOIN EMPLOYEE   e ON s.EmployeeID   = e.EmployeeID
                   LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                   ORDER BY NetSalary DESC"""
            )
        if rows:
            df = pd.DataFrame(rows, columns=[
                "Emp ID", "Name", "Department",
                "Basic (₹)", "HRA (₹)", "DA (₹)", "Bonus (₹)", "Tax (₹)", "PF (₹)", "Net Salary (₹)"
            ])
            st.subheader("� Detailed Salary Table")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No salary data available.")

    # ------------------------------------------------------------------
    # TAB 3 — Highest Paid
    # ------------------------------------------------------------------
    with tabs[2]:
        st.subheader("🏆 Highest Paid Employee")
        with st.spinner("Fetching…"):
            row = run_query(
                """SELECT e.EmployeeID, e.Name, COALESCE(d.DepartmentName,'N/A') AS Dept,
                          (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
                   FROM EMPLOYEE e
                   JOIN SALARY s ON e.EmployeeID = s.EmployeeID
                   LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                   ORDER BY NetSalary DESC
                   LIMIT 1""",
                fetch="one"
            )
        if row:
            st.markdown(
                f"""<div class="highlight-card">
                    <p>🏆 Highest Paid Employee</p>
                    <h2>{row[1]}</h2>
                    <p>🆔 ID: {row[0]} &nbsp;|&nbsp; 🏢 {row[2]}</p>
                    <div class="salary">{fmt_currency(row[3])}</div>
                    <p style="opacity:0.7; font-size:0.85rem; margin-top:8px;">Net Monthly Salary</p>
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.warning("⚠️ No salary records found.")

    # ------------------------------------------------------------------
    # TAB 4 — Generate Payslip
    # ------------------------------------------------------------------
    with tabs[3]:
        st.subheader("🧾 Generate Payslip")
        ps_emp_id = st.number_input("Enter Employee ID", min_value=1, step=1, key="ps_emp_id")
        if st.button("🧾 Generate Payslip", key="btn_gen_payslip"):
            with st.spinner("Generating payslip…"):
                row = run_query(
                    """SELECT e.EmployeeID, e.Name, e.Email,
                              COALESCE(d.DepartmentName,'N/A') AS Dept,
                              s.BasicSalary, s.HRA, s.DA, s.Bonus, s.Tax, s.PF,
                              (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
                       FROM EMPLOYEE e
                       JOIN SALARY s ON e.EmployeeID = s.EmployeeID
                       LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                       WHERE e.EmployeeID = %s""",
                    (int(ps_emp_id),), fetch="one"
                )
            if row:
                gross    = float(row[4]) + float(row[5]) + float(row[6]) + float(row[7])
                deduct   = float(row[8]) + float(row[9])
                net      = float(row[10])

                st.markdown(
                    f"""<div class="payslip-container">
                        <div class="payslip-header">
                            <h2>💼 SALARY PAYSLIP</h2>
                            <p>Salary Management System</p>
                        </div>

                        <div class="payslip-section">
                            <h4>Employee Details</h4>
                            <div class="payslip-row"><span>Employee ID</span><span>{row[0]}</span></div>
                            <div class="payslip-row"><span>Name</span><span>{row[1]}</span></div>
                            <div class="payslip-row"><span>Email</span><span>{row[2]}</span></div>
                            <div class="payslip-row"><span>Department</span><span>{row[3]}</span></div>
                        </div>

                        <div class="payslip-section">
                            <h4>💚 Earnings</h4>
                            <div class="payslip-row"><span>Basic Salary</span><span>{fmt_currency(row[4])}</span></div>
                            <div class="payslip-row"><span>HRA (House Rent Allowance)</span><span>{fmt_currency(row[5])}</span></div>
                            <div class="payslip-row"><span>DA (Dearness Allowance)</span><span>{fmt_currency(row[6])}</span></div>
                            <div class="payslip-row"><span>Bonus</span><span>{fmt_currency(row[7])}</span></div>
                            <div class="payslip-row" style="font-weight:600; border-top:1px dashed #bfdbfe; padding-top:6px; margin-top:4px;">
                                <span>Gross Earnings</span><span>{fmt_currency(gross)}</span>
                            </div>
                        </div>

                        <div class="payslip-section">
                            <h4>🔴 Deductions</h4>
                            <div class="payslip-row"><span>Income Tax</span><span>- {fmt_currency(row[8])}</span></div>
                            <div class="payslip-row"><span>PF (Provident Fund)</span><span>- {fmt_currency(row[9])}</span></div>
                            <div class="payslip-row" style="font-weight:600; border-top:1px dashed #fecaca; padding-top:6px; margin-top:4px;">
                                <span>Total Deductions</span><span>- {fmt_currency(deduct)}</span>
                            </div>
                        </div>

                        <div class="payslip-total">
                            <span>💰 NET SALARY</span>
                            <span>{fmt_currency(net)}</span>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.warning("⚠️ No salary record found for this employee.")

    # ------------------------------------------------------------------
    # TAB 5 — Add Salary
    # ------------------------------------------------------------------
    with tabs[4]:
        st.subheader("➕ Add Salary Record")
        with st.form("form_add_salary", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                sal_id  = st.number_input("Salary ID *", min_value=1, step=1)
                emp_id  = st.number_input("Employee ID *", min_value=1, step=1)
                basic   = st.number_input("Basic Salary (₹) *", min_value=0.0, step=500.0)
                hra     = st.number_input("HRA (₹)", min_value=0.0, step=100.0)
            with c2:
                da      = st.number_input("DA (₹)", min_value=0.0, step=100.0)
                bonus   = st.number_input("Bonus (₹)", min_value=0.0, step=100.0)
                tax     = st.number_input("Tax (₹)", min_value=0.0, step=100.0)
                pf      = st.number_input("PF (₹)", min_value=0.0, step=100.0)

            net_preview = basic + hra + da + bonus - tax - pf
            st.info(f"💡 Net Salary Preview: **{fmt_currency(net_preview)}**")
            submitted = st.form_submit_button("✅ Add Salary", use_container_width=True)

        if submitted:
            with st.spinner("Adding salary record…"):
                try:
                    add_salary(int(sal_id), int(emp_id), basic, hra, da, bonus, tax, pf)
                    st.success(f"✅ Salary record added for Employee ID **{emp_id}**!")
                except Exception as exc:
                    st.error(f"❌ Error: {exc}")

    # ------------------------------------------------------------------
    # TAB 6 — Update Salary
    # ------------------------------------------------------------------
    with tabs[5]:
        st.subheader("✏️ Update Salary Record")
        upd_sal_id = st.number_input("Enter Employee ID", min_value=1, step=1, key="upd_sal_emp_id")

        if st.button("🔎 Load Salary", key="btn_load_sal"):
            row = run_query(
                """SELECT s.SalaryID, s.EmployeeID, e.Name,
                          s.BasicSalary, s.HRA, s.DA, s.Bonus, s.Tax, s.PF,
                          (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
                   FROM SALARY s
                   JOIN EMPLOYEE e ON s.EmployeeID = e.EmployeeID
                   WHERE s.EmployeeID = %s""",
                (int(upd_sal_id),), fetch="one"
            )
            if row:
                st.session_state["upd_sal_row"] = row
            else:
                st.warning("⚠️ No salary record found for this employee.")
                st.session_state.pop("upd_sal_row", None)

        if "upd_sal_row" in st.session_state:
            row = st.session_state["upd_sal_row"]
            st.markdown(
                f"""<div class="info-card">
                    <p><span class="label">👤 {row[2]}</span> (ID: {row[1]}) &nbsp;|&nbsp;
                       <span class="label">Current Net Salary:</span> {fmt_currency(row[9])}</p>
                </div>""",
                unsafe_allow_html=True,
            )
            with st.form("form_upd_salary"):
                uc1, uc2 = st.columns(2)
                with uc1:
                    new_basic = st.number_input("Basic Salary (₹)", value=float(row[3]), min_value=0.0, step=500.0)
                    new_hra   = st.number_input("HRA (₹)",          value=float(row[4]), min_value=0.0, step=100.0)
                    new_da    = st.number_input("DA (₹)",           value=float(row[5]), min_value=0.0, step=100.0)
                with uc2:
                    new_bonus = st.number_input("Bonus (₹)",        value=float(row[6]), min_value=0.0, step=100.0)
                    new_tax   = st.number_input("Tax (₹)",          value=float(row[7]), min_value=0.0, step=100.0)
                    new_pf    = st.number_input("PF (₹)",           value=float(row[8]), min_value=0.0, step=100.0)

                new_net = new_basic + new_hra + new_da + new_bonus - new_tax - new_pf
                st.info(f"💡 New Net Salary Preview: **{fmt_currency(new_net)}**")
                upd_submitted = st.form_submit_button("✅ Update Salary", use_container_width=True)

            if upd_submitted:
                with st.spinner("Updating…"):
                    ok, res = run_write(
                        """UPDATE SALARY
                           SET BasicSalary=%s, HRA=%s, DA=%s, Bonus=%s, Tax=%s, PF=%s
                           WHERE EmployeeID=%s""",
                        (new_basic, new_hra, new_da, new_bonus, new_tax, new_pf, int(row[1]))
                    )
                if ok and res > 0:
                    st.success("✅ Salary updated successfully!")
                    st.session_state.pop("upd_sal_row", None)
                elif ok:
                    st.warning("⚠️ No rows updated.")
                else:
                    st.error(f"❌ Error: {res}")

    # ------------------------------------------------------------------
    # TAB 7 — Salary Range Filter
    # ------------------------------------------------------------------
    with tabs[6]:
        st.subheader("🔎 Filter Employees by Salary Range")
        rc1, rc2 = st.columns(2)
        with rc1:
            min_sal = st.number_input("Minimum Net Salary (₹)", min_value=0.0, step=1000.0, key="range_min")
        with rc2:
            max_sal = st.number_input("Maximum Net Salary (₹)", min_value=0.0, value=200000.0, step=1000.0, key="range_max")

        if st.button("🔎 Filter", key="btn_sal_range"):
            if min_sal > max_sal:
                st.error("❌ Minimum salary cannot be greater than maximum salary.")
            else:
                with st.spinner("Filtering…"):
                    rows = run_query(
                        """SELECT e.EmployeeID, e.Name,
                                  COALESCE(d.DepartmentName,'N/A') AS Department,
                                  (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
                           FROM EMPLOYEE e
                           JOIN SALARY s ON e.EmployeeID = s.EmployeeID
                           LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
                           WHERE (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) BETWEEN %s AND %s
                           ORDER BY NetSalary DESC""",
                        (min_sal, max_sal)
                    )
                if rows:
                    df = pd.DataFrame(rows, columns=["Emp ID", "Name", "Department", "Net Salary (₹)"])
                    st.success(f"✅ Found **{len(df)}** employee(s) in range {fmt_currency(min_sal)} – {fmt_currency(max_sal)}.")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"⚠️ No employees found in the salary range {fmt_currency(min_sal)} – {fmt_currency(max_sal)}.")

    # ------------------------------------------------------------------
    # TAB 8 — Average Salary
    # ------------------------------------------------------------------
    with tabs[7]:
        st.subheader("📉 Average Net Salary")
        with st.spinner("Calculating…"):
            result = run_query(
                "SELECT AVG(BasicSalary + HRA + DA + Bonus - Tax - PF) FROM SALARY",
                fetch="one"
            )
            highest = run_query(
                "SELECT MAX(BasicSalary + HRA + DA + Bonus - Tax - PF) FROM SALARY",
                fetch="one"
            )
            lowest = run_query(
                "SELECT MIN(BasicSalary + HRA + DA + Bonus - Tax - PF) FROM SALARY",
                fetch="one"
            )

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("📉 Average Net Salary", fmt_currency(result[0]) if result and result[0] else "₹ 0.00", "blue")
        with c2:
            metric_card("🏆 Highest Net Salary", fmt_currency(highest[0]) if highest and highest[0] else "₹ 0.00", "green")
        with c3:
            metric_card("📊 Lowest Net Salary", fmt_currency(lowest[0]) if lowest and lowest[0] else "₹ 0.00", "orange")

        # Distribution chart
        st.markdown("---")
        st.subheader("📊 Salary Distribution")
        rows = run_query(
            """SELECT e.Name,
                      (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
               FROM SALARY s
               JOIN EMPLOYEE e ON s.EmployeeID = e.EmployeeID
               ORDER BY NetSalary DESC"""
        )
        if rows:
            df = pd.DataFrame(rows, columns=["Employee", "Net Salary (₹)"])
            st.bar_chart(df.set_index("Employee"))


# =============================================================================
# MAIN — Sidebar Navigation + Router
# =============================================================================

def main():
    # ---- Sidebar ----
    with st.sidebar:
        st.markdown(
            """<div style="text-align:center; padding: 16px 0 8px 0;">
                <span style="font-size:2.5rem;">💼</span>
                <h2 style="margin:6px 0 2px 0; font-size:1.1rem; color:#f1f5f9;">
                    Salary Management
                </h2>
                <p style="font-size:0.75rem; color:#94a3b8; margin:0;">College DBMS Project</p>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        section = st.radio(
            "Navigate to",
            ["🏠 Dashboard", "👥 Employees", "🏢 Departments", "💰 Salary"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown(
            """<div style="font-size:0.75rem; color:#64748b; text-align:center; padding-top:8px;">
                Built with Streamlit &amp; MySQL
            </div>""",
            unsafe_allow_html=True,
        )

    # ---- Route ----
    if section == "🏠 Dashboard":
        show_dashboard()
    elif section == "👥 Employees":
        show_employees()
    elif section == "🏢 Departments":
        show_departments()
    elif section == "💰 Salary":
        show_salary()


if __name__ == "__main__":
    main()
