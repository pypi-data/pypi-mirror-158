=============
user_feedback
=============

SALTISE-user-feedback is a simple Django app to collect and store user feedback.

Quick start
-----------

1. Add the UserFeedback app to your requirements, then pip install::

    pip install SALTISE-user-feedback

1. Add "user_feedback" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'user_feedback',
        ...
    ]

2. Include the user_feedback URLconf in your project urls.py like this::

    url("feedback/", include("user_feedback.urls")),

3. Migrate::

    python manage.py migrate

4. Setup an `EMAIL_BACKEND` in your project's settings.py.

5. Add admin emails to `ADMINS`'s list of tuples in your project's settings.py::

    ADMINS = [('John', 'john@example.com'), ('Mary', 'mary@example.com')]

6. If '/accounts/login/' is not active, make sure to have a `LOGIN_URL` in your settings.py.

7. Import user_feedback's minified script and styles in your base template(s).  Note that the styles are nested within container id::

    <script src="{% static 'user_feedback/js/app.min.js' %}" defer="true"></script>
    <link rel="stylesheet" href="{% static 'user_feedback/css/styles.min.css' %}" />

8. Place the following element in templates where you would like for users to offer feedback::

    <div id="user-feedback-app"></div>

9. If not in the template already, add a csrf token::

    {% csrf_token %}

10. Inject the app into the DOM, customizing props as needed:

    .. code-block:: javascript

        <script>
          window.addEventListener("load", function () {
            const feedback = () => {
              return user_feedback.h(user_feedback.App, {
                acceptText: "{% trans 'Send' %}",
                cancelText: "{% trans 'Cancel' %}",
                charCountText: "{% trans 'characters remaining' %}",
                description: "{% trans 'Leave feedback or get help' %}",
                feedbackTypes: [
                  { value: 1, text: "Bug report" },
                  { value: 2, text: "Feature request" },
                  { value: 3, text: "General feedback" }
                ],
                menuFeedbackText: "{% trans 'Give Feedback' %}",
                menuHelpText: "{% trans 'Tutorials and Forums' %}",
                menuHelpUrl: "#",
                placeholder: "{% trans 'Let us know what is on your mind...' %}",
                snackbarError:
                  "{% trans 'An error occurred.  Please try again later.' %}",
                snackbarSuccess: "{% trans 'Thanks for your feedback!' %}",
                text: "",
                title: "{% trans 'How can we improve your experience?' %}",
                url: "{% url 'user_feedback:post' %}"
              });
            };
            user_feedback.render(feedback(), document.getElementById("user-feedback-app"));
          });
        </script>

Quick start dev
---------------

1. Install node modules::

    npm install

2. Install dev-requirements::

    pip install -r requirements/dev-requirements.txt

3. Install pre-commit::

    pre-commit install

4. Create a superuser and login::

    python user_feedback.py createsuperuser

5. Start the server::

    python user_feedback.py runserver

6. Navigate to '(root)/test/button/', to see the user_feedback button in action.

7. Build when you make edits to app.js or styles.scss::

    npx gulp scripts
    npx gulp styles

8. If you wish, remake the package::

    tox --recreate

9. To publish, e.g.::

    twine upload .tox/dist/SALTISE_user_feedback-1.0.zip --verbose


Notes
-----

mcw v0.41.1 textfield needs to be manually patched to correct missing units in calc
