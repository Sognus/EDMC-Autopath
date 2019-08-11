import json
import time
from threading import Lock
from threading import Thread
import requests

# Core API link
API = "https://spansh.co.uk/api/"
# Timeout value
TIMEOUT = 30


class NeutronPlotter:

    def __init__(self, globals):
        self.globals = globals
        self.origin = None
        self.destination = None
        self.efficiency = None
        self.range = None
        # Special data handling
        self.route = None
        self.job = None
        # synchronize
        self.lock = Lock()

    def request_calculation(self, origin, destination, efficiency, ship_range):
        self.globals.logger.debug("Neutron plotter -> calculation requested")
        self.origin = origin
        self.destination = destination
        self.efficiency = efficiency
        self.range = ship_range

        # Prepare link for job queue
        link_job = API + "route?from={}&to={}&efficiency={}&range={}".format(origin, destination,efficiency, ship_range)
        self.globals.logger.debug("Neutron -> request target is {}".format(link_job))
        # API calls for job queue
        request = requests.get(link_job).json()
        self.job = request["job"]

        thread = Thread(target=self.wait_for_route)
        thread.start()
        # After timeout we dont care anymore
        thread.join(timeout=TIMEOUT+1)

        # synchronize critical path
        with self.lock:
            return self.route

    def wait_for_route(self,):
        if self.job is None or len(self.job) < 1:
            return
        # Prepare link for route data
        link_data = API + "results/{}".format(self.job)
        # WAIT for data
        data = None
        time_start = time.time()
        data_request = requests.get(link_data)
        while data_request.status_code != 200:
            data_request = requests.get(link_data)
            time_elapsed = time.time() - time_start
            if time_elapsed > TIMEOUT:
                break

        # Get json
        data = data_request.json()
        # Synchronize
        with self.lock:
            self.route = data


