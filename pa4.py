# File: pa4.py
# Author(s): Liam Sefton, Alex Bae
# Date: 11/19/2022
# Description: Lexical analyzer capable of tokenizing the contents of a file, based on a set of regular expressions.

import pa3v2

class InvalidExpression(Exception):
	pass

class InvalidToken(Exception):
	""" 
	Raised if while scanning for a token,
	the lexical analyzer cannot identify 
	a valid token, but there are still
	characters remaining in the input file
	"""
	pass

class Lex:
	def __init__(self, reg_ex_file, source_file):
		"""
		Initializes a lexical analyzer.  reg_ex_file
		contains specifications of the types of tokens
		(see problem assignment for format), and source_file
		is the text file that tokens are returned from.
		"""

		regex_file = open(reg_ex_file, 'r')
		self.token_name_dict = {} #maps indices to token names
		self.dfa_list = [] #holds the DFAs for each regex, indices are used for token_name_dict
		counter = 0
		self.alphabet = ""
		for line in regex_file:
			splitter = line.index("\"")
			line = [line[:line.index("\"")].strip("\" \n"), line[splitter:].strip("\" \n")] #all bc the regex can have spaces in it :'^(
			token_name = line[0]
			regex = line[1].strip("\"")
			self.token_name_dict[counter] = token_name 
			counter += 1
			self.dfa_list.append(regex)
			for ch in regex:
				if ch not in ['(', ')', '|', ' ', '*', 'N', 'e'] and ch not in self.alphabet:
					self.alphabet += ch

		for i in range(len(self.dfa_list)):
			self.dfa_list[i] = pa3v2.RegEx(self.alphabet, self.dfa_list[i]) #converts regex to DFA

		
		self.source_file = open(source_file, 'r') #file used for next_token

	def next_token(self):
		"""
		Returns the next token from the source_file.
		The token is returned as a tuple with 2 item:
		the first item is the name of the token type (a string),
		and the second item is the specific value of the token (also
		as a string).
		Raises EOFError exception if there are not more tokens in the
		file.
		Raises InvalidToken exception if a valid token cannot be identified,
		but there are characters remaining in the source file.
		"""
		curr_string = ""

		first_char_found = False #Used for getting the start position of a string in file

		start_pos = self.source_file.tell()
		curr_char = self.source_file.read(1)
		while curr_char not in [" ", "\n", ""] or len(curr_string) == 0: #builds first string up until space or end of file
			if curr_char not in [" ", "\n", ""]:
				if not first_char_found:
					start_pos = self.source_file.tell() - 1
				first_char_found = True
				curr_string += curr_char
			else:
				if curr_char == "":
					break
			curr_char = self.source_file.read(1)

			
		for ch in curr_string: #checks for invalid characters
			if ch not in self.alphabet:
				raise InvalidToken


		if curr_char == "" and len(curr_string) == 0:
			raise EOFError

		successful_dfas = []
		temp_string = curr_string
		for i in range(len(curr_string)): #stripping string 1 character at a time and breaking loop on the first successful set of simulations
			for j in range(len(self.dfa_list)):
				result = self.dfa_list[j].simulate(temp_string)
				if result:
					successful_dfas.append(j)
			if len(successful_dfas) > 0:
				break
			temp_string = curr_string[:-(i+1)]


		if len(temp_string) < len(curr_string): #if the curr_string is equal to temp_string, no need to seek at all
			self.source_file.seek(start_pos) #seeks to start of recent string
			for i in range(len(temp_string)): #reads past the part that was tokenized
				self.source_file.read(1)

		if len(successful_dfas) == 0: 
			raise InvalidToken

		chosen_dfa = min(successful_dfas) #choose first index, as it was first read in

		return (self.token_name_dict[chosen_dfa], temp_string)