# CozyBlanket Network Features 

CozyBlanket remote network features allow controlling CozyBlanket from desktop DCCs, servers and pipeline tools for integration with existing software. This package provides a python implementation of the API.

**Make sure you have Network Features enabled in CozyBlanket. Network Features are only available as part of Retopology Pack.**

The `CozyBlanketConnection` class can be used to connect to a running instance of CozyBlanket. You can find all the available commands in the class definition, but here is a quick example of what can be done:

```
from cozyblanket import CozyBlanketConnection

# Connect to a running instance
CB = CozyBlanketConnection() # This can take an optional device_id argument if you want to connect to a specific device
CB.connect()

...

# Close the current document and clear the current scene, otherwise the current document will be overwirtten
CB.document_close()
CB.scene_clear()

...

# Push a new retopology target from an OBJ file
CB.target_push_obj("target.obj", "named_target")
CB.target_load("named_target")

...

# Save the currently open retopology mesh to an OBJ file
CB.editmesh_pull_obj("editmesh.obj")

...

# Add a remote action button to the device's UI
CB.remote_actions_add("Example Button", lambda: print("The user pressed the button!"))

# remote_actions_process() needs to be called periodically from your client app
while True:
    CB.remote_actions_process()

...

# Close any running connections
CB.diconnect()
```
