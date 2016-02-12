from abc import ABCMeta, abstractmethod

class Strategy(object):

	__metaclass__ = ABCMeta


	@abstractmethod
	def generate_signals(self):
		raise NotInplementedError("Should implement generate_signals()!")


class Portfolio(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def generate_positions(self):
		raise NotInplementedError("Should implement generate_positions()!")

	@abstractmethod
	def backtest_portfolio(self):
		raise NotInplementedError("Should implement backtest_portfolio()!")
		