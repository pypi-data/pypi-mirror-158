to install run the command
```
    pip install django-requesting-os-analyzer
```
add to your installed apps
```
    INSTALLED_APPS = [
        ...,
        'django_requesting_os_analyzer.apps.DjangoRequestingOsAnalyzerConfig',
    ]
```
add middleware
```
    MIDDLEWARE = [
        ...,
        'django_requesting_os_analyzer.middleware.CounterMiddleware',
    ]
```
and then to allow the graph to show up you have to tweak your templates settings,
make sure 'APP_DIRS' is set to True.
```
TEMPLATES = [
    {
        ...,
        'DIRS': ['templates'],
        'APP_DIRS': True,
    },
]
```
you can also change the color of the graph's bar and their border by defing following
```
REQUEST_ANALYZER_BG_COLOR = (255,255,255,0.2)
REQUEST_ANALYZER_CHART_COLOR = (255,0,0,0.2)
```