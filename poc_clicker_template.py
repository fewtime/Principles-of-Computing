"""
Cookie Clicker Simulator
"""

import math
import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
# SIM_TIME = 10000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [ (0.0, None, 0.0, 0.0) ]
        # self._history = [ (self._current_time, self._current_item,
        #                self._cost_item, self._total_cookies) ]

    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self.get_time()) + "\n" \
            + "Current cookies: " + str(self.get_cookies()) + "\n" \
            + "CPS: " + str(self.get_cps()) + "\n" \
            + "Total Cookies: " + str(self._total_cookies) + "\n" \
            + "History: " + str(self.get_history()) + "\n"

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self.get_cookies():
            return 0.0
        else:
            return float( math.ceil( (cookies-self.get_cookies()) / self.get_cps() ) )

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        else:
            self._current_time = self.get_time() + time
            self._current_cookies += self.get_cps() * time
            self._total_cookies += self.get_cps() * time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.get_cookies():
            return
        else:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append( (self.get_time(), item_name,
                                   cost, self._total_cookies) )


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    copy = build_info.clone()
    clicker_state = ClickerState()
    present_time = 0.0

    while True:
        if present_time > duration:
            break
        else:
            item = strategy(clicker_state.get_cookies(),
                            clicker_state.get_cps(),
                            clicker_state.get_history(),
                            duration-present_time, copy)

            if item == None:
                break
            else:
                cookies_needed = copy.get_cost(item)
                item_cps = copy.get_cps(item)
                time_needed = clicker_state.time_until(cookies_needed)
                if (present_time+time_needed) > duration:
                    break
                else:
                    clicker_state.wait(time_needed)
                    present_time += time_needed
                    clicker_state.buy_item(item, cookies_needed, item_cps)
                    copy.update_item(item)
                    
    if present_time < duration:
        clicker_state.wait(duration-present_time)
        present_time += (duration-present_time)

    return clicker_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    total_cookies = cookies + cps*time_left
    min_val = total_cookies
    item_name = None

    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost <= total_cookies:
            if item_cost <= min_val:
                min_val = item_cost
                item_name = item

    return item_name

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    total_cookies = cookies + cps*time_left
    max_val = float('-inf')
    item_name = None

    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost <= total_cookies:
            if item_cost > max_val:
                max_val = item_cost
                item_name = item

    return item_name

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    total_cookies = cookies + cps*time_left
    best_cps_to_cost_ratio = float('-inf')
    item_name = None

    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost <= total_cookies:
            cps_to_cost_ratio = build_info.get_cps(item) / (item_cost*1.0)
            if cps_to_cost_ratio >= best_cps_to_cost_ratio:
                best_cps_to_cost_ratio = cps_to_cost_ratio
                item_name = item

    return item_name

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

run()

