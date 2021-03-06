import os

import datetime

currentyear = datetime.date.today().year
year3 = (datetime.date.today().year - 3)
year2 = datetime.date.today().year - 2
year1 = datetime.date.today().year - 1

aathreshold = 240000
aallowance = 40000
maxaareduction = 36000
personalallowance = 12570
pathreshold = 100000
basic_rate = 50270
higher_rate = 150000
additiional_rate = 150000


class Client:
    def __init__(self, name, salary, bonus, interest, employeepercent, employerpercent, pensionlump, salaryexchange,
                 deathbenefits, year3contribution, year2contribution, year1contribution):
        self.name = name
        self.salary = salary
        self.bonus = bonus
        self.interest = interest
        self.employeecontribution = salary * (employeepercent / 100)
        self.employercontribution = salary * (employerpercent / 100)
        self.pensionlump = pensionlump
        self.salaryexchange = salaryexchange
        self.deathbenefits = deathbenefits
        self.totalgross = salary + bonus + interest
        self.totalannualpensioncontributions = self.employeecontribution + self.employercontribution + self.pensionlump
        self.year3contribution = year3contribution
        self.year2contribution = year2contribution
        self.year1contribution = year1contribution

    @classmethod
    def from_input(cls):
        return cls(input('Name: '),
                   int(input('Salary + Bonus: ')),
                   int(input('Bonus & Comission: ')),
                   int(input('Interest : ')),
                   int(input('Employee gross workplace contribution % : ')),
                   int(input('Employer gross workplace contribution % :')),
                   int(input('Lump sum contributions: ')),
                   int(input('Employment income given through salary exchange')),
                   int(input('Taxed lump sum death benefits: ')),
                   int(input(f'Please enter your pension contributions for {year3}: ')),
                   int(input(f'Please enter your pension contributions for {year2}: ')),
                   int(input(f'Please enter your pension contributions for {year1}: '))
                   )

    def get_taxableincome(self):
        taxableinc = self.salary + self.interest + self.bonus
        return taxableinc

    def get_threshold(self):
        threshinc = self.totalgross - self.pensionlump - self.employeecontribution \
                    + self.salaryexchange - self.deathbenefits
        return threshinc

    def get_adjustedincome(self):
        adjustedinc = self.totalgross + self.employercontribution - self.deathbenefits
        return adjustedinc

    def get_adjustednetincome(self):
        adjustednetinc = self.totalgross - self.employeecontribution - self.pensionlump
        return adjustednetinc

    def calculate_personal_allowance(self):
        if self.get_adjustednetincome() > pathreshold:
            reductionamount = (self.get_adjustednetincome() / 2) - pathreshold
            print(reductionamount)
            new_personal_allowance = personalallowance - reductionamount
            if new_personal_allowance <= 0:
                new_personal_allowance = 0
                return new_personal_allowance
            else:
                return new_personal_allowance
        else:
            new_personal_allowance = 0
            return new_personal_allowance

    def get_remaining_aa(self):
        taperexcess = 0
        if Client.get_adjustedincome(self) > aathreshold:
            taperexcess = (Client.get_adjustedincome(self) - aathreshold) / 2
            if taperexcess > maxaareduction:
                taperexcess = maxaareduction
        annualallowance = aallowance - taperexcess
        remaining_aa = annualallowance - self.totalannualpensioncontributions
        if remaining_aa <= 0:
            remaining_aa = 0
        return remaining_aa

    def get_carryforward(self):
        def cap_carryforward(contribution):
            if contribution > aallowance:
                contribution = aallowance
                remaining_allowance = aallowance - contribution
                return remaining_allowance
            else:
                remaining_allowance = aallowance - contribution
                return remaining_allowance

        year3remallowance = cap_carryforward(self.year3contribution)
        year2remallowance = cap_carryforward(self.year2contribution)
        year1remallowance = cap_carryforward(self.year1contribution)
        cf_allowance = year3remallowance + year2remallowance + year1remallowance
        return cf_allowance

    def get_maximum_contribution(self):
        combinedallowance = (Client.get_remaining_aa(self) + Client.get_carryforward(self))
        if (self.salary - combinedallowance) <= 0:
            maxcontribution = self.salary
            return maxcontribution
        elif (self.salary - combinedallowance) > 0:
            maxcontribution = combinedallowance
            return maxcontribution

    def __str__(self):
        line1 = f"{self.name} Maximum pension contribution you can make personally this tax year: {self.get_maximum_contribution()} "
        line3 = f"{self.name} Remaining annual allowance:   {self.get_remaining_aa()}"
        line4 = f"{self.name} Carryforward available:   {self.get_carryforward()}"
        return os.linesep.join([line1, line3, line4])


# Main
# Specify how many clients

num_clients = int(input("How many people would you like to assess? "))
client_list = [Client.from_input() for _ in range(num_clients)]
for client in client_list:
    print(client)