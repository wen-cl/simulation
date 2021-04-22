Simulation of 2 Elevators in 20 floors Building


1. Run Simulation.py in terminal with python 3.9.x
2. Output Files:
     static-event-list.txt : a list of pre-generated event list for calling the elevator to serve, eg. going up OR going down
        columns 
        t - instant of the occurence 
        client id - identity of event instance 
        Floor Number - floor number that the event 
        Direction - desired direction of the user to go
    
    log.txt : logging for all activites of the simulation program.

    elevator-event.txt : logging for activities of the lifts
        columns
        t - instant of the occurence (at the elevator going to move)
        elevator x - x is the id of elevator
        current_floor - current floor of the elevator
        end_floor - the target floor to travel to, as where the client's call is located
        empty/ occupied - task of the elevator at instance of travelling

    user-event.txt : a list of generated event list for reqeusting the elevator to travel to specific floor.
        columns 
        t - instant of the occurence that client set request  
        client id - identity of event instance
        current floor - floor number currently where the user at
        desired floor - floor number to travel to 
        travelling time - total time requried to travel
        Direction - direction to travel, relative to current floor

3. Simulation Program & Flow
    1. Event class 
        - instance will be generated with occurence instant (t), calling floor and direction to go in random order AS the representation of calling of user 
        - instance will be generated with occurence instant (t), request floor to go in random order AS the representaion of request of user

        function : Generate_Desired_Floor - generate a random floor number to travel to as the request of user
    
    2. Elevator class : a representation of elevator
        - instance of elevator contains own identity, current location/ floor o the elevator, travelling direction, status of the elevator (busy when the elevator is travelling),
            content of the elevator (empty/ occupied), event that the elevator is currently handling, floor to floor interval (cycle time), travel_end_time is the calculated 
            travelling time
        
        function : Move - to calculate the travel end time of the elevator

    3 Flow
        3.1 declaration and implementation of Event's and Elevator's classes
        3.2 declaration

            queue = [] queue list for the call from different levels
            elevators = [] list of elevators
            static_event_list = [] pre-generated call events
            elevator_event_list = [] elevators events to serve calls and requests
            user_event_list = [] user request list (request to move to desired floor)
        
        3.3 Generate a static call event list, then log the list to a text by function (Log_Event_List). The static event list is generated
            based on the a random t in incremental manner. Every t instant correspond to 1 call event only. The randomized function 
            do not generate multiple events at an instant, t.
        
        3.4 While True : the loop will continously run for event loop instance, the t will increase by 1 unit. Eventually, the loop will break when achieve these condition,
                1. there is no call in the queue (call from the floor by user) and for the static event list (len(queue) == 0)
                2. all request events are served elevator 1 and 2 are NOT busy.

        3.5 line 92 to 95 
            push event from pre-generated event list (static event list) to call queue (if t of the event is equal to current t of the while loop)

        3.6 line 100 to 113 (first come first serve order)
            dispatch event to elevators
            - check the elevator is free (NOT busy) 
            - pop the first call in queue list to the elevator in FOREACH loop
            - elevator Move (When the elevator's travelling end time equal to the environment time (while loop) t, another event to generate)

        3.7 line 118 Check if elevator arrive at the calling floor

        3.8 line 119 to line 136 
            on arrival, it will generate another user event. to create a desired floor to go. Elevator will set to occupied (occupied ==  true) to indicate 
            elevator travelling with user.
            Elevator will start to move (elevator will calculate the travelling time, when its travelling end time equal to environment time,
            the service will end and elevator is freed - NOT busy and elevator is set to empty - NOT occupied)

        3.9 line 139 to line 146
            on arrival, the elevator will set free ( NOT busy and NOT occupied ). The elevator is ready for next call. 
        
        



         



 