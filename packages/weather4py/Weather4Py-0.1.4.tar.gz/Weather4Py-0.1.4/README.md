# Weather4Py
a weather library for python to get the weather of a location or set of coordinates, with the ability to save to a json. By default it's C, and it can be changed to F temperature measuring system.

[Github repository for Weather4Py](https://github.com/MintTeaNeko/Weather4Py)

# Here's some examples to how to use the library.
```py
from WeatherPy import WeatherMan

# takes an input of metric(C)/imperial(F)
WeatherMan("owo").set_measurement("metric")

# to get the region of a location
print(WeatherMan("38.8,37.7").region)
# result: Kuluncak/Malatya, Turkey

# to get the weather of a location
print(WeatherMan("israel").weather)
# result: Sunny

# to get the temperature of a location
print(WeatherMan("texas").temperature)
# result: 30

# to get the humidity of a location
print(WeatherMan("newyork").humidity)
# result: 64%

# to reobtain infromation about a location.
WeatherMan("owo").obtain_information()

# to save the results to a folder in json format
WeatherMan("38.8,37.7").save_to_file("output.json")
```