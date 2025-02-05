# Architecture

```mermaid
---
title: MVVM ?
---
flowchart
    db[(DB)]
    data_layer[Repositories]
    models[Models]
    vms[ViewModels]
    views[Views]
    db  <-- add/get/update --> data_layer
    data_layer <--> models
    models <-- content --> vms
    vms <-- bindings --> views
```

## TODOs

### Player Selector

* need to be able to search for a player who hasn't already played for the team. Or possibly create a player not already in the database at all
* selecting players other than defaults (or unselecting defaults) doesn't affect the team list for the innings
