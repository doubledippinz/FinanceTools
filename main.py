# import datetime
# currentyear = datetime.date.today().year
# year3 = (datetime.date.today().year - 3)
# year2 = datetime.date.today().year - 2
# year1 = datetime.date.today().year - 1
aathreshold = 240000
aallowance = 40000
maxaareduction = 36000


class Client:
    def __init__(self, name, salary, bonus, intdiv, employeepercent, employerpercent, pensionlump, salaryexchange,
                 deathbenefits, year3contribution, year2contribution, year1contribution):
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
        self.totalannualpensioncontributions = self.employeecontribution + self.employercontribution + self.pensionlump
        self.year3contribution = year3contribution
        self.year2contribution = year2contribution
        self.year1contribution = year1contribution

    @classmethod
    def from_input(cls):
        return cls(input('Name: '),
                   int(input('Salary + Bonus: ')),
                   int(input('Bonus & Comission: ')),
                   int(input('Interest & Dividends: ')),
                   int(input('Employee gross workplace contribution % : ')),
                   int(input('Employer gross workplace contribution % :')),
                   int(input('Lump sum contributions: ')),
                   int(input('Employment income given through salary exchange')),
                   int(input('Taxed lump sum death benefits: ')),
                   int(input('Please enter your pension contributions for 2018: ')),
                   int(input('Please enter your pension contributions for 2019: ')),
                   int(input('Please enter your pension contributions for 2020: '))
                   )

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

    def get_threshold(self):
        threshinc = self.totalgross - self.pensionlump - self.employeecontribution\
                    + self.salaryexchange - self.deathbenefits
        return threshinc

    def get_adjustedincome(self):
        adjustedinc = self.totalgross + self.employercontribution - self.deathbenefits
        return adjustedinc

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

    def get_maximum_contribution(self):
        combinedallowance = (Client.get_remaining_aa(self) + Client.get_carryforward(self))
        if (self.salary - combinedallowance) <= 0:
            maxcontribution = self.salary
            return maxcontribution
        elif (self.salary - combinedallowance) > 0:
            maxcontribution = combinedallowance
            return maxcontribution



client1 = Client.from_input()
print(client1.name, 'Maximum pension contribution you can make this tax year: ', client1.get_maximum_contribution())
print(client1.name, 'Maximum pension contribution your employer can make this year: ', client1.get_carryforward() + client1.get_remaining_aa())
print(client1.name, 'Remaining annual allowance: ', client1.get_remaining_aa())
print(client1.name, 'Carryforward available: ', client1.get_carryforward())

client2 = Client.from_input()

print(client2.name, 'Maximum pension contribution you can make this tax year: ', client2.get_maximum_contribution())
print(client2.name, 'Maximum pension contribution your employer can make this year: ', client2.get_carryforward() + client1.get_remaining_aa())
print(client2.name, 'Remaining annual allowance: ', client2.get_remaining_aa())
print(client2.name, 'Carryforward available: ', client2.get_carryforward())



