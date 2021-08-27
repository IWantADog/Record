# about unittest

## Basic

- Testcase
- setup & setUpClass
- teardown & tearDownClass

## unittest.mock

### commom usage

- Mock:
- MagicMock: a subclass of `Mock` with all the magic methods pre-created
- NonCallableMock: `Mock` non-callable varient
- NonCallableMagicMock: `MagicMock` non-callable varient
- patch: create a `Mock` object by `decorator` or `context manager`
- path.object: patch the named member (`attribute`) on an `object` (target) with a mock object.
- path.dict: __Patch a dictionary, or dictionary like object, and restore the dictionary to its original state after the test__. If it is a `mapping` then it must at least support `getting`, `setting` and `deleting` items plus iterating over keys.

### auto-specing

- patch: autospec
- create_autospec()

__For ensuring that the mock objects in your tests have the same api as the objects they are replacing, you can use auto-speccing.__ Auto-speccing can be done through the `autospec` argument to patch, or the `create_autospec()` function. __Auto-speccing creates mock objects that have the same attributes and methods as the objects they are replacing, and any functions and methods (including constructors) have the same call signature as the real object.__

### mock class

Mocks are `callable` and __create attributes as new mocks when you access them__. Accessing the same attribute will always return the same mock. __Mocks record how you use them, allowing you to make assertions about what your code has done to them.__

## Reference

https://docs.python.org/3/library/unittest.html

https://docs.python.org/3/library/unittest.mock.html#module-unittest.mock

https://docs.python.org/3/library/unittest.mock-examples.html