Store/Retrieve an item
    POST: Create a new item
        - Base type
        - Data
    PUT: Update an item
Store/retrieve list of items
    - body json for filter criteria
Linking items
Create a context

- items
    - performs CRUD operations on items
    - creates relationships
    - queries based on relationships
- activities
- scheduler
    - triggers actions based on time-events



===
- Start with an unstructured object, e.g. text snippet:
    > Type: (text?)
    > Container: text/plain or other mime type
- Infer one or more structured types
    e.g. contact / person, to-do item, country
- ???


Activities
==========
- Used as a container for items related to a specific user-task
- Often generates one or more items that represent the 'output'


Examples:

- Plan a trip to tokyo:
    - Output: Itinerary
    Notes:
        - Lifespan: ~1 week
        - Contains several discrete sub-tasks (book flight, hotel, activities)
     
- Buy groceries
    - Output: receipt 
    - Notes
        - Lifespan: <1 day
        - Repeated task. Same activity may be useful to re-use 

- Write novel
    - Output: book
    - Notes:
        - Lifespan: ongoing/indefinite.

- Check e-mail:
    - Output: activit(ies)
    - Notes:
        - Meta-activity. More of a passive event-stream. see: news feed, web
              surfing, etc

- Learn Chinese
    - Output: ??
    - Notes:
        - Lifespan: on-going/indefinite


Implementation workflow
=======================

# Create a new activity
- POST /activities
    ! [ n3 ] _, contains, item
    ? n3 _, has-description, description
    ? [ n3 ] _, related-to, activity
    < activity-id


# Get activities
- GET /activities
    ? <filter criteria: active, time range, etc>

# Get all items in activity
- GET /activities/<uuid>
    ? <filter criteria>

# Modify an activity, archive an item
???
DELETE /activities/<uuid>/<item-uuid>

