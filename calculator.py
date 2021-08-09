from PyQt5 import QtCore, QtGui, QtWidgets
from ui_qtcalculator import Ui_MainWindow

class CalculatorWindow(QtWidgets.QMainWindow,Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.temp_numbers = []
		self.perm_numbers = []
		self.latest_result = ""
		self.is_latest_result = False
		self.is_zero_division = False

		self.show()

		#UI FUNCTIONS
		## ==> MINIMIZE BUTTON
		self.button_minimize.clicked.connect(lambda: self.showMinimized())

		## ==> CLOSE BUTTON
		self.button_close.clicked.connect(lambda: self.close())

		## ==> ROMOVE DEFAULT WINDOW BOX
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

		## ==> MOVE WINDOW FUNCTION
		def moveWindow(event):
			if event.buttons() == QtCore.Qt.LeftButton:
				self.move(self.pos() + event.globalPos() -self.dragPos)
				self.dragPos = event.globalPos()
				event.accept()

		self.top_color.mouseMoveEvent = moveWindow

		self.show()
		#KEYPAD BUTTONS
		self.button_0.clicked.connect(lambda: self.number_press("0"))
		self.button_1.clicked.connect(lambda: self.number_press("1"))
		self.button_2.clicked.connect(lambda: self.number_press("2"))
		self.button_3.clicked.connect(lambda: self.number_press("3"))
		self.button_4.clicked.connect(lambda: self.number_press("4"))
		self.button_5.clicked.connect(lambda: self.number_press("5"))
		self.button_6.clicked.connect(lambda: self.number_press("6"))
		self.button_7.clicked.connect(lambda: self.number_press("7"))
		self.button_8.clicked.connect(lambda: self.number_press("8"))
		self.button_9.clicked.connect(lambda: self.number_press("9"))
		self.button_division.clicked.connect(lambda: self.operator_press("/"))
		self.button_multiplication.clicked.connect(lambda: self.operator_press("*"))
		self.button_minus.clicked.connect(lambda: self.operator_press("-"))
		self.button_plus.clicked.connect(lambda: self.operator_press("+"))
		self.button_clear.clicked.connect(self.special_operator_clear)
		self.button_pos_or_neg.clicked.connect(self.special_operator_pos_or_neg)
		self.button_percentage.clicked.connect(self.special_operator_percentage)
		self.button_decimal.clicked.connect(self.special_operator_decimal)
		self.button_equal.clicked.connect(self.special_operator_equal)


	#CALCULATOR FUNCTIONS
	def number_press(self, key_number):
		if (self.is_latest_result == False):
			self.temp_numbers.append(key_number)
			temp_string = "".join(self.temp_numbers)
			if ((len(temp_string) == 1) and (temp_string.count("0") == 1)):
				self.temp_numbers.pop(len(self.temp_numbers)-1)
				temp_string = "".join(self.temp_numbers)
			elif ((temp_string.count("0") + temp_string.count(".") == len(temp_string)) and (temp_string.count("0") != 1) and (temp_string.count("0.0") != 1)):
				self.temp_numbers.pop(len(self.temp_numbers)-1)
				temp_string = "".join(self.temp_numbers)			
			if self.perm_numbers:
				self.result_field.setText("".join(self.perm_numbers) + temp_string)
				self.label.clear()
			else:
				self.result_field.setText(temp_string)
				self.label.clear()
		else:
			self.latest_result += key_number
			self.result_field.setText(self.latest_result)
			self.label.clear()

	def operator_press(self, key_operator):
		if (self.is_latest_result == False):
			if (self.perm_numbers):
				if (((self.perm_numbers[len(self.perm_numbers)-1] == "+") or (self.perm_numbers[len(self.perm_numbers)-1] == "-") or (self.perm_numbers[len(self.perm_numbers)-1] == "/") or (self.perm_numbers[len(self.perm_numbers)-1] == "*")) and not(self.temp_numbers)):
					self.perm_numbers.pop(len(self.perm_numbers)-1)
					self.perm_numbers.append(key_operator)
					self.temp_numbers = []
					self.result_field.setText("".join(self.perm_numbers))
					self.label.clear()				
				else:
					temp_string = "".join(self.temp_numbers)
					self.perm_numbers.append(temp_string)
					self.perm_numbers.append(key_operator)
					self.temp_numbers = []
					self.result_field.setText("".join(self.perm_numbers))
					self.label.clear()
			else:
				temp_string = "".join(self.temp_numbers)
				self.perm_numbers.append(temp_string)
				self.perm_numbers.append(key_operator)
				self.temp_numbers = []
				self.result_field.setText("".join(self.perm_numbers))
				self.label.clear()				
		else:
			self.perm_numbers = list(self.latest_result)
			self.perm_numbers.append(key_operator)
			self.temp_numbers = []
			self.latest_result = ""
			self.is_latest_result = False
			self.result_field.setText("".join(self.perm_numbers))
			self.label.clear()

	def special_operator_equal(self):
		zero_division_test = "".join(self.perm_numbers) + "".join(self.temp_numbers) 
		try:
			eval(zero_division_test)
		except ZeroDivisionError as zde:
			self.is_zero_division = True

		if (self.is_zero_division == True):
			self.label.setText("Error")
			self.result_field.clear()
			self.temp_numbers = []
			self.perm_numbers = []
			self.latest_result = ""
			self.is_latest_result = False
			self.is_zero_division = False
		else:
			if (self.is_latest_result == True):
				result_string = eval(self.latest_result)
				self.latest_result = str(result_string)
				self.is_latest_result = True
				final_string = str(result_string)
				final_string += "="
				self.result_field.setText(final_string)
				self.label.setText(str(result_string))
			else:
				final_string = "".join(self.perm_numbers) + "".join(self.temp_numbers)
				if ((final_string[len(final_string)-1] == "+") or (final_string[len(final_string)-1] == "x") or (final_string[len(final_string)-1] == "/") or (final_string[len(final_string)-1] == "-")):
					button_press_void = 0
				else:
					test_temp_list = list(str(eval(final_string)))
					if ((test_temp_list[len(test_temp_list) -1] == "0") and (test_temp_list[len(test_temp_list) -2] == ".")):
						result_string = eval(final_string)
						temp_list = list(str(result_string))
						temp_list.pop(len(temp_list)-1)
						temp_list.pop(len(temp_list)-1)
						self.latest_result = "".join(temp_list)
						self.is_latest_result = True
						final_string += "="
						self.result_field.setText(final_string)
						self.label.setText(str(result_string))			
					else:
						result_string = eval(final_string)
						self.latest_result = str(result_string)
						self.is_latest_result = True
						final_string += "="
						self.result_field.setText(final_string)
						self.label.setText(str(result_string))

	def special_operator_clear(self):
		self.result_field.clear()
		self.label.setText("0")
		self.temp_numbers = []
		self.perm_numbers = []
		self.latest_result = ""
		self.is_latest_result = False

	def special_operator_pos_or_neg(self):
		if (self.is_latest_result == False):
			if not(self.temp_numbers):
				button_press_void = 0
			elif (self.temp_numbers):
				if (self.temp_numbers[0] != "-"):
					temp_string = "-"
					temp_string += "".join(self.temp_numbers)
					self.temp_numbers = list(temp_string)
					final_string = "".join(self.perm_numbers) + "".join(self.temp_numbers)
					self.result_field.setText(final_string)
					self.label.clear()
				else:
					self.temp_numbers.pop(0)
					final_string = "".join(self.perm_numbers) + "".join(self.temp_numbers)
					self.result_field.setText(final_string)
					self.label.clear()
			else:
				if (self.temp_numbers[0] != "-"):
					temp_string = "-"
					temp_string += "".join(self.temp_numbers)
					self.temp_numbers = []
					self.temp_numbers = list(temp_string)
					self.result_field.setText(temp_string)
					self.label.clear()
				else:
					self.temp_numbers.pop(0)
					self.result_field.setText("".join(self.temp_numbers))
					self.label.clear()
		else:
			if (self.latest_result[0] != "-"):
				temp_string = "-"
				temp_string += self.latest_result
				self.temp_numbers = []
				self.temp_numbers = list(temp_string)
				self.latest_result = temp_string
				self.result_field.setText(temp_string)
				self.label.clear()
			else:
				temp_list = list(self.latest_result)
				temp_list.pop(0)
				self.result_field.setText("".join(temp_list))
				self.latest_result = "".join(temp_list)
				self.label.clear()			

	def special_operator_percentage(self):
		if (self.is_latest_result == False):
			if (self.temp_numbers):
				temp_string = "".join(self.temp_numbers)
				second_temp_string = float(temp_string)/100
				self.temp_numbers = []
				self.temp_numbers = list(str(second_temp_string))
				if self.perm_numbers:
					self.result_field.setText("".join(self.perm_numbers) + "".join(self.temp_numbers))
					self.label.clear()
				else:
					self.result_field.setText("".join(self.temp_numbers))
					self.label.clear()
		else:
			temp_string = float(self.latest_result)/100
			self.latest_result = str(temp_string)
			self.result_field.setText(str(temp_string))
			self.label.clear()


	def special_operator_decimal(self):
		if (self.is_latest_result == False):
			if (self.temp_numbers):
				if (self.temp_numbers.count(".") == 0):
					self.temp_numbers.append(".")
					self.result_field.setText("".join(self.perm_numbers) + "".join(self.temp_numbers))
					self.label.clear()
			else:
				if (self.temp_numbers.count(".") == 0):
					self.temp_numbers.append("0")
					self.temp_numbers.append(".")
					self.result_field.setText("".join(self.perm_numbers) + "".join(self.temp_numbers))
					self.label.clear()
		else:
			if (self.latest_result.count(".") == 0):
				self.latest_result += "."
				self.result_field.setText(self.latest_result)
				self.label.clear()

	def mousePressEvent(self, event):
		self.dragPos = event.globalPos()