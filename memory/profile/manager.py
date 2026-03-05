import json
import os

class ProfileManager:
    def __init__(self, path="~/.recall_profile.json"):
        self.path = os.path.expanduser(path)
        if not os.path.exists(self.path):
            self._data = {'watchlist': [], 'portfolio': []}
            self._save()
        else:
            self._data = self._load()

    def _load(self):
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                if 'watchlist' not in data: data['watchlist'] = []
                if 'portfolio' not in data: data['portfolio'] = []
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {'watchlist': [], 'portfolio': []}

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def get_watchlist(self):
        return self._data.get('watchlist', [])

    def add_to_watchlist(self, ticker):
        if ticker not in self._data['watchlist']:
            self._data['watchlist'].append(ticker)
            self._save()

    def remove_from_watchlist(self, ticker):
        if ticker in self._data['watchlist']:
            self._data['watchlist'].remove(ticker)
            self._save()

    def get_portfolio(self):
        return self._data.get('portfolio', [])

    def add_position(self, symbol, quantity, price):
        """Adds a position or updates an existing one (weighted average)."""
        portfolio = self._data.get('portfolio', [])
        found = False
        for p in portfolio:
            if p['symbol'] == symbol:
                old_qty = p['quantity']
                old_cost = old_qty * p['avg_price']
                new_cost = quantity * price
                total_qty = old_qty + quantity

                p['quantity'] = total_qty
                p['avg_price'] = (old_cost + new_cost) / total_qty if total_qty > 0 else 0.0
                found = True
                break

        if not found:
            portfolio.append({'symbol': symbol, 'quantity': quantity, 'avg_price': price})

        self._data['portfolio'] = portfolio
        self._save()

    def remove_position(self, symbol):
        portfolio = self._data.get('portfolio', [])
        self._data['portfolio'] = [p for p in portfolio if p['symbol'] != symbol]
        self._save()
