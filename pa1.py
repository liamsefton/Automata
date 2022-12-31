# Name: pa1.py
# Author(s): Liam Sefton, Alex Bae
# Date: 09/23/2022
# Description: Program to read in DFAs and evaluate strings on the given DFAs.
import sys

class DFA:
	""" Simulates a DFA """

	def __init__(self, alphabet, start_state, accept_states, transitions): #(self, alphabet, start_state, accept_states, transitions)
		"""
		Initializes DFA from the file whose name is
		filename
		"""
		self.alphabet = alphabet #2nd line of txt file, symbols in alphabet
		self.transitions = transitions #empty dictionary for transitions

		self.start_state = start_state #initial state is start state, 2nd to last line
		self.accept_states = accept_states  #last line contains accept states

	def simulate(self, str):
		""" 
		Simulates the DFA on input str.  Returns
		True if str is in the language of the DFA,
		and False if not.
		"""
		curr_state = self.start_state
		for ch in str:
			curr_state = self.transitions[curr_state][ch]   #update transitions, current state and ch as key
			                                                #output state as values
		return curr_state in self.accept_states 