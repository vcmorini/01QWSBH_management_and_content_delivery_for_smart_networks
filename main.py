import simpy
import numpy
import random
from runstats import Statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 1
NUM_SERVERS = 1
SIM_TIME = 1
total_users= 765367947 + 451347554 + 244090854 + 141206801 + 115845120
nations = {"china": round(765367947/total_users, 2), "usa": round(451347554/total_users, 2), "india": round(244090854/total_users, 2),
           "brazil": round(141206801/total_users, 2), "japan": round(115845120/total_users, 2)}
arrival_rate_global = 100
nation_stats = {"china": 0, "usa": 0, "india": 0, "brazil": 0, "japan": 0}

def arrival(environment, nation, arrival_rate):
    global client_id
    client_id = 1
    # keep track of client number client id
    # arrival will continue forever
    while True:
        nation_stats[nation] += 1

        inter_arrival = random.expovariate(lambd=arrival_rate)

        # yield an event to the simulator
        yield environment.timeout(inter_arrival)

        # a new client arrived
        client_id += 1
        Client(environment, nation, client_id)


class Client(object):

    def __init__(self, environment, i="nations", client_id=0):
        self.env = environment
        self.nation = i
        self.client_id = client_id
        self.response_time = 0
        self.k = random.randint(1, 4)
        # the client is a "process"
        env.process(self.run())

    def run(self):
        # store the absolute arrival time
        time_arrival = self.env.now
        print("client", self.client_id, "from ", self.nation, "has arrived at", time_arrival)
        print("client tot request: ", self.k)

        for j in range(1, self.k+1):
            print("client request number : ", j)
            # The client goes to the first server to be served ,now is changed
            # until env.process is complete
            yield env.process(env.servers.serve())

        self.response_time = self.env.now - time_arrival
        print("client", self.client_id, "from ", self.nation, "response time ", self.response_time)
        stats.push(self.response_time)


class Servers(object):
    # constructor
    def __init__(self, environment, num_servers, service_rate):
        global maximum_number_of_concurrent_requests
        maximum_number_of_concurrent_requests = 10
        self.env = environment
        self.service_rate = service_rate
        self.servers = simpy.Resource(env, capacity=num_servers)  # https://simpy.readthedocs.io/en/latest/simpy_intro/shared_resources.html

    def serve(self):
        # request a server
        with self.servers.request() as request:  # create obj then destroy
            yield request
            global maximum_number_of_concurrent_requests
            maximum_number_of_concurrent_requests -= 1

            # server is free, wait until service is finished
            service_time = random.expovariate(lambd=self.service_rate)

            # yield an event to the simulator
            yield self.env.timeout(service_time)
            maximum_number_of_concurrent_requests += 1
            print(maximum_number_of_concurrent_requests)


if __name__ == '__main__':
    random.seed(RANDOM_SEED)  # same sequence each time

    mu = 20.0  # 2 customer on average per unit time (service time)
    response_time = []

    # create lambda clients
    #for i in range(1, lambd):
    env = simpy.Environment()
    stats = Statistics()

    # servers
    env.servers = Servers(environment=env, num_servers=NUM_SERVERS, service_rate=mu)

    # start the arrival process
    env.process(arrival(environment=env, nation ="china", arrival_rate=arrival_rate_global*nations["china"]))  # technically, a process actually is an event. Example: process of parking a car. https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html?highlight=process
    env.process(arrival(environment=env, nation ="usa", arrival_rate=arrival_rate_global*nations["usa"]))  # technically, a process actually is an event. Example: process of parking a car. https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html?highlight=process
    env.process(arrival(environment=env, nation ="india", arrival_rate=arrival_rate_global*nations["india"]))  # technically, a process actually is an event. Example: process of parking a car. https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html?highlight=process
    env.process(arrival(environment=env, nation ="brazil", arrival_rate=arrival_rate_global*nations["brazil"]))  # technically, a process actually is an event. Example: process of parking a car. https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html?highlight=process
    env.process(arrival(environment=env, nation ="japan", arrival_rate=arrival_rate_global*nations["japan"]))  # technically, a process actually is an event. Example: process of parking a car. https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html?highlight=process

    # simulate until SIM_TIME
    env.run(until=SIM_TIME)  # the run process starts waiting for it to finish
    response_time.append(stats.mean())
    print(nation_stats)
# totally occupied servers in this case
# we need parallel servers for example 5 servers for 5 continents