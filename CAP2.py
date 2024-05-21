class Person:
    def __init__(self, name, age, marital_status, org_type=None, emp_type=None, salary=None, has_children=False, children_in_school=False, num_children_in_school=0):
        self.name = name
        self.age = age
        self.marital_status = marital_status
        self.org_type = org_type
        self.emp_type = emp_type
        self.salary = salary
        self.has_children = has_children
        self.children_in_school = children_in_school
        self.num_children_in_school = num_children_in_school

class Employee(Person):
    def __init__(self, name, age, marital_status, org_type, emp_type, salary, has_children, children_in_school, num_children_in_school):
        super().__init__(name, age, marital_status, org_type, emp_type, salary, has_children, children_in_school, num_children_in_school)

class TaxPayer:
    def __init__(self, name, income, num_children, self_education_allowance, donations):
        self.name = name
        self.income = income
        self.num_children = num_children
        self.self_education_allowance = self_education_allowance
        self.donations = donations

    def calculate_tax(self):
        taxable_income = self.income - self.get_deductibles()

        # Calculate deductions
        deductions = Deductions(self.num_children, taxable_income, self.self_education_allowance, self.donations)
        total_deductions = deductions.get_total_deductions()

        # Calculate taxable income after deductions
        taxable_income -= total_deductions

        # Check if taxable income is below minimum taxable income
        if taxable_income < MIN_TAXABLE_INCOME:
            return 0

        # Calculate tax based on tax brackets
        tax_calculator = TaxCalculator(taxable_income)
        tax = tax_calculator.calculate_tax()

        # Apply surcharge if applicable
        if tax >= 1000000:
            tax *= 1.1

        return tax

    def get_deductibles(self):
        raise NotImplementedError("get_deductibles method must be implemented in the child class.")

class Employee(TaxPayer):
    def __init__(self, name, income, num_children, is_contract, org_type, pf_contribution, gis_contribution, life_insurance_premium, children_allowance, sponsored_children_education_expense, self_education_allowance, donations, dividend_income=0, rental_income=0):
        super().__init__(name, income, num_children, self_education_allowance, donations)
        self.is_contract = is_contract
        self.organization = Organization(org_type)
        self.pf_contribution = pf_contribution if self.organization.is_pf_applicable(is_contract) else 0
        self.gis_contribution = gis_contribution
        self.life_insurance_premium = life_insurance_premium
        self.children_allowance = children_allowance
        self.sponsored_children_education_expense = sponsored_children_education_expense
        self.dividend_income = dividend_income
        self.rental_income = rental_income

    def get_deductibles(self):
        return self.pf_contribution + self.gis_contribution + self.life_insurance_premium + self.children_allowance + self.sponsored_children_education_expense

class Organization:
    def __init__(self, org_type):
        self.org_type = org_type

    def is_pf_applicable(self, is_contract):
        if self.org_type == "government" and is_contract:
            return False
        return True

class Deductions:
    def __init__(self, num_children, taxable_income, self_education_allowance, donations):
        self.num_children = num_children
        self.taxable_income = taxable_income
        self.self_education_allowance = self_education_allowance
        self.donations = donations

    def get_education_allowance(self):
        return min(self.num_children * EDUCATION_ALLOWANCE_PER_CHILD, EDUCATION_ALLOWANCE_PER_CHILD * self.num_children)

    def get_self_education_allowance(self):
        return min(self.self_education_allowance, SELF_EDUCATION_ALLOWANCE)

    def get_donation_allowance(self):
        # Correctly handle donations
        donation_limit = self.taxable_income * 0.05  # 5% of taxable income
        if self.donations > donation_limit:
            print(f"The donation amount exceeds the allowed limit of 5% of your income. Please enter a donation amount up to 5%.")
            self.donations = donation_limit
        return self.donations

    def get_sponsored_child_education_allowance(self):
        return min(self.num_children * SPONSORED_CHILD_EDUCATION_ALLOWANCE, SPONSORED_CHILD_EDUCATION_ALLOWANCE * self.num_children)

    def get_total_deductions(self):
        return self.get_education_allowance() + self.get_self_education_allowance() + self.get_donation_allowance() + self.get_sponsored_child_education_allowance()

