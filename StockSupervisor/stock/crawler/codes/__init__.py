from .codes import StockAgents
from .fetch import update_codes

stock_agents = StockAgents()

tpex = stock_agents.tpex
twse = stock_agents.twse
codes = stock_agents.codes
