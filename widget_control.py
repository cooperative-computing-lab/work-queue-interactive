import ipywidgets as widgets
import time

class Display():
    num_workers = widgets.IntSlider(
        value=10,
        min=1,
        max=10,
        step=1,
        description='Max number of workers:',
        style = {'description_width': 'initial'},
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )
    tasks_range = widgets.IntRangeSlider(
        value=[2, 100],
        min=2,
        max=1000,
        step=1,
        description='Task Range:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
    )
    
    tasks_done_bar = None
    tasks_idling = None
    workers_connected = None
    status_message = None
    worker_time = None
    tasks_per_second = None

    worker_properties = ["Number of workers", "Cores", "Memory", "Disk", "GPUs"]
    worker_array = []
    task_output_storage = []
    
    starting_time = time.perf_counter() # track time since tasks were submitted: used in output display
    
    def create_user_input_widgets(self):
        display(widgets.HBox([self.tasks_range, self.num_workers])) # displays the input widgets 
        
    def create_output_widgets(self):
        self.tasks_done_bar = widgets.IntProgress(
            value=0,
            min=0,
            max=self.tasks_range.value[1]-self.tasks_range.value[0],
            description='Percent of tasks complete:',
            style = {'description_width': 'initial'},
            orientation='horizontal'
        )
        self.tasks_idling = widgets.IntProgress(
            value=0,
            min=0,
            max=self.num_workers.value,
            description='Percent of workers idle',
            style = {'description_width': 'initial'},
            orientation='horizontal'
        )
        self.workers_connected = widgets.IntProgress(
            value=0,
            min=0,
            max=self.num_workers.value,
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
        self.task_output_storage = []
        for name in self.worker_properties:
            self.worker_array.append(widgets.Text(description=name, disabled=True, style = {'description_width': 'initial'}, layout=widgets.Layout(width='15%', height='40px')))
        display(widgets.HBox([self.status_message, self.tasks_per_second, self.worker_time]))
        display(widgets.HBox([self.tasks_done_bar, self.workers_connected, self.tasks_idling]))
        for i in range(self.tasks_range.value[0], self.tasks_range.value[1] + self.num_workers.value + 10):
            self.task_output_storage.append(widgets.ToggleButton(
                value=False,
                description=str(i - 2),
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                layout=widgets.Layout(width='20%', height='20px')
            ))
        horizontal_boxes = 15
        vertical_boxes = (self.tasks_range.value[1] - self.tasks_range.value[0]) // horizontal_boxes + 1
        vertical_temp = []
        for j in range(vertical_boxes):
            horizontal_temp = []
            for i in range(horizontal_boxes):
                if (i + j * horizontal_boxes + 2) > (self.tasks_range.value[1]-self.tasks_range.value[0]):
                    break
                horizontal_temp.append(self.task_output_storage[i + j * horizontal_boxes + 2])
            vertical_temp.append(widgets.HBox(horizontal_temp))
        display(widgets.VBox(vertical_temp))
        self.starting_time = time.perf_counter()
        
    def update_output_widgets(self, q, t):
        self.status_message.value = "Updating output"
        if t.output == 1: # if x is a prime number then update it accordingly
            self.task_output_storage[int(t.id) + 1].disabled = True
        self.task_output_storage[int(t.id) + 1].button_style = 'success'
        for i in range(q.stats.workers_connected + 1): # update the display of which tasks are currently being worked on
            if (int(t.id) + 1 - i) > 0:
                if (self.task_output_storage[int(t.id) + 1 - i].button_style == ''):
                        self.task_output_storage[int(t.id) + 1 - i].button_style='warning'
        self.tasks_done_bar.value = q.stats.tasks_done
        self.workers_connected.value = q.stats.workers_connected
        self.tasks_idling.value = q.stats.workers_idle
        self.tasks_per_second.value = self.tasks_done_bar.value / (time.perf_counter() - self.starting_time)
        self.status_message.value = "Waiting for workers"
        self.worker_time.value = str(q.stats.time_workers_execute / 1000000)
        if q.stats.tasks_done >= (self.tasks_range.value[1]-self.tasks_range.value[0]) - 1:
            self.status_message.value = "All tasks complete!"
        elif q.stats.tasks_done == 0:
            self.status_message.value = "Initializing workers"

                

    