# IoT Data Strategy: Centralized vs. Independent Branching

This document compares two methods for routing sensor data into multiple MySQL tables, helping to visualize the architectural differences for future scaling.

---

## 🚀 Comparison Graph (Visualizing the Difference)

### Method A: Centralized Dispatcher (The "Router" Approach)
*Logic is concentrated in one node with multiple outputs.*

```mermaid
graph LR
    A[Source: Sensor Data] --> B{Central Dispatcher}
    B -- "Output 1" --> C[(MySQL: Table_01)]
    B -- "Output 2" --> D[(MySQL: Table_02)]
    
    subgraph "Single Point of Logic"
    B
    end
    
    style B fill:#69f,stroke:#333,stroke-width:2px
```
### Method B: Independent Processors (The "Parallel" Approach)
Logic is split into separate nodes for each destination.
```mermaid
graph LR
    A[Source: Sensor Data] --> B[Function Node 01]
    A --> C[Function Node 02]
    B --> D[(MySQL: Table_01)]
    C --> E[(MySQL: Table_02)]
    
    subgraph "Decoupled Logic"
    B
    C
    end
    
    style B fill:#f96,stroke:#333
    style C fill:#f96,stroke:#333
```
💡 Architectural Memory Hook
Method A is like a Post Office: One sorting center dispatches mail to different cities.

Method B is like Individual Couriers: Each courier takes one letter to one specific city independently.
