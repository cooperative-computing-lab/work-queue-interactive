import ipywidgets as widgets
import time
import bqplot
from bqplot import pyplot as plt

class Display():
    min_workers = 1
    max_workers = 4
    starting_task = 2
    ending_task = 100
    # instantiate the output widgets as None so that they are properly reset between runs
    tasks_done_bar = None
    tasks_idling = None
    workers_connected = None
    status_message = None
    worker_time = None
    tasks_per_second = None

    # holds output for the primality of the numbers
    task_output_storage = []
    
    starting_time = time.perf_counter() # track time since tasks were submitted: used in output display
   
    # variable to hold the pie chart
    pie = None   
        
    def create_output_widgets(self):
        # create the output widgets
        self.tasks_done_bar = widgets.IntProgress(
            value=0,
            min=0,
            max=self.ending_task-self.starting_task,
            description='Percent of tasks complete:',
            style = {'description_width': 'initial'},
            orientation='horizontal'
        )
        self.tasks_idling = widgets.IntProgress(
            value=0,
            min=0,
            max=self.max_workers,
            description='Percent of workers idle',
            style = {'description_width': 'initial'},
            orientation='horizontal'
        )
        self.workers_connected = widgets.IntProgress(
            value=0,
            min=0,
            max=self.max_workers,
            description='Percent of max workers connected',
            style = {'description_width': 'initial'},
            orientation='horizontal'
        )
        self.status_message = widgets.Text(
            value='Initializing workers',
            description='Workqueue Status',
            disabled=True,
            style = {'description_width': 'initial'},
            orientation='horizontal'
        )
        self.worker_time = widgets.Text(
            description='Time spent by workers (Seconds)',
            disabled=True,
            style = {'description_width': 'initial'},
            orientation='horizontal'
        )
        self.tasks_per_second = widgets.FloatText(
            value=0,
            description='Average tasks complete per second',
            style = {'description_width': 'initial'},
            disabled=True
        )
        self.task_output_storage = [] # clear output from previous runs
        # display output
        display(widgets.HBox([self.status_message, self.tasks_per_second, self.worker_time]))
        display(widgets.HBox([self.tasks_done_bar, self.workers_connected, self.tasks_idling]))
        # initialize real time task display output
        for i in range(self.starting_task, self.ending_task + self.max_workers + 10):
            self.task_output_storage.append(widgets.ToggleButton(
                value=False,
                description=str(i - 2),
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                layout=widgets.Layout(width='20%', height='20px')
            ))
        horizontal_boxes = 15
        vertical_boxes = (self.ending_task - self.starting_task) // horizontal_boxes + 1
        vertical_temp = []
        # actually place the real time display output on screen
        for j in range(vertical_boxes):
            horizontal_temp = []
            for i in range(horizontal_boxes):
                if (i + j * horizontal_boxes + 2) > (self.ending_task):
                    break
                horizontal_temp.append(self.task_output_storage[i + j * horizontal_boxes + 2])
            vertical_temp.append(widgets.HBox(horizontal_temp))
        display(widgets.VBox(vertical_temp))
        
        self.starting_time = time.perf_counter() # reset starting time
        
        # below are just properties of the worker time pie chart
        fig = plt.figure(title="Work Queue Time Distribution (Milliseconds)")
        self.pie = plt.pie(sizes = [0, 0, 0],
                  labels =['Work Queue internal', 'Waiting for workers', 'Application'],
                  display_values = True,
                  values_format=".1f",
                  display_labels='outside')
        self.pie.stroke="black"
        self.pie.colors = ["tomato","lawngreen", "gray"]

        self.pie.radius = 150
        self.pie.inner_radius = 60

        self.pie.label_color = 'orangered'
        self.pie.font_size = '20px'
        self.pie.font_weight = 'bold'
        plt.show()

        
    def update_output_widgets(self, q, t):
        self.status_message.value = "Updating output"
        if t.output == 1: # if x is a prime number then update it accordingly
            self.task_output_storage[int(t.id) + 1].disabled = True
        self.task_output_storage[int(t.id) + 1].button_style = 'success'
        for i in range(q.stats.workers_connected + 1): # update the display of which tasks are currently being worked on
            if (int(t.id) + 1 - i) > 0:
                if (self.task_output_storage[int(t.id) + 1 - i].button_style == ''):
                        self.task_output_storage[int(t.id) + 1 - i].button_style='warning'
        # the below lines just update the output widgets
        self.tasks_done_bar.value = q.stats.tasks_done
        self.workers_connected.value = q.stats.workers_connected
        self.tasks_idling.value = q.stats.workers_idle - 1
        self.tasks_per_second.value = self.tasks_done_bar.value / (time.perf_counter() - self.starting_time)
        self.status_message.value = "Waiting for workers"
        self.worker_time.value = str(q.stats.time_workers_execute / 1000000)
        self.pie.sizes = [q.stats.time_internal / 1000, q.stats.time_polling / 1000, q.stats.time_application / 1000]
        if q.stats.tasks_done >= (self.ending_task-self.starting_task) - 1:
            self.status_message.value = "All tasks complete!"
        elif q.stats.tasks_done == 0:
            self.status_message.value = "Initializing workers"

        

                

    