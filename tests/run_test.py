from tests.validation import test_validation
from tests.broadcast import test_broadcast

print('********************************')
print('TESTS: Schema validation')
test_validation.run_test()
print('********************************')
print('TESTS: Service broadcast')
test_broadcast.run_test()
print('********************************')