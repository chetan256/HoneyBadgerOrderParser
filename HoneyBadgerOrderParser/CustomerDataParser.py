import os
from collections import defaultdict,OrderedDict
from jinja2 import Environment, FileSystemLoader
class CustomerDataParser:
	'''This class consists of methods and attributes to process customer data and generate HTML reports
	from this data'''

	def __init__(self, datafile):
		print "Initializing CustomerDataParser Object..."
		self.TotalOrders = 0
		self.TotalAmount = 0
		self.OrderedOnce = []
		self.OrderSummary = OrderedDict()
		self.OrderDistribution = defaultdict(int)
		self.SingleOrder = ''
		self.Columns = []
		self.DataFile = datafile
		self.CurDir = os.path.dirname(os.path.realpath(__file__))
		self.load_html_template()

	def process_orders(self):
		'''
		author : cc
		process_orders - will Parse Data from file and process the data
		'''
		print "\nProcessing file " + self.DataFile
		with open(self.DataFile,'r') as f:
			for line in f:
				data = line.strip().split(', ')
				if not self.Columns: 
					self.Columns = data #Assign Column Names from first line
				else:
					self.TotalOrders+=1
					self.TotalAmount+=int(data[3])
					self.OrderDistribution[data[2]]+=1
		print "\nTotal Orders:" + str(self.TotalOrders)
		print "\nTotal Amount of all orders:" + str(self.TotalAmount)
		self.generate_table_data()
		self.create_html_report()

	def generate_table_data(self):
		'''
		author : cc
		generate_table_data() - will generate data for the HTML Report
		'''
		self.OrderDistributionCount = [0]*5
		get_index = lambda i:i-1 if i<5 else 4
		for ele in self.OrderDistribution.items():
			self.OrderDistributionCount[get_index(ele[1])]+=1
			if ele[1] == 1:
				self.SingleOrder+=ele[0]+', '
		self.OrderSummary = {'Total Orders Received':self.TotalOrders,'Total Amount of Orders':self.TotalAmount}
		self.OrderSummary['Single Order'] = self.SingleOrder
		print "\nCustomers Who ordered only once: " + self.SingleOrder
		for index in xrange(len(self.OrderDistributionCount)):
			print "\nNumber of Customers Who made " + str(index+1) + " Order: " + str(self.OrderDistributionCount[index])


	def load_html_template(self):
		'''
		author : cc
		load_html_template() - will load the HTML template
		'''
		TemplateName = 'report_template.html'
		print "\nLoading HTML Template " + TemplateName
		env = Environment(loader=FileSystemLoader(self.CurDir),extensions=["jinja2.ext.do",])
		self.template = env.get_template(TemplateName)

	def create_html_report(self):
		'''
		Author: cc
		create_html_report - will create the html report'''
		print "\nGenerating HTML Report"
		output_from_parsed_template = self.template.render(ordersummary=self.OrderSummary,orderdistributioncount=self.OrderDistributionCount)
		fn = os.path.join(self.CurDir,'output.html')
		with open(fn, "wb") as fh:
		   fh.write(output_from_parsed_template)
		print "\nReport output.html successfully created in current Directory!!!"

if __name__=='__main__':
	DataObj = CustomerDataParser('customerdata.txt')
	DataObj.process_orders()