class TaxCalculator:
    def __init__(self, taxable_income):
        self.taxable_income = taxable_income

    def calculate_tax(self):
        tax = 0
        for lower_bound, upper_bound, rate in TAX_BRACKETS:
            if self.taxable_income > lower_bound:
                taxable_at_this_rate = min(self.taxable_income, upper_bound) - lower_bound
                tax += taxable_at_this_rate * rate
        return tax

# Constants
TAX_BRACKETS = [
    (0, 300000, 0),
    (300001, 400000, 0.1),
    (400001, 650000, 0.15),
    (650001, 1000000, 0.2),
    (1000001, 1500000, 0.25),
    (1500001, float('inf'), 0.3)
]

MIN_TAXABLE_INCOME = 300000

EDUCATION_ALLOWANCE_PER_CHILD = 350000
SELF_EDUCATION_ALLOWANCE = 350000
SPONSORED_CHILD_EDUCATION_ALLOWANCE = 350000

def get_user_input():
    employees = []
    num_employees = int(input("Enter the number of employees: "))

    for i in range(num_employees):
        print(f"\nEnter details for Employee {i+1}:")
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        if age < 18:
            print("You are below 18. You are not required to pay tax.")
            continue

        marital_status = input("Is the employee single or married? (single/married): ").lower()
        
        income = float(input("Enter income: "))
        
        if marital_status == 'married':
            num_children = int(input("Enter number of children: "))
            children_allowance = 0
            while True:
                children_allowance = float(input(f"Enter children's education allowance (max {num_children * EDUCATION_ALLOWANCE_PER_CHILD}): "))
                if children_allowance <= num_children * EDUCATION_ALLOWANCE_PER_CHILD:
                    break
                else:
                    print(f"Children's education allowance cannot exceed {num_children * EDUCATION_ALLOWANCE_PER_CHILD}. Please re-enter.")
            sponsored_children_education_expense = 0
            while True:
                sponsored_children_education_expense = float(input(f"Enter sponsored children education expense (max {num_children * SPONSORED_CHILD_EDUCATION_ALLOWANCE}): "))
                if sponsored_children_education_expense <= num_children * SPONSORED_CHILD_EDUCATION_ALLOWANCE:
                    break
                else:
                    print(f"Sponsorship expense cannot exceed {num_children * SPONSORED_CHILD_EDUCATION_ALLOWANCE}. Please re-enter.")
        else:
            num_children = 0
            children_allowance = 0
            sponsored_children_education_expense = 0

        is_contract = input("Is the employee a contract employee? (y/n): ").lower() == 'y'
        org_type = input("Enter organization type (government/private/corporate): ").lower()
        pf_contribution = float(input("Enter PF contribution (0 if not applicable): "))
        gis_contribution = float(input("Enter GIS contribution (0 if not applicable): "))
        life_insurance_premium = float(input("Enter life insurance premium: "))
        self_education_allowance = float(input("Enter self-education allowance (max 350000): "))
        donations = float(input("Enter donations amount: "))
        dividend_income = float(input("Enter dividend income (0 if not applicable): "))
        rental_income = float(input("Enter rental income (0 if not applicable): "))

        employee = Employee(name, income, num_children, is_contract, org_type, pf_contribution, gis_contribution, life_insurance_premium, children_allowance, sponsored_children_education_expense, self_education_allowance, donations, dividend_income, rental_income)
        employees.append(employee)

    return employees

def main():
    employees = get_user_input()

    for employee in employees:
        if employee.income < MIN_TAXABLE_INCOME:
            print(f"{employee.name} is exempt from paying tax.")
        else:
            tax = employee.calculate_tax()
            if tax == 0:
                print(f"{employee.name} does not have to pay tax.")
            else:
                print(f"{employee.name} needs to pay Nu. {tax:.2f} as personal income tax.")

if __name__ == "__main__":
    main()
