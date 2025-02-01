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