### Starting Development

0. git clone the repo (the master branch is the stable production code,
   the magic happens in the develop branch)
1. create your virtualenv and activate it
2. run scripts/bootstrap.sh
3. install phantomjs (see instructions on docs/phantomjs_instructions.txt)
4. if you wan the gnome notifier for python tests run
   scripts/nose_notification.sh

5. run the tests and verify that everything works: fab tests


### Dependencies, stack and aditional info:

- our serve-side code uses python and flask.

- our front-end code uses coffeescript + backbone + jquery + requirejs

- we test js code with qunit. You can run the test from the browser or
  from phantomjs. The tests page is served from the server itself (to better
  reflect the real runtime conditions) on the /tests/ route. To run the
  phantomjs code you must have it installed.

- we test python code with unittests + nose.

- we use some watchers in the development process to speed up the code/test
  cycles. For python we use nosy + nose-notify-send
  (for integration with gnome notification). For js we use phantomjs + a
  qunit runner + phantomjs-notify (also for gnome notification). If dont use
  ubuntu or dont want the notification you can easily disable them.

- for styling we use zurb foundation + SCSS (sass).

- we manage development and deploy tasks via Fabric

- for forms we use the reForm.js framework, which is a submodule inside this
  project so after you clone the repo you must init and update the submodules.

- we use mongodb for persistent data store and redis for transient
  storage (session, task-queue, etc)

