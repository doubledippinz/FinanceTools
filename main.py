import datetime

currentyear = datetime.date.today().year
year3 = (datetime.date.today().year - 3)
year2 = datetime.date.today().year - 2
year1 = datetime.date.today().year - 1
aathreshold = 240000
aallowance = 40000
maxaareduction = 36000


class Client:

    def __init__(self, name, salary, bonus, intdiv, employeepercent, employerpercent, pensionlump, salaryexchange,
                 deathbenefits):
        self.name = name
        self.salary = salary
        self.bonus = bonus
        self.intdiv = intdiv
        self.employeecontribution = salary * (employeepercent / 100)
        self.employercontribution = salary * (employerpercent / 100)
        self.pensionlump = pensionlump
        self.salaryexchange = salaryexchange
        self.deathbenefits = deathbenefits
        self.totalgross = salary + bonus + intdiv

    @classmethod
    def from_input(cls):
        return cls(input('Name: '),
                   int(input('Salary + Bonus: ')),
                   int(input('Bonus & Comission')),
                   int(input('Interest & Dividends: ')),
                   int(input('Employee gross workplace contribution % : ')),
                   int(input('Employer gross workplace contribution % :')),
                   int(input('Lump sum contributions: ')),
                   int(input('Employment income given through salary exchange')),
                   int(input('Taxed lump sum death benefits: '))
                   )

    @staticmethod
    def get_carryforward():

        def cap_carryforward(contribution):
            if contribution > aallowance:
                contribution = aallowance
                remaining_allowance = aallowance - contribution
                return remaining_allowance
            else:
                remaining_allowance = aallowance - contribution
                return remaining_allowance

        print("Please enter your pension contributions for ", year3)
        year3contribution = int(input())
        year3remallowance = cap_carryforward(year3contribution)
        print("Please enter your pension contributions for ", year2)
        year2contribution = int(input())
        year2remallowance = cap_carryforward(year2contribution)
        print("Please enter your pension contributions for ", year1)
        year1contribution = int(input())
        year1remallowance = cap_carryforward(year1contribution)
        cf_allowance = year3remallowance + year2remallowance + year1remallowance
        return cf_allowance

    def get_threshold(self):
        threshinc = self.totalgross - self.pensionlump - self.employeecontribution + self.salaryexchange - self.deathbenefits
        return threshinc

    def get_adjustedincome(self):
        adjustedinc = self.totalgross + self.employercontribution - self.deathbenefits
        return adjustedinc

    def get_annualallowance(self):
        taperexcess = 0
        if Client.get_adjustedincome(self) > aathreshold:
            taperexcess = (Client.get_adjustedincome(self) - aathreshold) / 2
            if taperexcess > maxaareduction:
                taperexcess = maxaareduction
        annualallowance = aallowance - taperexcess
        return annualallowance


c = Client.from_input()

# print(c.get_threshold())
# print(c.get_adjustedincome())
# print(c.get_annualallowance())

print(c.get_carryforward())
