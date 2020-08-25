import pandas as pd
import numpy as np
import os
import calendar
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .pdf_convertor import pdf_convert
from .data_formating import input_data_formatting, num_to_words_convert
import locale




@api_view(['GET'])
def salary_slip_generate(request):
    if request.method == 'GET':
        data = request.data
        inputfile = data['file']
        df = pd.read_excel(inputfile, keep_default_na=False, dtype=str, na_values=['']) # read excel file
        df = df.replace(r'^\s+$', np.nan, regex=True) # replace white space with Nan
        try:
            # remove col/row if entire rows or columns is Nan
            # find index number(row, column) with Nan
            nan_list_rows = df[df.isnull().all(axis='columns')].index.tolist()
            nan_list_cols = df.columns[df.isnull().all(axis='index')].tolist()

            # Check the last row present in nan_list_rows or nan_list_cols and the difference between the elements present
            # in nan_list_rows or nan_list_cols is one(1), then to delete rows/columns that are immediate ones not in the middle
            # of the input grid
            if df.shape[1] - 1 in nan_list_cols and np.all(np.diff(np.array(nan_list_cols)) == 1):
                df = df.dropna(axis='columns', how='all')
            if df.shape[0] - 1 in nan_list_rows and np.all(np.diff(np.array(nan_list_rows)) == 1):
                df = df.dropna(axis='index', how='all')

            #replace nan with blanck space
            df = df.replace(np.nan, '', regex=True)
        except:
            pass

        # convert dataframe to dictionary, index as key and data values
        dict2 = df.to_dict('index')
        data_list = []  # make list of dictionary
        for value in dict2.values():
            value_dict2 = {}
            for key, val in value.items():
                value_dict2[key.strip()]=val     # for removing white space in input columns
            l = []
            l.append(value_dict2)
            data_list.append(l)

       # created folder for store PDF file
        path1 = "E:\\Salary_slip_pdf\\"
        try:
            os.mkdir(path1)
        except:
            pass


        # iterate loop till no. of row in your input file, data_list
        for i in range(len(data_list)):
            # for handling key not found error, keyError------------------------------------
            dict_key = []  # store input file column name(key) in dict_key
            html_key = []  # html page static, key fixed ex-> {Basic PaY}
            html_key = ['Company name', 'Salary slip for the month', 'Employee Code', 'Employee Name', 'Designation', 'Bank Name', 'Bank Account Number', 'PAN', 'PF UAN Number', 'Total Days', 'Days Worked', 'LOP Days', 'Basic Pay', 'House Rent Allowance', 'Special Allowance', 'Additional Allowance', 'Advance Incentive', 'Gross Salary', 'Provident Fund', 'Contribution', 'Loan', 'Professiaonal Tax', 'TDS/IT', 'Total Deduction', 'Net Payable', 'Opening', 'Earned', 'Availed', 'Leave without Pay', 'Closing']

            for key in data_list[i][0].keys():
                dict_key.append(key)

            dict_html_set = set(html_key) - set(dict_key)
            dict_input_column = set(dict_key) - set(html_key)

            # handling key error if it input file column and html key not macth, throw error
            if len(dict_key) == len(html_key):
             # if key of input file and html key match then, matching key will substract, length=0 (dict_html_set)
                if len(dict_html_set) == 0 :

                    leave_day = float(data_list[i][0]['Leave without Pay'])
                    date = data_list[i][0]['Salary slip for the month'].split()

                    # convert integer value to month name
                    date1 = date[0].split('-')
                    y, m = date1[0], date1[1]
                    date_month = calendar.month_name[int(m)] + " " + y

                    file_name = "Salary-Slip" + " " + data_list[i][0]['Employee Name'] + " " + date_month
                    html_file_name = file_name + ".html"  # html file name
                    pdf_file_name = file_name + ".pdf"  # pdf file name
                    html_full_path = os.path.join('E:\\parwej\code office\\salary_slip\\salary_slipApp\\template\\', html_file_name)  # html file path
                    pdf_full_path = os.path.join(path1, pdf_file_name)  # pdf full path(pdf file will store this location)

                    # checking leave without pay is greater, if leave_day > 0, need to add one more column according to requirements.
                    if leave_day > 0 :
                        # reading html template
                        with open('E:\\parwej\code office\\salary_slip\\salary_slipApp\\template\\salary_template_leave_balance.html', 'r') as rd:
                            data_template = rd.read()
                        # key, value pair of input file
                        for dict_data in data_list[i]:
                            # adding gross emoluments.
                            s1 = sum([float(dict_data['Basic Pay']), float(dict_data['House Rent Allowance']),
                                      float(dict_data['Special Allowance']), float(dict_data['Advance Incentive']),
                                      float(dict_data['Additional Allowance'])])
                            locale.setlocale(locale.LC_ALL, '')
                            d1 = {'Gross Emoluments': locale.format("%.2f", s1, grouping=True)}
                            dict_data.update(d1)

                            # for show date in template file, make dictionary for store date
                            date_month_dict = {'date_month_dict': date_month}
                            dict_data.update(date_month_dict)

                            # convert integer data to words formate --> ex- 20.25 twenty rupees and .25 convert it into paisa (twenty five paisa), Import num2words
                            net_pay = float("%.2f" % float(dict_data['Net Payable']))
                            num_to_words_convert(net_pay, dict_data)

                            # given column value like 5000 ,convert decimal no. with two digit and comma with number ex-> 5,000.00 and store in dict_data
                            input_data_formatting(dict_data)

                            # check if key of dict_data == data_template, key match insert value of dict_data in html template
                            d = data_template.format(**dict_data)  #if key not match means input file have a space in column or may be html {key} key error , not accept dot between column name(aa.bb)

                            #  write data in html template
                            with open(html_full_path, 'w') as wf:
                                wf.write(d)

                        # calling function to convert PDF
                        pdf_convert(html_full_path, pdf_full_path)

                        # after converting html to pdf, delete html file
                        os.remove(html_full_path)

                    else:
                        # read html template from dir
                        with open('E:\\parwej\code office\\salary_slip\\salary_slipApp\\template\\salary_slip_template.html', 'r') as rd:
                            data_template = rd.read()

                        for dict_data in data_list[i]:  # key, value pair of input file
                            # adding gross emoluments.
                            s1=sum([float(dict_data['Basic Pay']), float(dict_data['House Rent Allowance']),
                                    float(dict_data['Special Allowance']), float(dict_data['Advance Incentive']),
                                    float(dict_data['Additional Allowance'])])
                            locale.setlocale(locale.LC_ALL, '')
                            d1 = {'Gross Emoluments': locale.format("%.2f", s1, grouping=True)}
                            dict_data.update(d1)

                            # for showing month, year in template file, make dictionary for store date
                            date_month_dict = {'date_month_dict': date_month}
                            dict_data.update(date_month_dict)

                            # convert integer data to words formate --> ex- 20 twenty, import num2words, .25 convert it into paisa (twenty five paisa)
                            net_pay = float("%.2f" % float(dict_data['Net Payable']))
                            num_to_words_convert(net_pay, dict_data)

                            # calling function to convert number(5000), decimal no. with two digit and comma with number 5,000.00 and store in dict_data
                            input_data_formatting(dict_data)

                            # check if key of dict_data == data_template, key match insert value of dict_data in html template
                            d = data_template.format(**dict_data)  # if key not match means input file have a space in column or may be html {key} key error , not accept dot between column name(aa.bb)

                            #  write data in html template
                            with open(html_full_path, 'w') as wf:
                                wf.write(d)

                        # calling function to convert PDF
                        pdf_convert(html_full_path, pdf_full_path)

                        # after converting html to pdf, delete html file
                        os.remove(html_full_path)

                else:
                    msg = 'Input file columns_name {} is not matching with required key {}'.format(dict_input_column, dict_html_set)
                    return  Response(msg, status=status.HTTP_404_NOT_FOUND)
            else:
                msg = 'Length of input file columns and length required key not equal, should length = {}'.format(len(html_key))
                return Response(msg, status=status.HTTP_205_RESET_CONTENT)

        return Response('created {} PDF file in dir {}'.format(len(data_list), path1),status=status.HTTP_201_CREATED)