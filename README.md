# Service Interval
An application for tracking maintenance interval of your car.
![ServiceInterval application screenshot](http://178.213.227.72:8080/share.cgi/pyServiceInterval.png?ssid=0zwPy6Y&fid=0zwPy6Y&open=normal&ep=)
You need to customize default service operations list and entry data about all
previous service operations with your car. After that this application can 
advice when does your car needs in the next preventive maintenance.

I hope it will be helpful for you. So I followed the idea of application 
that was:

* Lightweight: no site-packages and no installation needed
* Provides easy way to keep and manage data
* Allow reliable data import/export
* Opensource: it released under GPL v3.0 license
* Crossplatform

With best regards,
Don Dmitriy Sergeevich.

Send your feedback to dondmitriys@gmail.com
## Installation
No installation needed. Just run \<servint.pyw\> file.
You only need Python 3.X.

But in Ubuntu you may obtain an error:
\>\>\> ImportError: No module named '_tkinter', please install the python3-tk package
So the solution is matter of course:
$ sudo apt-get install python3-tk
## Usage
* At first time you need to enter some information. For the beginning push button
\<Edit vehicle properties\> on toolbar or Edit menu and enter vehicle label, 
production date and haul (mileage) in kilometers.
* Than add operations that must be complete periodically. Use \<Add new operation\> 
button on toolbar or menu Edit \> New operation.
Than fill operation label and period fields and press \<Ok\>. This way add all 
periodical operations that you need. Operations will be stored at tab 
\<Periodic operations catalogue.\>
* Than add entries for complete service operations history by selecting operation
name from drop-down list and filling operation-done information. Operations will
be stored at tab \<Operations history.\>

In general you can add, edit or remove operations in any order. 
When all data have been introduced you can go to the tab \<Maintenance plan\> 
and check when does your car needs in the next preventive maintenance.
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
* **v1.0 (2015-12-20)**
    * First release. Basical functionality realised.

## Credits
* ToolTip widget for Tkinter by Tucker Beck
http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
* Free icons from [iconfinder](http://iconfinder.com)

## License
GPL v3.0 License. See the LICENSE file.