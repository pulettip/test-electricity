# test-electricity

Setup
-----

Assuming fish is the default shell.

Install [virtualfish](https://github.com/adambrenecki/virtualfish)

vf new backend
pip install -r requirements.txt

Or you can use any other environment.

Comments:

For a shortage of time, I could not perform all the desirable content. This is a short summary of what the app has and what is missing:

1) BackEnd: There are three models for buldings, meters and readings. All of them have a POST method to create objects from a CSV file as the ones defined in the excercise. Also they have a GET endpoint for retrieving data with some special query options. I didn't have time to prepare the proper tests.

2) FrontEnd: A simple interface to list the buildings, with a search field. In the list you can see the name and also the amount of meters for each building. When you press in one of those, a modal is opened and then you can select the meter you want to visualize. Again for a shortage of time there is no function to upload files.

It can be tested here, although since is a TEST-APP it has only few meters readings lines. Only the first meters have information available:
https://test-electricity-by-pablo.herokuapp.com/

```
