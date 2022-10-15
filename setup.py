from setuptools import setup

setup(
    name='BubbleShoota',
    version='0.1.0',    
    description='A game of Bubble Shoota',
    url='https://github.com/Atheriz-46/TheGame',
    author='Aditya Mohan Mishra, Harsh Wardhan, Pushpit Srivastava',
    author_email='{me1180582,ee3180610,bb1180031}@iitd.ac.in',
    license='MIT-License',
    packages=['src'],
    install_requires=['tk'
                      'pillow',                    
                      ],

    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
