Dart `List`s have a `first` and a `last` getter and setter, so you can easily
do stuff like this:

```dart
var theList = ['banana'];
theList.first = 'apple';
print(theList.last);
```

## But why stop there?

Wouldn't it be cool to also be able to call `theList.second` or `theList.thirdLast`?

Or even `theList.eigth`?

Wonder no more! By harnessing the power of extension methods, this package offers getters and setters for the first and last twenty items of a list!
