import sys


# tax bracket
income = [0, 36000, 144000, 300000, 420000, 660000, 960000]
rate = [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]
quick_del = [0, 2520, 16920, 31920, 52920, 85920, 181920]

def compute_tax(taxable):
    level = 6
    for n, i in enumerate(income):
        if i > taxable:
            level = n - 1
            break
    # print(rate[level])
    return taxable * rate[level] - quick_del[level]


################### salary configuration #########################

# 税前工资 (每年发放金额 = salary * salary_num)
salary = int(sys.argv[1])

# 多少薪 (如16薪、14薪等)
salary_num = int(sys.argv[2])

# 补助 (加班补助、租房补助、饭补等 - 和薪资不同，每年只发放12个月)
subsidy = int(sys.argv[3])

# 税前年薪
annual_salary_pre_tax = salary * salary_num + subsidy * 12
print('你的税前年薪为:', annual_salary_pre_tax)

################### salary configuration #########################

allowance = 5000  # 免税额 (每个月工资低于5000无需纳税)

deduction = 1500  # 专项扣除费用 (每个人不一样，自己填一下)

insurance = 6054.92  # 五险一金 (每家公司不一样，和工资成一定比例，自己填一下)

##################################################################

# 税后年薪
annual_salary_after_tax = 0

# 累计缴纳过的个人所得税 
accumulated_tax = 0  

# 计算每个月缴纳的个税以及税后收入
for i in range(1, 12 + 1):  # [1, 13)

    # 以下几项为税前扣除
    accumulated_insurance = insurance * i  # 累计五险一金
    accumulated_allowance = allowance * i  # 累计免税额
    accumulated_deduction = deduction * i  # 累计专项扣除

    # 累计个人所得
    if i < 12:
        accumulated_income = (salary + subsidy) * i
    elif i == 12:
        accumulated_income = annual_salary_pre_tax

    # 累计应税收入
    taxable = accumulated_income - accumulated_insurance - accumulated_deduction - accumulated_allowance

    # 累计应该缴纳的个人所得税
    tax = compute_tax(taxable)

    # 当前月份个税 = 累计应纳税额 - 已缴纳税额
    current_tax = tax - accumulated_tax
    accumulated_tax = tax

    # 当前月份税后收入 = 当前月份工资 + 当前月份补助 - 五险一金 - 当前月份个税
    if i < 12:
        current_after_tax = salary + subsidy - insurance - current_tax
    elif i == 12:  # 12月工资 + 12月补助 + 年终奖 - 12月五险一金 - 12月个人所得税(含年终奖税额)
        current_after_tax = salary + subsidy + salary * (salary_num - 12) - insurance - current_tax

    # 更新全年收入
    annual_salary_after_tax += current_after_tax

    print('{}月税后收入: {:.2f},'.format(i, current_after_tax), '当月个税{0:.2f}'.format(current_tax))


print('全年保险费用:', insurance * 12)
print('全年个税:', accumulated_tax)
print('全年税后收入:', annual_salary_after_tax)
print(insurance * 12 + accumulated_tax + annual_salary_after_tax, annual_salary_pre_tax)

