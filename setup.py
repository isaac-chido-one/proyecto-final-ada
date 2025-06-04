from setuptools import setup

setup(
    name='Catálogo de vacantes de empleo',
    version='1.0',
    description='Proyecto Final Análisis y Diseño de Algoritmos.',
    author='Perla Noemí Dueñas Martínez, Herón Ortiz De Anda, Salomón Isaac Rojas Montoya',
    author_email='perladuenas4@gmail.com, heron10z@gmail.com, isaac.chido.one@gmail.com',
    scripts=['app.py'],
    install_requires=[
        'distro>1.9.0',
        'jeepney>0.9.0',
        'loguru>0.6.0',
        'lxml>5.4.0',
        'notify_py>0.3.43',
        'packaging>25.0',
        'scikit-build>0.18.1',
        'tkfontawesome>0.3.2',
        'tksvg>0.7.4',
        'tomli>2.2.1',
    ]
)
