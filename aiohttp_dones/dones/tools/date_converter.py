import datetime, time, json

class Date_converter():
	@staticmethod
	def jalali_to_gregorian(jy,jm,jd):
		g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
		jy = jy - 979
		jm = jm - 1
		jd = jd - 1
		j_day_no = 365*jy +int(jy//33)*8 + (jy%33+3)//4
		for i in range(jm):
			j_day_no += j_days_in_month[i]
		j_day_no += jd
		g_day_no = j_day_no+79
		gy = 1600 + 400*int(g_day_no// 146097) # 146097 = 365*400 + 400/4 - 400/100 + 400/400
		g_day_no = g_day_no % 146097
		leap = 1
		if g_day_no >= 36525: # 36525 = 365*100 + 100/4
			g_day_no-=1
			gy += 100*int(g_day_no// 36524) # 36524 = 365*100 + 100/4 - 100/100
			g_day_no = g_day_no % 36524

			if g_day_no >= 365:
				g_day_no+=1
			else:
				leap = 0
		gy += 4*int(g_day_no//1461) # 1461 = 365*4 + 4/4
		g_day_no %= 1461

		if g_day_no >= 366:
			leap = 0
			g_day_no-=1
			gy += g_day_no//365
			g_day_no = g_day_no % 365
		i=0
		while g_day_no >= g_days_in_month[i] + (i == 1 and leap):
			g_day_no -= g_days_in_month[i] + (i == 1 and leap)
			i+=1
		gmonth = i+1
		gday = g_day_no+1
		gyear = gy
		return [gyear, gmonth, gday]

	@staticmethod
	def gregorian_to_jalali(gy,gm,gd):
		g_d_m=[0,31,59,90,120,151,181,212,243,273,304,334]
		if(gy>1600):
			jy=979
			gy-=1600
		else:
			jy=0
			gy-=621
		if(gm>2):
			gy2=gy+1
		else:
			gy2=gy
		days=(365*gy) +(int((gy2+3)/4)) -(int((gy2+99)/100)) +(int((gy2+399)/400)) -80 +gd +g_d_m[gm-1]
		jy+=33*(int(days/12053))
		days%=12053
		jy+=4*(int(days/1461))
		days%=1461
		if(days > 365):
			jy+=int((days-1)/365)
			days=(days-1)%365
		if(days < 186):
			jm=1+int(days/31)
			jd=1+(days%31)
		else:
			jm=7+int((days-186)/30)
			jd=1+((days-186)%30)
		return [jy,jm,jd]

	@staticmethod
	def unix_timestamp_to_jalali(unix_timestamp):
		gregorian_datetime = Date_converter.unix_timestamp_to_gregorian(unix_timestamp)
		jalali_start_datetime = '/'.join(str(item) for item in Date_converter.gregorian_to_jalali(gregorian_datetime.year, gregorian_datetime.month, gregorian_datetime.day))
		return jalali_start_datetime

	@staticmethod
	def jalali_to_unix_timestamp(jy,jm,jd, h=0, m=0, s=0):
		g = Date_converter.jalali_to_gregorian(jy,jm,jd)
		unix_time = Date_converter.gregorian_to_unix_timestamp(g[0],g[1],g[2], h, m, s)
		return unix_time

	@staticmethod
	def unix_timestamp_to_gregorian(unix_timestamp):
		local_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
		return local_datetime
	
	@staticmethod
	def gregorian_to_unix_timestamp(gy,gm,gd, h=0, m=0, s=0):
		d = datetime.datetime(gy,gm,gd, h, m, s)
		unix_time = int(datetime.datetime.timestamp(d))
		return unix_time

	


