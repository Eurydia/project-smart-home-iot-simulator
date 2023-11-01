# smart-home-iot-simulator

An assignment for Python course at ELTE to emulate a smart home IoT system.

## General architecture

Since this project is a simulation, it is not a real IoT system.

I want to create a robust and extensible system, so I decided to use a layered architecture.

The idea is that we have a scheduler, which is responsible for running the simulation.
It simply runs periodically.

The scheduler stores a collection of events.
Each event has a set of requirements, which must be satisfied in order to run the event.

The scheduler checks the requirements of each event, and if they are satisfied, it runs the event which causes some kind of change in the system.

Optionally, these events are logged to a file or outputted to the console.

Finally, I want to build a user interface on top of this system, which allows the user to interact with the system through a GUI.

### Sensors

A sensor is a device which can measure some kind of data.
In this project, a sensor generates a random value to simulate environmental noise.

### Smart devices (Actuators)

An actuator is a device which can change the state of the system.
In this project, an actuator is a smart device.

### Event (Binder)

An event binds a sensor and an actuator together.
It stores some requirements and a actions to perform.

If the requirements are satisfied, actions of the event are triggered.

Ideally, The readings from the sensor are used to determine the actions of smart devices.

### Scheduler (Runner)

A scheduler is responsible for running the simulation.

It is responsible for periodically checking the requirements of each event, and trigger the associated actions if needed.

## Dependencies

Originally, the primary dependencies were PySimpleGUI for user interface,
but the lack of type annotations have made it impossible to use.
In the end, I decided to migrate to Tkinter, which is a standard library.

So apart from black, coverage, pytest and mypy, which are technically dev dependencies,
there are no dependencies for this project.

But in order to run the tests, you need to install the dev dependencies.

```bash
pip install -r requirements.txt
```

Then, use the following command to run the example program.

```bash
python main.py
```

Run Pytest using Coverage and genrate an HTML report.

```bash
coverage run -m pytest && coverage html
```

Run typechecking using mypy.

```bash
python -m mypy .
```

## References

**Dependcies**:

- Black: https://black.readthedocs.io/en/stable/index.html
- Coverage: https://coverage.readthedocs.io/en/coverage-5.5/
- Mypy: https://mypy.readthedocs.io/en/stable/
- Pytest: https://docs.pytest.org/en/stable/
- PySimpleGUI: https://pysimplegui.readthedocs.io/en/latest/

**Documentation**:

- Tkinter: https://docs.python.org/3/library/tkinter.html
- Tcl manual: https://www.tcl.tk/man/tcl8.5/TkCmd/ttk_scale.html
