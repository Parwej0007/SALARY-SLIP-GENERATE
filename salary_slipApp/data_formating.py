# purpose of module formatting number (ex-> 5000), decimal no. with two digit and comma separated number 5,000.00 and store in dict_data
#purpose of module convert integer data to words formate --> ex- 20 twenty, import num2words, .25 convert it into paisa (twenty five paisa)


import locale
from num2words import num2words


def input_data_formatting(dict_data):
    locale.setlocale(locale.LC_ALL, '')  # utf-8 type

    dict_data['Basic Pay'] = locale.format("%.2f", float(dict_data['Basic Pay']), grouping=True)
    dict_data['House Rent Allowance'] = locale.format("%.2f", float(dict_data['House Rent Allowance']), grouping=True)
    dict_data['Special Allowance'] = locale.format("%.2f", float(dict_data['Special Allowance']), grouping=True)
    dict_data['Additional Allowance'] = locale.format("%.2f", float(dict_data['Additional Allowance']), grouping=True)
    dict_data['Advance Incentive'] = locale.format("%.2f", float(dict_data['Advance Incentive']), grouping=True)
    dict_data['Provident Fund'] = locale.format("%.2f", float(dict_data['Provident Fund']), grouping=True)
    dict_data['Gross Salary'] = locale.format("%.2f", float(dict_data['Gross Salary']), grouping=True)
    dict_data['Contribution'] = locale.format("%.2f", float(dict_data['Contribution']), grouping=True)
    dict_data['Loan'] = locale.format("%.2f", float(dict_data['Loan']), grouping=True)
    dict_data['Professiaonal Tax'] = locale.format("%.2f", float(dict_data['Professiaonal Tax']), grouping=True)
    dict_data['TDS/IT'] = locale.format("%.2f", float(dict_data['TDS/IT']), grouping=True)
    dict_data['Total Deduction'] = locale.format("%.2f", float(dict_data['Total Deduction']), grouping=True)
    dict_data['Net Payable'] = locale.format("%.2f", float(dict_data['Net Payable']), grouping=True)


def num_to_words_convert(net_pay, dict_data):
    if '.' in str(net_pay):
        rupees, paisa = str(net_pay).split('.')
        if int(paisa) > 0:
            rupees = num2words(int(rupees))
            paisa = num2words(int(paisa))
            rupees = ' '.join(
                word for word in rupees.split(','))  # remove comma into words ex-> five thousand, two hundred
            net_pay = '{}, {} paisa'.format(rupees, paisa)
            net_pay_words = {'net_pay_words': net_pay.title()}
            dict_data.update(net_pay_words)
        else:
            rupees = num2words(int(rupees))
            rupees = ' '.join(
                word for word in rupees.split(','))  # remove comma into words ex-> five thousand, two hundred
            net_pay_words = {'net_pay_words': rupees.title()}
            dict_data.update(net_pay_words)

    else:
        rupees = num2words(net_pay)
        rupees = ' '.join(word for word in rupees.split(','))  # remove comma into words ex-> five thousand, two hundred
        net_pay_words = {'net_pay_words': rupees.title()}
        dict_data.update(net_pay_words)