import requests
import json


def get_data(ip):
	params = {}
	params['ip'] = ip
	params['full'] = 'full'
	params['mode'] = 'out'
	headers = {'x-api-key': 'CbZsUSM88EzE6I61m5fEKVO2FeLZExwzN14aoakZ'}

	res = requests.get('https://api.criminalip.com/getipdata?ip={}'.format(params['ip']), headers=headers)
	if res.status_code == 200:
		res = res.json()
		try:
			country = res['country'].replace(',','')
		except:
			country = 'None'
		try:
			is_cloud = res['is_cloud'].replace(',','')
		except:
			is_cloud = 'None'
		try:
			asn_name = res['list_whois_info'][0]['asn_name'].replace(',','')
		except:
			asn_name = 'None'
		return (country,is_cloud,asn_name)
	else:
		return ('None','None','None')

if __name__ == '__main__':

	fp = open('result.csv','r',encoding='cp949')
	lines = fp.readlines()
	fp.close()
	del lines[0]

	fp2 = open('result3.csv','w')
	fp2.write('main_url,main_ip,connect_url,connect_ip,keywords,banner_count,site_type,main_country,is_main_cloud,main_org,connect_country,is_connect_cloud,connect_org\n')

	for l in lines:
		l = l.strip()
		values = l.split(',')

		if values[1] != 'None':
			main_data = get_data(values[1]) # main_ip
		else:
			main_data = ('None','None','None')
		if values[3] != 'None':
			connect_data = get_data(values[3]) # connect_ip
		else:
			connect_data = ('None','None','None')

		l = l + ','+ ','.join(main_data+connect_data) + '\n'
		fp2.write(l)
	fp2.close()

