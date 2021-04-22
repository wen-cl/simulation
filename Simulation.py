# Generate 100 sample event
# 1. timestamp(t - random number(1 to 20)) 2.user_id 3.calling floor 4.direction
import random
import uuid

class Event(object):
    def __init__(self, time, client_id, floor_number, direction=True):
        self.time = time
        self.client_id = client_id
        self.floor_number = floor_number
        self.direction = direction
    
    def Generate_Desired_Floor(self, current_floor):
        self.floor_number = random.choice([i for i in range(1,20) if i not in [current_floor]])
        return self.floor_number

class Elevator(object):
    def __init__(self, id, current_floor, direction, busy, occupied):
        self.id = id
        self.current_floor = current_floor
        self.direction = direction
        self.busy = busy
        self.occupied = occupied
        self.event = None
        self.floor_2_floor_interval = 2.1
        self.travel_end_time = 0
    
    def Move(self, file, current_time, elevator_event_list):
        travelling_time = abs(self.event.floor_number - self.current_floor) * self.floor_2_floor_interval
        self.travel_end_time = current_time + travelling_time
        file.writelines("starting to move, elevator's travelling end time " + str(self.travel_end_time) + "\n")
        if ((self.event.floor_number - self.current_floor) > 0):
            self.direction = True
        elif ((self.event.floor_number - self.current_floor) < 0):
            self.direction = False
        if (self.occupied == True):
            status = "occupied"
        elif (self.occupied == False):
            status = "empty"
        eventline = " t = " + str(current_time) + ", elevator " + str(self.id) + ", current floor=" + str(self.current_floor) + ", end floor=" + str(self.event.floor_number) + ", " + status
        elevator_event_list.append(eventline)

def Generate_Static_Events(static_list=[]):
    t = 0
    number_of_calls = int(input("enter the number of event to generate : "))
    while(number_of_calls > 0):
        t = t + random.randint(1,10)
        #generate floor number
        floor_number = random.randint(1,20)
        #generate direction
        if (floor_number == 1):
            direction = True
        elif (floor_number == 20):
            direction = False
        else:
            random_bit = random.getrandbits(1)
            direction = bool(random_bit)
        #client id
        client_id = uuid.uuid1()
        static_list.append(Event(t, client_id, floor_number, direction))
        number_of_calls = number_of_calls - 1

# generate static event list
def Log_Event_List(static_list=[]):
    f2 = open("static-event-list.txt", "w")
    line =  "t"+ "          " + "Clent Id" + "                           " + "Floor Number" + "              " + "Direction" + "\n"
    f2.write(line)
    for event in static_list:
        if (event.direction == True):
            direction = "Up"
        else :
            direction = "down"
        line = str(event.time) + "      " + str(event.client_id) + "         " + str(event.floor_number) + "                        " + direction + "\n"
        f2.write(line)
    f2.close()

t = 0.0
queue = []
elevators = []
static_event_list = []
elevator_event_list = []
user_event_list = []

elevators.append(Elevator(1, 1, True, False, False))
elevators.append(Elevator(2, 1, True, False, False))

Generate_Static_Events(static_event_list)
Log_Event_List(static_event_list)

f = open("log.txt", "w")
while True:
    line = "At t = " + str(t) + "\n"
    f.writelines(line)
    if (len(static_event_list) > 0):
        next_event = static_event_list[0]
        if (next_event.time == t):
            queue.append(static_event_list.pop(0))
    line = "queue length : " + str(len(queue)) + "\n"
    f.writelines(line)

    #dispatch event to elevator
    if (len(queue) > 0):
        for e in queue:
            if (e.direction == True):
                direction = "Up"
            else :
                direction = "down"
            line = "In queue: event t = " + str(e.time) + ", client id - " + str(e.client_id) + ", client's floor number - " + str(e.floor_number) + ", direction - " + direction + "\n"
            f.writelines(line)

        for elevator in elevators:
            if (elevator.busy == False and len(queue) > 0):
                elevator.event = queue.pop(0)
                elevator.busy = True
                elevator.Move(f, t, elevator_event_list)
    
    for elevator in elevators:
        #check if arrive at destination
        if (elevator.busy == True and elevator.occupied == False):
            if (elevator.travel_end_time <= t):
                elevator.current_floor =  elevator.event.floor_number
                line = "Elevator " + str(elevator.id) + " arrived at floor - ", str(elevator.current_floor) + "\n"
                f.writelines(line)

                user_event = Event(t, 1, elevator.current_floor)
                desired_floor = user_event.Generate_Desired_Floor(elevator.current_floor)
                
                if ((user_event.floor_number - elevator.current_floor) > 0):
                    user_event.direction = True
                    user_direction = "up"
                elif ((user_event.floor_number - elevator.current_floor) < 0):
                    user_event.direction = False
                    user_direction = "down"
                eventline = "t = " + str(t) + ", client id=" + str(elevator.event.client_id) + ", current_floor=" + str(elevator.current_floor) + ", desired floor=" + str(desired_floor) + ", travelling time=" + str(abs(user_event.floor_number - elevator.current_floor)*elevator.floor_2_floor_interval) + ", direction=" + user_direction 
                user_event_list.append(eventline)
                elevator.event = user_event
                elevator.occupied = True
                elevator.Move(f, t, elevator_event_list)

        #check if arrive at user desired destination
        elif (elevator.busy == True and elevator.occupied == True):
            if (elevator.travel_end_time <= t):
                elevator.current_floor =  elevator.event.floor_number
                elevator.occupied = False
                elevator.busy = False
                elevator.event = None
                elevator.travel_end_time = 0
                elevator.direction = None
    
    if ( len(static_event_list) == 0 and len(queue) == 0 and elevators[0].busy == False and elevators[1].busy == False):
        f3 = open("elevator-event.txt", "w")
        for e in elevator_event_list:
            line = e + "\n"
            f3.writelines(line)
        f3.close()
        f4 = open("user-event.txt", "w")
        for e in user_event_list:
            line = e + "\n"
            f4.writelines(line)
        f4.close()
        f.close()
        print("simulation end")
        break
    t = t + 1.0
    