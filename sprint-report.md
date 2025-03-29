# Sprint x Report (1/12/25 - 2/28/2025)
## What's New (User Facing)
* Fixed login view bug where it would direct the user to a page that doesn't exist
* User can login
* Admin can create/delete accounts
* Accounts can add inventory items
## Work Summary (Developer Facing)
This sprint we completed the Solution approach document as well as setting up a lot of code in the backend. This was fairly straightforward but gives us a good base to 
build off of and complete more of the app as well as the frontend. This sprint was a lot of skeletal code and account management related code.
## Unfinished Work
We need to develop a comprehensive system that includes a login page with user authentication to grant access to different pages based on user roles. The system will also feature an inventory management module where users can monitor product inflow and outflow. This will include an inventory display page that provides real-time updates on stock levels, as well as an account management section to oversee user credentials and access permissions. Additionally, the system will generate reports using visual representations like pie charts and bar charts to analyze inventory trends and performance. An inventory login page will also be implemented to ensure secure access to stock-related information.
## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:
* [Login view bug URL](https://github.com/tbergdahl/InventoryManagement/issues/1)
* [Admin account creation and deletion URL](https://github.com/tbergdahl/InventoryManagement/issues/3)
* [Admin account creation usertype URL](https://github.com/tbergdahl/InventoryManagement/issues/5)
* [Admin can create inventory items URL](https://github.com/tbergdahl/InventoryManagement/issues/7)
* [Added requirements.txt file URL](https://github.com/tbergdahl/InventoryManagement/issues/9)
* [Implement Navigation to Report Page From Inventory Screen](https://github.com/tbergdahl/InventoryManagement/issues/27)
* [Implement UI for admin report creation](https://github.com/tbergdahl/InventoryManagement/issues?q=is%3Aissue%20state%3Aclosed)
* [Implement the report generation based off UI feedback](https://github.com/tbergdahl/InventoryManagement/issues/32)

## Incomplete Issues/User Stories
There are currently no issues that are incomplete yet as the app is in its very early stages.
## Code Files for Review
Please review the following code files, which were actively developed during this
sprint, for quality:
* [user_management views.py](https://github.com/tbergdahl/InventoryManagement/blob/main/apps/user_management/views.py)
* [user_management models.py](https://github.com/tbergdahl/InventoryManagement/blob/main/apps/user_management/models.py)
* [user_management admin.py](https://github.com/tbergdahl/InventoryManagement/blob/main/apps/user_management/admin.py)
* [report_generation](https://github.com/tbergdahl/InventoryManagement/blob/main/apps/report_generation/views.py)
* [report_generation/templates](https://github.com/tbergdahl/InventoryManagement/tree/main/apps/report_generation/templates)
## Retrospective Summary
#### Here's what went well:
* Backend setup
* Account creation/deletion
* Bug fixes were fairly straightforward
* Backend setup allowed for easy filtering for reports
#### Here's what we'd like to improve:
* Better UI
* Having more pages implemented
* More report types
#### Here are changes we plan to implement in the next sprint:
* Add styling to the user interface
* Build out more of the pages of the app
* Testing
## Demo Video
[CptS 582 Sprint 1 Video](https://youtu.be/FLbpDkTvuso)


