
Custom configuration for Linux users
Notice for Linux users regarding permissions
Please read this if you are following this course on a Linux OS. Otherwise, feel free to skip to the next video.



In the next video we will create a new Django project using Docker.

Some Linux users have mentioned that they see the following error in the following video:

Traceback (most recent call last):
  File "/usr/local/bin/django-admin.py", line 5, in <module>
    management.execute_from_command_line()
  File "/usr/local/lib/python3.7/site-packages/django/core/management/__init__.py", line 381, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.7/site-packages/django/core/management/__init__.py", line 375, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/base.py", line 316, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/base.py", line 353, in execute
    output = self.handle(*args, **options)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/commands/startproject.py", line 20, in handle
    super().handle('project', project_name, target, **options)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/templates.py", line 155, in handle
    with open(new_path, 'w', encoding='utf-8') as new_file:
PermissionError: [Errno 13] Permission denied: '/app/manage.py'
If you see this error, this is because of a known issue with Docker on Linux: https://github.com/moby/moby/issues/2259

Unfortunately I have not found a perfect solution, however a good workaround is as follows:

1. Update your docker-compose.yaml file to include user: $UID:$GID in the app service like this: https://gist.github.com/LondonAppDev/93f84cc9b86c0f513a18c70571af208a#file-docker-compose-yml-L5

2. Change the ownership of your app/ directory to your user by running chown -R $(whoami):$(whoami) app/

3. Now run export UID=${UID} && export GID=${GID} in the terminal to set your UID and GID variables (if you don't do this then you'll see a warning saying these values were not set when running docker).

4. Run the command again: docker-compose run app sh -c "django-admin.py startproject app .".

You should see that is works and the project is created with the correct permissions.

The drawback / issue with this solution is that step 3 needs to be ran every time you load a new terminal window. There are a few workarounds to this.

One is adding the export lines to your .bash_profile file so they are ran automatically each time you start a new terminal.

If you have any issues with the above workaround, please message me in the Q&A and include a link to your full source code on GitHub.