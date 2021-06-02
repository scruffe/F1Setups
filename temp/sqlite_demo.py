import sqlite3
from user import User
from department import Department

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS 
                departments (
                    Department_id integer,
                    Department_name text
                    )""")


def insert_dep(dep):
    with conn:
        c.execute("INSERT INTO departments VALUES (:id, :name)",
                  {'id': dep.department_id, 'name': dep.name})


dep_1 = Department(1, 'Human Resources')
dep_2 = Department(2, 'Development')
dep_3 = Department(3, 'Sales')
dep_4 = Department(4, 'Technical Support')

insert_dep(dep_1)
insert_dep(dep_2)
insert_dep(dep_3)
insert_dep(dep_4)


def get_deps():
    c.execute("""SELECT * FROM departments 
                """)
    return c.fetchall()


print(get_deps())


c.execute("""CREATE TABLE IF NOT EXISTS 
                employees (
                    first text,
                    last text,
                    pay integer,
                    department_id integer
                    )""")


def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay, :department_id)",
                  {'first': emp.first, 'last': emp.last, 'pay': emp.pay, 'department_id': emp.department_id})


def get_emps_by_name(lastname):
    c.execute("""SELECT * FROM employees WHERE last=:last
                """,
              {'last': lastname})
    return c.fetchall()


def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})


def get_emps_by_fullname(firstname, lastname):
    c.execute("SELECT * FROM employees WHERE first=:first AND last=:last",
              {'first': firstname, 'last': lastname})
    return c.fetchall()


emp_1 = User('John', 'Doe', 80000, 1)
emp_2 = User('Jane', 'Doe', 90000, 2)
emp_3 = User('James', 'heck', 90000, None)


def insert(emp):
    check = get_emps_by_fullname(emp.first, emp.last)

    if not check:
        print('inserting ', emp)
        insert_emp(emp)
    else:
        print(emp.first, emp.last, ' already exists')


insert(emp_1)
insert(emp_2)
insert(emp_2)
insert(emp_3)

print(get_emps_by_name('Doe'))

# c.execute("DELETE FROM employees")
update_pay(emp_1, 50000)
remove_emp(emp_2)
print(get_emps_by_name('Doe'))


def get_joined(lastname):
    c.execute("""SELECT
                    first,
                    last,
                    pay,
                    Department_name
                FROM employees 
                LEFT JOIN departments
                ON employees.department_id = departments.department_id
                WHERE last=:last;
                        """, {'last': lastname})
    return c.fetchall()

print(" ")
print(get_joined('heck'))

conn.close()