import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import sys
axes = plt.gca()
axes.yaxis.grid()
axes.xaxis.grid()


def calculate_daily_baseline(value, interest_rate_per_annum, days, 
	days_in_year=365, restake=None, restake_fee=0, interest_inflation_per_annum=0):
	hours_in_year = days_in_year * 24
	hours_in_quarter = hours_in_year//4
	hours_in_month = hours_in_year//12
	hours_in_day = 24
	hours_in_2day = hours_in_day*2
	hours_in_3day = hours_in_day*3
	hours_in_4day = hours_in_day*4
	hours_in_5day = hours_in_day*5
	hours_in_6day = hours_in_day*6
	hours_in_week = hours_in_day*7

	procentage_per_hour = interest_rate_per_annum/100/hours_in_year
	
	x = []
	y = []

	earn = 0
	last_earn = 0
	hours = days*24
	for hour in range(hours):
		x.append(hour/24)
		y.append(earn)

		if hour%hours_in_year == 0:
			procentage_per_hour-(procentage_per_hour*interest_inflation_per_annum/100)

		if (restake == "hour"
			or (restake == "day" and hour%hours_in_day == 0)
			or (restake == "2days" and hour%hours_in_2day == 0)
			or (restake == "3days" and hour%hours_in_3day == 0)
			or (restake == "4days" and hour%hours_in_4day == 0)
			or (restake == "5days" and hour%hours_in_5day == 0)
			or (restake == "6days" and hour%hours_in_6day == 0)
			or (restake == "week" and hour%hours_in_week == 0)
			or (restake == "month" and hour%hours_in_month == 0)
			or (restake == "quarter" and hour%hours_in_quarter == 0)
			or (restake == "year" and hour%hours_in_year == 0)
			):
			value += (last_earn - restake_fee)
			last_earn = 0
		last_earn += procentage_per_hour*value
		earn += procentage_per_hour*value

	return x, y, 

def get_values_from_ags():
	ret = {
		"value": 0, 
		"interest_rate_per_annum": 12, 
		"days": 365, 
		"days_in_year": 365, 
		"restake_fee": 0.0002, 
		"interest_inflation_per_annum": 1,
	}
	if 'help' in sys.argv[1:]:
		return

	for arg in sys.argv[1:]:
		name, value = arg.split("=")
		if name not in ret.keys():
			raise AttributeError(f"Unknown argument {arg}")
		if name in ["days", "days_in_year"]:
			ret[name] = int(value)
		elif name in ["value", "interest_rate_per_annum", "restake_fee", "interest_inflation_per_annum"]:
			ret[name] = float(value)
		else:
			ret[name] = value
	axes.xaxis.set_major_locator(MultipleLocator(ret['days']//12))
	return ret


def show_help():
	msg = """
------------------------------------------------ Instruction -----------------------------------------------
- help - show help
------------------------------------------------------------------------------------------------------------
- value - amount of cash at the beginning
- interest_rate_per_annum - a.p (default 12)
- days - days of deposit (default 365)
- days_in_year - days in year (default 365), year on the Earth is 365 or 366 days, on the Mars may be less.
- restake_fee - fee of restake (default 0.0002)
- interest_inflation_per_annum - inflation in percents of `interest_rate_per_annum` per year (default 1)
------------------------------------------------------------------------------------------------------------
example:
python crypto_restake.py value=10000 days=780
------------------------------------------------------------------------------------------------------------
	"""
	print(msg)


if __name__ == '__main__':
	kwargs = get_values_from_ags()
	if kwargs is None:
		show_help()
	else:
		interest_rate_per_annum = kwargs['interest_rate_per_annum']
		interest_inflation_per_annum = kwargs['interest_inflation_per_annum']

		# plt.plot(*calculate_daily_baseline(restake="hour", **kwargs), label=f"Restake every hour")
		plt.plot(*calculate_daily_baseline(restake="day", **kwargs), '--', label=f"Restake every day")
		plt.plot(*calculate_daily_baseline(restake="2days", **kwargs), label=f"Restake every 2 days")
		plt.plot(*calculate_daily_baseline(restake="3days", **kwargs), '--', label=f"Restake every 3 days",)
		plt.plot(*calculate_daily_baseline(restake="4days", **kwargs), label=f"Restake every 4 days")
		plt.plot(*calculate_daily_baseline(restake="5days", **kwargs), '--', label=f"Restake every 5 days",)
		plt.plot(*calculate_daily_baseline(restake="6days", **kwargs), label=f"Restake every 6 days")
		plt.plot(*calculate_daily_baseline(restake="week", **kwargs), '--', label=f"Restake every week")
		plt.plot(*calculate_daily_baseline(restake="month", **kwargs), label=f"Restake every month")
		plt.plot(*calculate_daily_baseline(restake="quarter", **kwargs), '--', label=f"Restake every quarter")
		plt.plot(*calculate_daily_baseline(restake="year", **kwargs), label=f"Restake  every year")
		# plt.plot(*calculate_daily_baseline(**kwargs), label=f"Without restake")

		plt.legend()
		plt.title(f"Interest rate per annum {interest_rate_per_annum}%. inflation  of interest rate per annum {interest_inflation_per_annum}%")
		plt.xlabel("Days")
		plt.ylabel("Income [currency]")
		plt.show()
